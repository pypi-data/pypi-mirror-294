# -*- coding: utf-8 -*-

"""
DB Snapshot to Data Lake Workflow Management.

This module provides a set of functions and a class to manage the workflow of
exporting database snapshots to a data lake. It offers both functional and
object-oriented programming approaches to suit different user needs and preferences.

**Functional API**:

The module includes step-by-step functions that can be used independently,
allowing for greater flexibility and customization of the workflow. These
functions cover various stages of the process, from planning the snapshot
export to executing the final data lake ingestion.

Key functions include:

- :func:`step_1_1_plan_snapshot_to_staging`: Plan the division of DB snapshot files.
- :func:`step_1_2_get_snapshot_to_staging_todo_list`: Retrieve the list of snapshot groups to process.
- :func:`step_1_3_process_db_snapshot_file_group_manifest_file`: Process individual snapshot groups.
- :func:`step_2_1_plan_staging_to_datalake`: Plan the merging of staging files into the data lake.
- :func:`step_2_2_get_staging_to_datalake_todo_list`: Get the list of staging file groups to process.
- :func:`step_2_3_process_partition_file_group_manifest_file`: Execute the compaction of staging files.

**Object-Oriented API**:

The module also provides a :class:`Project` class that encapsulates the entire workflow.
This class-based approach simplifies usage for those who prefer a more
streamlined, less customizable process. Users can initialize a Project instance
with all necessary parameters and then execute each step of the workflow using
class methods.

Key methods of the Project class include:

- :meth:`Project.step_1_1_plan_snapshot_to_staging`
- :meth:`Project.step_1_2_process_db_snapshot_file_group_manifest_file`
- :meth:`Project.step_2_1_plan_staging_to_datalake`
- :meth:`Project.step_2_2_process_partition_file_group_manifest_file`

The functional API offers more flexibility for advanced users who need to extend
or customize the workflow, while the class-based API provides a simpler interface
for users who want to quickly implement the standard workflow with minimal setup.

This module is designed to be part of a larger data processing ecosystem,
integrating with other components for S3 interactions, manifest file handling,
and data transformations.
"""

import typing as T
import dataclasses
from functools import cached_property

import polars as pl
from pynamodb_mate.api import Connection
from s3pathlib import S3Path
from s3manifesto.api import ManifestFile
from polars_writer.api import Writer
from .vendor.vislog import VisLog

from .typehint import T_OPTIONAL_KWARGS
from .utils import repr_data_size
from .s3_loc import S3Location
from .logger import dummy_logger
from .snapshot_to_staging import DBSnapshotManifestFile
from .snapshot_to_staging import DBSnapshotFileGroupManifestFile
from .snapshot_to_staging import StagingFileGroupManifestFile
from .snapshot_to_staging import T_BatchReadSnapshotDataFileCallable
from .snapshot_to_staging import process_db_snapshot_file_group_manifest_file
from .staging_to_datalake import PartitionFileGroupManifestFile
from .staging_to_datalake import process_partition_file_group_manifest_file
from .validate_datalake import ValidateDatalakeResult
from .validate_datalake import validate_datalake
from .tracker import create_orm_model
from .tracker import T_TASK

if T.TYPE_CHECKING:  # pragma: no cover
    from boto_session_manager import BotoSesManager
    from mypy_boto3_s3.client import S3Client


def print_manifest_file_info(
    manifest_file: ManifestFile,
    logger,
):
    """
    A helper function to print the summary of a manifest file.
    """
    # fmt: off
    logger.info(f"Process manifest file: {manifest_file.fingerprint}")
    logger.info(f"  manifest summary: {manifest_file.uri_summary}")
    logger.info(f"    preview at: {S3Path.from_s3_uri(manifest_file.uri_summary).console_url}")
    logger.info(f"  manifest data: {manifest_file.uri}")
    logger.info(f"    preview at: {S3Path.from_s3_uri(manifest_file.uri).console_url}")
    logger.info(f"  total files: {len(manifest_file.data_file_list)}")
    logger.info(f"  total size: {repr_data_size(manifest_file.size)}")
    logger.info(f"  total n_record: {manifest_file.n_record}")
    # fmt: on


def step_1_1_plan_snapshot_to_staging(
    s3_client: "S3Client",
    s3_loc: S3Location,
    db_snapshot_manifest_file: DBSnapshotManifestFile,
    target_size: int,
    logger=dummy_logger,
) -> T.List[DBSnapshotFileGroupManifestFile]:
    print_manifest_file_info(
        manifest_file=db_snapshot_manifest_file,
        logger=logger,
    )
    logger.info(
        f"Divide db snapshot files into {repr_data_size(target_size)}-sized groups"
    )
    db_snapshot_file_group_manifest_file_list = (
        db_snapshot_manifest_file.split_into_groups(
            s3_loc=s3_loc,
            s3_client=s3_client,
            target_size=target_size,
        )
    )
    logger.info(f"  got {len(db_snapshot_file_group_manifest_file_list)} groups")
    return db_snapshot_file_group_manifest_file_list


def step_1_2_get_snapshot_to_staging_todo_list(
    s3_client: "S3Client",
    s3_loc: S3Location,
) -> T.List[DBSnapshotFileGroupManifestFile]:
    db_snapshot_file_group_manifest_file_list = (
        DBSnapshotFileGroupManifestFile.read_all_groups(
            s3_loc=s3_loc,
            s3_client=s3_client,
        )
    )
    return db_snapshot_file_group_manifest_file_list


def step_1_3_process_db_snapshot_file_group_manifest_file(
    db_snapshot_file_group_manifest_file: DBSnapshotFileGroupManifestFile,
    s3_client: "S3Client",
    s3_loc: S3Location,
    batch_read_snapshot_data_file_func: T_BatchReadSnapshotDataFileCallable,
    partition_keys: T.List[str],
    sort_by: T.Optional[T.List[str]] = None,
    descending: T.Union[bool, T.List[bool]] = False,
    s3pathlib_write_bytes_kwargs: T_OPTIONAL_KWARGS = None,
    logger=dummy_logger,
) -> StagingFileGroupManifestFile:
    print_manifest_file_info(
        manifest_file=db_snapshot_file_group_manifest_file,
        logger=logger,
    )
    logger.info("Transform and write data files ...")
    staging_file_group_manifest_file = process_db_snapshot_file_group_manifest_file(
        db_snapshot_file_group_manifest_file=db_snapshot_file_group_manifest_file,
        batch_read_snapshot_data_file_func=batch_read_snapshot_data_file_func,
        s3_client=s3_client,
        partition_keys=partition_keys,
        sort_by=sort_by,
        descending=descending,
        s3_loc=s3_loc,
        s3pathlib_write_bytes_kwargs=s3pathlib_write_bytes_kwargs,
        logger=logger,
    )
    return staging_file_group_manifest_file


def step_2_1_plan_staging_to_datalake(
    s3_client: "S3Client",
    s3_loc: S3Location,
    target_size: int = 128_000_000,  # 128 MB
    logger=dummy_logger,
) -> T.List[PartitionFileGroupManifestFile]:
    logger.info(
        f"Merge partition data files into {repr_data_size(target_size)} sized files"
    )
    partition_file_group_manifest_file_list = (
        PartitionFileGroupManifestFile.plan_partition_compaction(
            s3_loc=s3_loc,
            s3_client=s3_client,
            target_size=target_size,
        )
    )
    logger.info(
        f"  got {len(partition_file_group_manifest_file_list)} compaction job todo."
    )
    return partition_file_group_manifest_file_list


def step_2_2_get_staging_to_datalake_todo_list(
    s3_client: "S3Client",
    s3_loc: S3Location,
) -> T.List[PartitionFileGroupManifestFile]:
    partition_file_group_manifest_file_list = (
        PartitionFileGroupManifestFile.read_all_groups(
            s3_loc=s3_loc,
            s3_client=s3_client,
        )
    )
    return partition_file_group_manifest_file_list


def step_2_3_process_partition_file_group_manifest_file(
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
    print_manifest_file_info(
        manifest_file=partition_file_group_manifest_file,
        logger=logger,
    )
    s3path = process_partition_file_group_manifest_file(
        partition_file_group_manifest_file=partition_file_group_manifest_file,
        s3_client=s3_client,
        s3_loc=s3_loc,
        polars_writer=polars_writer,
        gzip_compress=gzip_compress,
        sort_by=sort_by,
        descending=descending,
        s3pathlib_write_bytes_kwargs=s3pathlib_write_bytes_kwargs,
        logger=logger,
    )
    return s3path


def step_3_1_validate_datalake(
    s3_client: "S3Client",
    s3_loc: S3Location,
    db_snapshot_manifest_file: DBSnapshotManifestFile,
    polars_writer: T.Optional[Writer] = None,
    count_column: T.Optional[str] = None,
    logger=dummy_logger,
) -> ValidateDatalakeResult:
    return validate_datalake(
        s3_client=s3_client,
        s3_loc=s3_loc,
        db_snapshot_manifest_file=db_snapshot_manifest_file,
        polars_writer=polars_writer,
        count_column=count_column,
        logger=logger,
    )


logger = VisLog(name="dbsnaplake", log_format="%(message)s")


class UseCaseIdSuffixEnum:
    # fmt: off
    step_0_prepare_db_snapshot_manifest = "step_0_prepare_db_snapshot_manifest"
    step_1_1_plan_snapshot_to_staging = "step_1_1_plan_snapshot_to_staging"
    step_1_2_process_db_snapshot_file_group_manifest_file = "step_1_2_process_db_snapshot_file_group_manifest_file"
    step_2_1_plan_staging_to_datalake = "step_2_1_plan_staging_to_datalake"
    step_2_2_process_partition_file_group_manifest_file = "step_2_2_process_partition_file_group_manifest_file"
    step_3_1_validate_datalake = "step_3_1_validate_datalake"
    # fmt: on


@dataclasses.dataclass
class Project:
    """
    Manages the workflow for converting database snapshots to a data lake format.

    This class encapsulates the entire process of exporting database snapshots,
    transforming them, and ingesting them into a data lake. It provides methods
    for each step of the workflow and manages the state using DynamoDB tables.

    :param s3_client: Initialized boto3 S3 client for S3 operations.
    :param s3uri_db_snapshot_manifest_summary: S3 URI of the DB snapshot manifest summary.
    :param s3uri_staging: S3 URI for storing intermediate staging data.
    :param s3uri_datalake: S3 URI for the final data lake storage.
    :param target_db_snapshot_file_group_size: Target size for DB snapshot file groups.
    :param partition_keys: list of partition keys.
    :param create_datalake: if False, skip the data lake ingestion step. We end up
        with a parquet datalake in the staging folder.
    :param sort_by: list of columns to sort by. for example: ["create_time"].
        use empty list or None if no sorting is needed.
    :param descending: list of boolean values to indicate the sorting order.
        for example: [True] or [False, True].
    :param target_parquet_file_size: Target size for output parquet files.
    :param polars_writer: `polars_writer.Writer <https://github.com/MacHu-GWU/polars_writer-project>`_ object.
    :param gzip_compress: Flag to enable GZIP compression.
    :param count_column: Name of the column to use for counting records.
    :param tracker_table_name: Name of the DynamoDB table for tracking tasks.
    :param aws_region: AWS region for the DynamoDB tracker table.
    :param use_case_id: Unique identifier for this specific use case.

    **Methods**

    - :meth:`connect_dynamodb`: Initializes connections to DynamoDB tables for task tracking.
    - :meth:`step_1_1_plan_snapshot_to_staging`: Plans the division of DB snapshot files.
    - :meth:`step_1_2_process_db_snapshot_file_group_manifest_file`: Processes snapshot groups.
    - :meth:`step_2_1_plan_staging_to_datalake`: Plans the merging of staging files.
    - :meth:`step_2_2_process_partition_file_group_manifest_file`: Executes file compaction.
    """

    s3_client: "S3Client" = dataclasses.field()
    s3uri_db_snapshot_manifest_summary: str = dataclasses.field()
    s3uri_staging: str = dataclasses.field()
    s3uri_datalake: str = dataclasses.field()
    target_db_snapshot_file_group_size: int = dataclasses.field()
    partition_keys: T.Optional[T.List[str]] = dataclasses.field()
    create_datalake: bool = dataclasses.field()
    sort_by: T.Optional[T.List[str]] = dataclasses.field()
    descending: T.Union[bool, T.List[bool]] = dataclasses.field()
    target_parquet_file_size: int = dataclasses.field()
    polars_writer: T.Optional[Writer] = dataclasses.field()
    gzip_compression: bool = dataclasses.field()
    count_column: T.Optional[str] = dataclasses.field()
    tracker_table_name: str = dataclasses.field()
    aws_region: str = dataclasses.field()
    use_case_id: str = dataclasses.field()

    def __post_init__(self):
        if isinstance(self.polars_writer, Writer) is False:
            self.polars_writer = Writer(
                format="parquet",
                parquet_compression="snappy",
            )

    @cached_property
    def s3_loc(self) -> S3Location:
        """
        Access the :class:`~dbsnaplake.s3_loc.S3Location` object for this project.
        """
        return S3Location(
            s3uri_staging=self.s3uri_staging,
            s3uri_datalake=self.s3uri_datalake,
        )

    @cached_property
    def db_snapshot_manifest_file(self) -> DBSnapshotManifestFile:
        """
        Access the :class:`~dbsnaplake.snapshot_to_staging.DBSnapshotManifestFile`
        object for this project.
        """
        return DBSnapshotManifestFile.read(
            uri_summary=self.s3uri_db_snapshot_manifest_summary,
            s3_client=self.s3_client,
        )

    def batch_read_snapshot_data_file(
        self,
        db_snapshot_file_group_manifest_file: DBSnapshotFileGroupManifestFile,
        **kwargs,
    ) -> pl.DataFrame:
        """
        You have to override this method and implement the logic to read the
        snapshot data file into a Polars DataFrame.
        """
        raise NotImplementedError

    @cached_property
    def task_model_step_0_prepare_db_snapshot_manifest(self) -> T.Type[T_TASK]:
        """
        Access the DynamoDB Status Tracking ORM model for step_0.

        .. note::

            This property is created only once and has to be cached.


        """
        return create_orm_model(
            tracker_table_name=self.tracker_table_name,
            aws_region=self.aws_region,
            use_case_id=f"{self.use_case_id}#{UseCaseIdSuffixEnum.step_0_prepare_db_snapshot_manifest}",
        )

    @cached_property
    def task_model_step_1_1_plan_snapshot_to_staging(self) -> T.Type[T_TASK]:
        """
        Access the DynamoDB Status Tracking ORM model for step_1_1.

        .. note::

            This property is created only once and has to be cached.
        """
        return create_orm_model(
            tracker_table_name=self.tracker_table_name,
            aws_region=self.aws_region,
            use_case_id=f"{self.use_case_id}#{UseCaseIdSuffixEnum.step_1_1_plan_snapshot_to_staging}",
        )

    @cached_property
    def task_model_step_1_2_process_db_snapshot_file_group_manifest_file(
        self,
    ) -> T.Type[T_TASK]:
        """
        Access the DynamoDB Status Tracking ORM model for step_1_2.

        .. note::

            This property is created only once and has to be cached.
        """
        return create_orm_model(
            tracker_table_name=self.tracker_table_name,
            aws_region=self.aws_region,
            use_case_id=f"{self.use_case_id}#{UseCaseIdSuffixEnum.step_1_2_process_db_snapshot_file_group_manifest_file}",
        )

    @cached_property
    def task_model_step_2_1_plan_staging_to_datalake(self) -> T.Type[T_TASK]:
        """
        Access the DynamoDB Status Tracking ORM model for step_2_1.

        .. note::

            This property is created only once and has to be cached.
        """
        return create_orm_model(
            tracker_table_name=self.tracker_table_name,
            aws_region=self.aws_region,
            use_case_id=f"{self.use_case_id}#{UseCaseIdSuffixEnum.step_2_1_plan_staging_to_datalake}",
        )

    @cached_property
    def task_model_step_2_2_process_partition_file_group_manifest_file(
        self,
    ) -> T.Type[T_TASK]:
        """
        Access the DynamoDB Status Tracking ORM model for step_2_2.

        .. note::

            This property is created only once and has to be cached.
        """
        return create_orm_model(
            tracker_table_name=self.tracker_table_name,
            aws_region=self.aws_region,
            use_case_id=f"{self.use_case_id}#{UseCaseIdSuffixEnum.step_2_2_process_partition_file_group_manifest_file}",
        )

    def connect_dynamodb(self, bsm: "BotoSesManager"):
        """
        Configure the DynamoDB ORM python library to use the right AWS credential.
        """
        with bsm.awscli():
            conn = Connection(region=bsm.aws_region)
            for Model in [
                self.task_model_step_0_prepare_db_snapshot_manifest,
                self.task_model_step_1_1_plan_snapshot_to_staging,
                self.task_model_step_1_2_process_db_snapshot_file_group_manifest_file,
                self.task_model_step_2_1_plan_staging_to_datalake,
                self.task_model_step_2_2_process_partition_file_group_manifest_file,
            ]:
                Model._connection = None
                Model.Meta.region = bsm.aws_region
                Model.create_table(wait=True)

    @logger.start_and_end(
        msg="{func_name}",
    )
    def step_1_1_plan_snapshot_to_staging(self):
        task_id = self.db_snapshot_manifest_file.uri_summary
        Task = self.task_model_step_1_1_plan_snapshot_to_staging
        task = Task.get_one_or_none(task_id=task_id)
        if task is None:
            task = Task.make_and_save(
                task_id=task_id,
                data={"uri_summary": self.db_snapshot_manifest_file.uri_summary},
            )
        if task.is_succeeded():
            return

        with Task.start(task_id=task_id, debug=True) as exec_ctx:
            db_snapshot_file_group_manifest_file_list = (
                step_1_1_plan_snapshot_to_staging(
                    s3_client=self.s3_client,
                    s3_loc=self.s3_loc,
                    db_snapshot_manifest_file=self.db_snapshot_manifest_file,
                    target_size=self.target_db_snapshot_file_group_size,
                    logger=logger,
                )
            )
            n = len(db_snapshot_file_group_manifest_file_list)
            exec_ctx.set_data({"n_db_snapshot_file_group_manifest_file": n})

            SubTask = (
                self.task_model_step_1_2_process_db_snapshot_file_group_manifest_file
            )
            with SubTask.batch_write() as batch:
                for (
                    db_snapshot_file_group_manifest_file
                ) in db_snapshot_file_group_manifest_file_list:
                    sub_task_id = db_snapshot_file_group_manifest_file.uri_summary
                    sub_task = SubTask.make(
                        task_id=sub_task_id,
                        data={
                            "uri_summary": db_snapshot_file_group_manifest_file.uri_summary,
                        },
                    )
                    batch.save(sub_task)

        # task = Task.get_one_or_none(task_id=task_id)  # for debug only
        # print(task.attribute_values)  # for debug only
        return db_snapshot_file_group_manifest_file_list

    @logger.start_and_end(
        msg="{func_name}",
    )
    def step_1_2_process_db_snapshot_file_group_manifest_file(
        self,
    ) -> T.List[StagingFileGroupManifestFile]:
        Task = self.task_model_step_1_2_process_db_snapshot_file_group_manifest_file
        task_list = Task.query_for_unfinished(limit=999, auto_refresh=True)
        new_step_1_3_process_db_snapshot_file_group_manifest_file = (
            logger.start_and_end(
                msg="{func_name}",
            )(step_1_3_process_db_snapshot_file_group_manifest_file)
        )
        staging_file_group_manifest_file_list = list()
        for task in task_list:
            db_snapshot_file_group_manifest_file = DBSnapshotFileGroupManifestFile.read(
                uri_summary=task.data["uri_summary"],
                s3_client=self.s3_client,
            )
            with logger.nested():
                with Task.start(task_id=task.task_id, debug=True) as exec_ctx:
                    staging_file_group_manifest_file: StagingFileGroupManifestFile = (
                        new_step_1_3_process_db_snapshot_file_group_manifest_file(
                            db_snapshot_file_group_manifest_file=db_snapshot_file_group_manifest_file,
                            s3_client=self.s3_client,
                            s3_loc=self.s3_loc,
                            batch_read_snapshot_data_file_func=self.batch_read_snapshot_data_file,
                            partition_keys=self.partition_keys,
                            sort_by=self.sort_by,
                            descending=self.descending,
                            logger=logger,
                        )
                    )
                    staging_file_group_manifest_file_list.append(
                        staging_file_group_manifest_file
                    )
                    uri = staging_file_group_manifest_file.uri_summary
                    exec_ctx.set_data(
                        {"staging_file_group_manifest_file_uri_summary": uri}
                    )
                # task = Task.get_one_or_none(task_id=task_id)  # for debug only
                # print(task.attribute_values)  # for debug only
        return staging_file_group_manifest_file_list

    @logger.start_and_end(
        msg="{func_name}",
    )
    def step_2_1_plan_staging_to_datalake(
        self,
    ) -> T.List[PartitionFileGroupManifestFile]:
        if self.create_datalake is False:  # pragma: no cover
            raise ValueError("no_datalake flag is set to True")
        Task = self.task_model_step_2_1_plan_staging_to_datalake
        task_id = self.s3_loc.s3dir_staging_file_group_manifest.uri
        task = Task.get_one_or_none(task_id=task_id)
        if task is None:
            task = Task.make_and_save(task_id=task_id)
        if task.is_succeeded():
            return

        with Task.start(task_id=task_id, debug=True) as exec_ctx:
            partition_file_group_manifest_file_list = step_2_1_plan_staging_to_datalake(
                s3_client=self.s3_client,
                s3_loc=self.s3_loc,
                target_size=self.target_parquet_file_size,
                logger=logger,
            )
            n = len(partition_file_group_manifest_file_list)
            exec_ctx.set_data({"n_partition_file_group_manifest_file": n})

            SubTask = (
                self.task_model_step_2_2_process_partition_file_group_manifest_file
            )
            with SubTask.batch_write() as batch:
                for (
                    partition_file_group_manifest_file
                ) in partition_file_group_manifest_file_list:
                    sub_task_id = partition_file_group_manifest_file.uri_summary
                    sub_task = SubTask.make(
                        task_id=sub_task_id,
                        data={
                            "uri_summary": partition_file_group_manifest_file.uri_summary,
                        },
                    )
                    batch.save(sub_task)

        # task = Task.get_one_or_none(task_id=task_id)  # for debug only
        # print(task.attribute_values)  # for debug only
        return partition_file_group_manifest_file_list

    @logger.start_and_end(
        msg="{func_name}",
    )
    def step_2_2_process_partition_file_group_manifest_file(self) -> T.List[S3Path]:
        if self.create_datalake is False:  # pragma: no cover
            raise ValueError("no_datalake flag is set to True")
        Task = self.task_model_step_2_2_process_partition_file_group_manifest_file
        task_list = Task.query_for_unfinished(limit=999, auto_refresh=True)
        new_step_2_3_process_partition_file_group_manifest_file = logger.start_and_end(
            msg="{func_name}",
        )(step_2_3_process_partition_file_group_manifest_file)
        s3path_list = list()
        for task in task_list:
            partition_file_group_manifest_file = PartitionFileGroupManifestFile.read(
                uri_summary=task.data["uri_summary"],
                s3_client=self.s3_client,
            )
            with logger.nested():
                with Task.start(task_id=task.task_id, debug=True) as exec_ctx:
                    s3path = new_step_2_3_process_partition_file_group_manifest_file(
                        partition_file_group_manifest_file=partition_file_group_manifest_file,
                        s3_client=self.s3_client,
                        s3_loc=self.s3_loc,
                        polars_writer=self.polars_writer,
                        gzip_compress=self.gzip_compression,
                        sort_by=self.sort_by,
                        descending=self.descending,
                        logger=logger,
                    )
                    s3path_list.append(s3path)
                    exec_ctx.set_data({"parquet_uri": s3path.uri})
                # task = Task.get_one_or_none(task_id=task_id)  # for debug only
                # print(task.attribute_values)  # for debug only
        return s3path_list

    @logger.start_and_end(
        msg="{func_name}",
    )
    def step_3_1_validate_datalake(self) -> ValidateDatalakeResult:
        if self.create_datalake is False:  # pragma: no cover
            raise ValueError("no_datalake flag is set to True")
        return step_3_1_validate_datalake(
            s3_client=self.s3_client,
            s3_loc=self.s3_loc,
            db_snapshot_manifest_file=self.db_snapshot_manifest_file,
            polars_writer=self.polars_writer,
            count_column=self.count_column,
            logger=logger,
        )
