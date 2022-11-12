#!/usr/bin/env python3

"""
Author: Tom Lubin
Description: A C++ build system
"""

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from pathlib import Path
from goat.project.project import Project
from goat.project.project_configuration import ProjectConfiguration
from goat.raw_configuration.configuration_base import ConfigurationRoot
from toml import loads as toml_to_dict


def build_project() -> None:
    project = Project.load(Path.cwd())
    project.build()


def new_project(name: str) -> None:
    root_path = Path.cwd() / name
    Project.default(root_path).initialize()


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


def main() -> None:
    arguments = parse_arguments()

    match arguments.subcommand:
        case "build":
            build_project()

        case "new":
            new_project(arguments.name)

        case "test" | "run" | "clean":
            raise NotImplementedError()


if __name__ == "__main__":
    main()
