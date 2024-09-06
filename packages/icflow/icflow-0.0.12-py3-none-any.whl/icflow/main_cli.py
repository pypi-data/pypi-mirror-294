#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path

from ictasks.session import Session as TasksSession
from ictasks.environment import BasicEnvironment
from ictasks.worker_collection import WorkerCollection
from ictasks.tasks import TaskLauncher, TaskCollection

from icflow.session.parameter_sweep import ParameterSweep, ParameterSweepConfig

logger = logging.getLogger(__name__)


def sweep(args):

    workers = WorkerCollection(args.work_dir)
    env = BasicEnvironment(workers)
    launcher = TaskLauncher(args.stop_on_err)
    tasks = TaskCollection(args.work_dir)

    task_runner = TasksSession(env, tasks, launcher)

    config = ParameterSweepConfig()
    config.read(args.config)

    param_sweep = ParameterSweep(task_runner, config)
    param_sweep.run()


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    sweep_parser = subparsers.add_parser("sweep")
    sweep_parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the config file to use for sweep",
    )
    sweep_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the working directory for output",
    )
    sweep_parser.add_argument(
        "--program_path",
        type=Path | None,
        default=None,
        help="If specified, the launch program in the config is relative this path",
    )
    sweep_parser.add_argument(
        "--stop_on_err",
        action="store_true",
        dest="stop_on_err",
        default=False,
        help="Stop whole run if any process fails",
    )
    sweep_parser.set_defaults(func=sweep)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
