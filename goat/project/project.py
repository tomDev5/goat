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
    project_configuration: ProjectConfiguration

    @classmethod
    def from_path(cls, root_path: Path) -> Project:
        logger.info(f"Loading project '{root_path.name}'")
        configuration_path = root_path / ProjectConfiguration.CONFIGURATION_FILE_NAME
        
        if not configuration_path.is_file():
            raise FileNotFoundError(f"Cannot find `{ProjectConfiguration.CONFIGURATION_FILE_NAME}` in `{root_path.absolute()}`")

        project_configuration = ProjectConfiguration.from_path(
            root_path, configuration_path
        )
        return cls(project_configuration)

    @classmethod
    def new(cls, root_path: Path) -> Project:
        logger.info(f"Creating project '{root_path.name}'")
        path_resolver = ProjectPathResolver(root_path)
        ProjectInitializer.initialize(path_resolver)
        return cls.from_path(root_path)

    def __init__(self, project_configuration: ProjectConfiguration) -> None:
        self.project_configuration = project_configuration

    def build(self, build_mode: BuildMode) -> None:
        logger.info(f"Building project (mode: {build_mode})")
        project_builder = ProjectBuilder(self.project_configuration)
        project_builder.build_target_file(build_mode)

    def run(self, build_mode: BuildMode) -> None:
        logger.info("Running project")
        result = run(self.project_configuration.target(build_mode))
        logger.info(f"Exit code: {result.returncode}")

    def clean(self) -> None:
        logger.info("Cleaning project")
        rmtree(self.path_resolver.build_directory)

    @property
    def path_resolver(self) -> ProjectPathResolver:
        return self.project_configuration.path_resolver
