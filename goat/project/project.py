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

    def build(self, test: bool = False) -> None:
        ProjectBuilder.build_target_file(self.configuration, test)

    def run(self, test: bool = False) -> None:
        result = run(self.configuration.target_file(test))
        print(f"Exit code: {result.returncode}")

    def clean(self) -> None:
        rmtree(self.configuration.build_directory)
