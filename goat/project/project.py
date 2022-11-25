from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from subprocess import run
from goat.project.build_mode import BuildMode
from goat.project.project_builder import ProjectBuilder
from goat.project.configuration.project_configuration import ProjectConfiguration
from goat.project.project_initializer import ProjectInitializer
from loguru import logger

from goat.project.project_path_resolver import ProjectPathResolver


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
        path_resolver = ProjectPathResolver(root_path)
        ProjectInitializer.initialize(path_resolver)
        return cls.from_path(root_path)

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    def build(self, build_mode: BuildMode) -> None:
        logger.info(f"Building project (mode: {build_mode})")
        project_builder = ProjectBuilder(self.configuration)
        project_builder.build_target_file(build_mode)

    def run(self, build_mode: BuildMode) -> None:
        logger.info("Running project")
        result = run(self.configuration.target(build_mode))
        logger.info(f"Exit code: {result.returncode}")

    def clean(self) -> None:
        logger.info("Cleaning project")
        rmtree(self.path_resolver.build_directory)

    @property
    def path_resolver(self) -> ProjectPathResolver:
        return self.configuration.path_resolver
