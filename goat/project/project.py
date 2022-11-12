from __future__ import annotations
from itertools import chain
from pathlib import Path
from shutil import rmtree
from subprocess import STDOUT, run
from goat.project.project_builder import ProjectBuilder
from goat.project.project_configuration import ProjectConfiguration
from goat.project.project_initializer import ProjectInitializer


class Project:
    configuration: ProjectConfiguration

    @classmethod
    def from_path(cls, root_path: Path) -> Project:
        configuration_path = root_path / ProjectConfiguration.CONFIGURATION_FILE_NAME
        configuration = ProjectConfiguration.from_path(
            root_path,
            configuration_path,
        )

        return cls(configuration)

    @classmethod
    def new(cls, root_path: Path) -> Project:
        project = cls(ProjectConfiguration.default(root_path))
        ProjectInitializer.initialize(project.configuration)
        return project

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    def get_source_object_mapping(self, test: bool = False) -> dict[Path, Path]:
        binary_source_files = self.configuration.source_directory.glob("**/*.cc")
        test_source_files = self.configuration.test_directory.glob("**/*.cc")
        source_files = (
            chain(binary_source_files, test_source_files)
            if test
            else binary_source_files
        )

        source_object_mapping: dict[Path, Path] = {}

        for source_file in source_files:
            relative_source_file = source_file.relative_to(self.configuration.root_path)

            object_file = (
                self.configuration.object_directory
                / relative_source_file.parent
                / f"{relative_source_file.name}.o"
            )

            source_object_mapping[source_file] = object_file

        return source_object_mapping

    def build(self, test: bool = False) -> None:
        self.configuration.build_directory.mkdir(parents=True, exist_ok=True)
        self.configuration.object_directory.mkdir(parents=True, exist_ok=True)
        self.configuration.binary_directory.mkdir(parents=True, exist_ok=True)

        source_object_mapping = self.get_source_object_mapping(test)

        for source_file, object_file in source_object_mapping.items():
            print(f"Compiling {source_file}")
            object_file.parent.mkdir(parents=True, exist_ok=True)
            result = ProjectBuilder.compile_object_file(
                self.configuration,
                source_file,
                object_file,
                test,
            )

            if result.returncode != 0:
                print(result.stderr)
                return

        print(f"Linking {self.configuration.target_file(test)}")

        result = ProjectBuilder.link_binary_file(
            self.configuration,
            list(source_object_mapping.values()),
            self.configuration.target_file(test),
            test,
        )

        if result.returncode != 0:
            print(result.stderr)
            return

    def run(self, test: bool = False) -> None:
        result = run(self.configuration.target_file(test))
        print(f"Exit code: {result.returncode}")

    def clean(self) -> None:
        rmtree(self.configuration.build_directory)
