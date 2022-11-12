from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from subprocess import run
from goat.project.project_builder import ProjectBuilder
from goat.project.project_configuration import ProjectConfiguration
from goat.project.project_initializer import ProjectInitializer
from loguru import logger


class Project:
    configuration: ProjectConfiguration

    @classmethod
    def from_path(cls, root_path: Path) -> Project:
        logger.info(f"Loading project '{root_path.name}'")
        configuration_path = root_path / ProjectConfiguration.CONFIGURATION_FILE_NAME
        configuration = ProjectConfiguration.from_path(root_path, configuration_path)
        return cls(configuration)

    @classmethod
    def new(cls, root_path: Path) -> Project:
        logger.info(f"Creating project '{root_path.name}'")
        project = cls(ProjectConfiguration.default(root_path))
        ProjectInitializer.initialize(project.configuration)
        return project

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    def build(self, test: bool = False) -> None:
        logger.info("Building project")
        ProjectBuilder.build_target_file(self.configuration, test)

    def run(self, test: bool = False) -> None:
        logger.info("Running project")
        result = run(self.configuration.target_file(test))
        logger.info(f"Exit code: {result.returncode}")

    def clean(self) -> None:
        logger.info("Cleaning project")
        rmtree(self.configuration.build_directory)
