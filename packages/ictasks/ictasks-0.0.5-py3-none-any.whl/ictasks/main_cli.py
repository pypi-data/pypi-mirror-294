"""
Main entry point for ictasks
"""

import os
from pathlib import Path
import sys
import signal
import argparse
import logging

from iccore import logging_utils

from ictasks.session import Session
from ictasks.environment import (
    Environment,
    SlurmEnvironment,
    BasicEnvironment,
    autodetect_environment,
)
from ictasks.settings import TaskfarmSettings
from ictasks.worker_collection import WorkerCollection
from ictasks.tasks import TaskCollection, TaskLauncher

logger = logging.getLogger(__name__)


def on_sig_int(*_):
    """
    Signal handler for SIGINT
    """

    logger.info("Session interrupted by SIGINT. Please check for orphaned processes.")
    sys.exit(1)


def taskfarm(args):

    logging_utils.setup_default_logger()

    signal.signal(signal.SIGINT, on_sig_int)

    settings = TaskfarmSettings()

    workers = WorkerCollection(
        settings.get_cores_per_node(), settings.processes_per_node
    )

    env: Environment | None = None
    if args.env == "slurm":
        logger.info("Running in slurm environment")
        env = SlurmEnvironment(workers)
    elif args.env == "basic":
        logger.info("Running in basic environment")
        env = BasicEnvironment(workers, args.job_id, args.nodelist.split(","))
    else:
        logger.info("Trying to detect runtime environment")
        env = autodetect_environment(workers)

    tasks = TaskCollection(args.work_dir, settings.get("group_size"))
    tasks.read_taskfile(args.tasklist)

    launcher = TaskLauncher(settings.get("launcher"), settings.cores_per_task)

    session = Session(env, tasks, launcher, settings.get("sleep"), settings.get("keep"))
    logger.info("Starting session run")
    session.run()
    logger.info("Finished session run")


def main_cli():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )

    subparsers = parser.add_subparsers(required=True)

    taskfarm_parser = subparsers.add_parser("taskfarm")

    taskfarm_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Directory to run the session in",
    )
    taskfarm_parser.add_argument("--tasklist", type=Path, help="Path to tasklist file")
    taskfarm_parser.add_argument(
        "--nodelist", type=str, default="", help="List of system nodes to use"
    )
    taskfarm_parser.add_argument(
        "--jobid", type=str, default="", help="Identifier for this job"
    )
    taskfarm_parser.add_argument(
        "--env",
        type=str,
        default=" ",
        help="Environment to run the session in, 'slurm' or 'basic'",
    )

    taskfarm_parser.set_defaults(func=taskfarm)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
