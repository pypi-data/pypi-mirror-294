# -*- coding: utf-8 -*-

"""
This module defines the abstraction of the transformation process from
Staging Data File to Final Datalake.
"""

import typing as T
import dataclasses

import polars as pl
from s3pathlib import S3Path
from s3manifesto.api import KeyEnum, ManifestFile
from polars_writer.api import Writer

from .typehint import T_OPTIONAL_KWARGS
from .partition import Partition
from .s3_loc import S3Location
from .polars_utils import (
    write_to_s3,
    read_parquet_from_s3,
    read_many_parquet_from_s3,
)
from .logger import dummy_logger

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3.client import S3Client


def extract_s3_directory(
    s3uri_col_name: str,
    s3dir_col_name: str,
) -> pl.Expr:
    """
    Generate a Polars expression to extract the directory part of S3 URIs.

    :param s3uri_col_name: Name of the column containing S3 URIs.
    :param s3dir_col_name: Name for the new column to store S3 directories.

    :return: Polars expression for extracting S3 directories.

    Example:
        If "s3uri_col_name" contains ``s3://bucket/path/to/file``,
        the resulting "s3dir_col_name" will contain ``s3://bucket/path/to/``.
    """
    return pl.concat_str(
        [
            pl.col(s3uri_col_name)
            .str.split("/")
            .list.slice(
                0,
                pl.col(s3uri_col_name).str.split("/").list.len() - 1,
            )
            .list.join("/"),
            pl.lit("/"),
        ]
    ).alias(s3dir_col_name)


PARTITION_URI = "partition_uri"


@dataclasses.dataclass
class PartitionFileGroupManifestFile(ManifestFile):
    """
    Represents a group of files across many partitions in the staging area.

    This class extends
    `ManifestFile <https://s3manifesto.readthedocs.io/en/latest/s3manifesto/manifest.html#module-s3manifesto.manifest>`_
    to provide specific functionality for handling partition file groups during
    the compaction process.
    """

    @classmethod
    def plan_partition_compaction(
        cls,
        s3_loc: S3Location,
        s3_client: "S3Client",
        target_size: int = 128_000_000,  # 128 MB
    ):
        """
        Plan the compaction of partition file groups.

        This method reads staging file group manifests, groups them by partition,
        and creates new partition file group manifests for compaction.

        :param s3_loc: S3 location information.
        :param s3_client: Boto3 S3 client.
        :param target_size: Target size for compacted files. Default is 128 MB.

        :return: List of planned partition file group manifests.
        """
        # read all staging file group manifest files
        s3path_list = s3_loc.s3dir_staging_file_group_manifest_data.iter_objects(
            bsm=s3_client
        ).all()
        df = read_many_parquet_from_s3(
            s3path_list=s3path_list,
            s3_client=s3_client,
        )

        # group by partition
        df = df.with_columns(
            extract_s3_directory(
                s3uri_col_name=KeyEnum.URI,
                s3dir_col_name=PARTITION_URI,
            ),
        )
        partition_file_group_manifest_file_list = list()
        for ith_partition, ((partition_uri,), sub_df) in enumerate(
            df.group_by(*[PARTITION_URI]),
            start=1,
        ):
            sub_df = sub_df.drop([PARTITION_URI])
            data_file_list = sub_df.to_dicts()
            master_partition_file_group_manifest_file = (
                PartitionFileGroupManifestFile.new(
                    uri="",
                    uri_summary="",
                    data_file_list=data_file_list,
                    calculate=True,
                )
            )

            # with in each partition, group files into tasks by size
            for ith, (
                file_group,
                total_size,
            ) in enumerate(
                master_partition_file_group_manifest_file.group_files_into_tasks_by_size(
                    target_size=target_size,
                ),
                start=1,
            ):
                partition_file_group_manifest_file = PartitionFileGroupManifestFile.new(
                    uri=s3_loc.s3dir_partition_file_group_manifest_data.joinpath(
                        f"manifest-data-{ith_partition}-{ith}.parquet"
                    ).uri,
                    uri_summary=s3_loc.s3dir_partition_file_group_manifest_summary.joinpath(
                        f"manifest-summary-{ith_partition}-{ith}.parquet"
                    ).uri,
                    data_file_list=file_group,
                    details={
                        PARTITION_URI: partition_uri,
                    },
                    calculate=True,
                )
                partition_file_group_manifest_file.write(s3_client=s3_client)
                partition_file_group_manifest_file_list.append(
                    partition_file_group_manifest_file
                )
        return partition_file_group_manifest_file_list

    @classmethod
    def read_all_groups(
        cls,
        s3_loc: S3Location,
        s3_client: "S3Client",
    ) -> T.List["PartitionFileGroupManifestFile"]:
        """
        Read all partition file group manifest files from the specified S3 location.

        :param s3_loc: S3 location information.
        :param s3_client: Boto3 S3 client.

        :returns: List of all file group manifest files.
        """
        s3path_list = s3_loc.s3dir_partition_file_group_manifest_summary.iter_objects(
            bsm=s3_client,
        ).all()
        partition_file_group_manifest_file_list = [
            PartitionFileGroupManifestFile.read(
                uri_summary=s3path.uri,
                s3_client=s3_client,
            )
            for s3path in s3path_list
        ]
        return partition_file_group_manifest_file_list


def process_partition_file_group_manifest_file(
    partition_file_group_manifest_file: PartitionFileGroupManifestFile,
    s3_client: "S3Client",
    s3_loc: S3Location,
    polars_writer: T.Optional[Writer] = None,
    gzip_compress: bool = False,
    sort_by: T.Optional[T.List[str]] = None,
    descending: T.Union[bool, T.List[bool]] = False,
    s3pathlib_write_bytes_kwargs: T_OPTIONAL_KWARGS = None,
    logger=dummy_logger,
) -> S3Path:
    """
    Execute the compaction process for a partition file group.

    This function reads all data files in the manifest, (optional) sorts them by
    the specified fields, and writes a single compacted file to the final
    data lake location.

    :param partition_file_group_manifest_file: Manifest file for the partition group.
    :param s3_client: Boto3 S3 client.
    :param s3_loc: S3 location information.
    :param polars_writer: `polars_writer.Writer <https://github.com/MacHu-GWU/polars_writer-project>`_ object.
    :param gzip_compress: Flag to enable GZIP compression.
    :param sort_by: List of column names to sort by.
    :param descending: List of boolean values to specify descending order.
    :param polars_write_parquet_kwargs: Custom keyword arguments for Polars' write_parquet method.
    :param s3pathlib_write_bytes_kwargs: Custom keyword arguments for S3Path's write_bytes method.
    :param logger: logger for logging operations.

    :return: S3 path of the compacted file in the data lake.

    .. note::

        This method only support writing data to S3. If your datalake is a
        datawarehouse / database liked system, you can ingest the data from the
        s3 datalake to the datawarehouse / database after doing this.
    """
    partition_uri = partition_file_group_manifest_file.details[PARTITION_URI]
    s3dir_partition = S3Path.from_s3_uri(partition_uri)
    logger.info(f"Execute compaction on partition: {partition_uri}")
    logger.info(f"  preview output at: {s3dir_partition.console_url}")

    # Read all the data file in this manifest, sort by update_at_col
    logger.info(f"Read all staging data files ...")
    sub_df_list = list()
    for data_file in partition_file_group_manifest_file.data_file_list:
        uri = data_file[KeyEnum.URI]
        s3path = S3Path.from_s3_uri(uri)
        logger.info(f"  Read: {uri}")
        sub_df = read_parquet_from_s3(s3path=s3path, s3_client=s3_client)
        sub_df_list.append(sub_df)
    df = pl.concat(sub_df_list)
    if sort_by:
        df = df.sort(by=sort_by, descending=descending)

    # prepare writer parameters
    if s3dir_partition.uri == s3_loc.s3dir_staging_datalake.uri:
        s3dir_datalake_partition = s3_loc.s3dir_datalake
    else:
        _relpath = s3dir_partition.relative_to(s3_loc.s3dir_staging_datalake)
        s3dir_datalake_partition = s3_loc.s3dir_datalake.joinpath(_relpath).to_dir()
    if s3pathlib_write_bytes_kwargs is None:
        s3pathlib_write_bytes_kwargs = {}
    if polars_writer is None:
        polars_writer = Writer(
            format="parquet",
            parquet_compression="snappy",
        )
    fname = partition_file_group_manifest_file.fingerprint
    # write to datalake
    logger.info(f"Write merged files to {s3dir_datalake_partition.uri} ...")
    console_url = s3dir_datalake_partition.console_url
    logger.info(f"  preview partition folder at: {console_url}")
    if polars_writer.is_delta():
        if polars_writer.delta_mode != "append":  # pragma: no cover
            raise ValueError(
                "For writing initial data to deltalake, the mode has to be 'append'!"
            )
        # for delta lake, we need to add partition columns to the dataframe
        partition = Partition.from_uri(
            s3uri=s3dir_partition.uri,
            s3uri_root=s3_loc.s3dir_staging_datalake.uri,
        )
        for k, v in partition.data.items():
            df = df.with_columns(pl.lit(v).alias(k))
        s3dir_datalake = s3_loc.s3dir_datalake
        polars_writer.write(df, file_args=[s3dir_datalake.uri])
        s3path_new = s3dir_datalake_partition
    else:
        s3path_new, _, _ = write_to_s3(
            df=df,
            s3_client=s3_client,
            polars_writer=polars_writer,
            gzip_compress=gzip_compress,
            s3pathlib_write_bytes_kwargs=s3pathlib_write_bytes_kwargs,
            s3dir=s3dir_datalake_partition,
            fname=fname,
        )
        logger.info(f"Write s3 file to {s3path_new.uri} ...")
        logger.info(f"  preview s3 file at: {s3path_new.console_url}")
    return s3path_new
