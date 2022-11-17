#!/usr/bin/env python3

"""
C/C++ build system.
"""

from sys import stdout
from loguru import logger
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path
from goat.project.project import Project

LOGGER_FORMAT = "[ {time:YYYY-MM-DD HH:mm:ss.SSS} ] | <level>{message}</level>"


def setup_logger() -> None:
    logger.remove()
    logger.add(sink=stdout, format=LOGGER_FORMAT, level="TRACE")
    logger.configure(
        levels=[
            dict(name="TRACE", color="<white>"),
            dict(name="INFO", color="<white><bold>"),
            dict(name="ERROR", color="<red><bold>"),
            dict(name="SUCCESS", color="<green><bold>"),
        ]
    )


def parse_arguments() -> Namespace:
    argument_parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )

    subparsers = argument_parser.add_subparsers(dest="subcommand", required=True)

    subparsers.add_parser("build", help="Build the current project")

    subparsers.add_parser("test", help="Test the current project")

    subparsers.add_parser("run", help="Run the current project")

    subparsers.add_parser("clean", help="Clean all built artifacts")

    new_parser = subparsers.add_parser("new", help="Create a new project")
    new_parser.add_argument("name", help="The project name")

    return argument_parser.parse_args()


def entry() -> None:
    setup_logger()
    arguments = parse_arguments()

    try:

        match arguments.subcommand:
            case "build":
                project = Project.from_path(Path.cwd())
                project.build()

            case "new":
                Project.new(Path.cwd() / arguments.name)

            case "run":
                project = Project.from_path(Path.cwd())
                project.build()
                project.run()

            case "test":
                project = Project.from_path(Path.cwd())
                project.build(test=True)
                project.run(test=True)

            case "clean":
                project = Project.from_path(Path.cwd())
                project.clean()

    except Exception as exception:
        logger.error(f"An error has occurred:")
        print(exception)

    else:
        logger.success("Done")
