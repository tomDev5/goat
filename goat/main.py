"""
C/C++ build system.
"""

from sys import stdout
from loguru import logger
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path
from goat.project.build_mode import BuildMode
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


def add_mode_arguments(subparser: ArgumentParser) -> None:
    group = subparser.add_mutually_exclusive_group()

    group.add_argument(
        "--mode",
        help=f"Select the configuration to use",
        type=BuildMode,
        choices=list(BuildMode),
        default=BuildMode.RELEASE,
    )

    for mode in BuildMode:
        group.add_argument(
            f"--{mode}",
            action="store_const",
            const=mode,
            dest="mode",
            help=f"Use the {mode} configuration",
        )


def parse_arguments() -> Namespace:
    argument_parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )

    subparsers = argument_parser.add_subparsers(dest="subcommand", required=True)

    build_parser = subparsers.add_parser("build", help="Build the current project")
    add_mode_arguments(build_parser)

    run_subparser = subparsers.add_parser("run", help="Run the current project")
    add_mode_arguments(run_subparser)

    subparsers.add_parser("clean", help="Clean all built artifacts")

    new_parser = subparsers.add_parser("new", help="Create a new project")
    new_parser.add_argument("name", help="The project name")

    return argument_parser.parse_args()


def main() -> int:
    setup_logger()
    arguments = parse_arguments()

    try:
        match arguments.subcommand:
            case "build":
                project = Project.from_path(Path.cwd())
                project.build(arguments.mode)

            case "new":
                Project.new(Path.cwd() / arguments.name)

            case "run":
                project = Project.from_path(Path.cwd())
                project.build(arguments.mode)
                project.run(arguments.mode)

            case "clean":
                project = Project.from_path(Path.cwd())
                project.clean()

    except Exception as exception:
        logger.error(f"An error has occurred:")
        logger.exception(exception)
        return 1

    else:
        logger.success("Done")
        return 0


if __name__ == "__main__":
    main()
