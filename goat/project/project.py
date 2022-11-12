from __future__ import annotations
from pathlib import Path
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

    def get_source_object_mapping(self) -> dict[Path, Path]:
        source_object_mapping: dict[Path, Path] = {}
        for source_file in self.configuration.source_directory.glob("**/*.cc"):
            relative_source_file = source_file.relative_to(
                self.configuration.source_directory
            )

            object_file = (
                self.configuration.object_directory
                / relative_source_file.parent
                / f"{relative_source_file.name}.o"
            )

            source_object_mapping[source_file] = object_file

        return source_object_mapping

    def build(self) -> None:
        self.configuration.build_directory.mkdir(exist_ok=True)
        self.configuration.object_directory.mkdir(exist_ok=True)
        self.configuration.binary_directory.mkdir(exist_ok=True)

        source_object_mapping = self.get_source_object_mapping()

        for source_file, object_file in source_object_mapping.items():
            print(f"Compiling {source_file}...")
            result = ProjectBuilder.compile_object_file(
                self.configuration,
                source_file,
                object_file,
            )

            if result.returncode != 0:
                print(result.stderr)
                return

        binary_file = self.configuration.binary_directory / self.configuration.binary
        print(f"Linking {binary_file}...")

        result = ProjectBuilder.link_binary_file(
            self.configuration,
            list(source_object_mapping.values()),
            binary_file,
        )

        if result.returncode != 0:
            print(result.stderr)
            return
