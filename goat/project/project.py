from __future__ import annotations
from pathlib import Path
from goat.project.project_configuration import ProjectConfiguration
from subprocess import CompletedProcess, run
from goat.project.project_initializer import ProjectInitializer
from goat.templates.template import Template


class Project:
    project_configuration: ProjectConfiguration

    @classmethod
    def load(cls, root_path: Path) -> Project:
        configuration_path = root_path / ProjectConfiguration.CONFIGURATION_FILE_NAME
        project_configuration = ProjectConfiguration.from_path(
            root_path,
            configuration_path,
        )

        return cls(project_configuration)

    @classmethod
    def new(cls, root_path: Path) -> Project:
        project = cls(ProjectConfiguration.default(root_path))
        ProjectInitializer.initialize(project.project_configuration)
        return project

    def __init__(self, project_configuration: ProjectConfiguration) -> None:
        self.project_configuration = project_configuration

    def build_object_file(
        self,
        source_file: Path,
        object_file: Path,
    ) -> CompletedProcess:
        include_flags = [
            f"-I{include_path}"
            for include_path in (
                self.project_configuration.include_paths
                + [self.project_configuration.include_directory]
            )
        ]

        compiler_flags = self.project_configuration.compiler_flags + [
            "-c",
            "-o",
            str(object_file),
        ]

        return run(
            [
                self.project_configuration.compiler,
                *include_flags,
                *compiler_flags,
                str(source_file),
            ]
        )

    def build(self) -> None:
        self.project_configuration.build_directory.mkdir(exist_ok=True)

        # Collect source and object files

        source_object_mapping = {}
        for source_file in self.project_configuration.source_directory.glob("**/*.cc"):
            relative_source_file = source_file.relative_to(
                self.project_configuration.source_directory
            )

            object_file = (
                self.project_configuration.object_directory
                / relative_source_file.parent
                / f"{relative_source_file.name}.o"
            )

            source_object_mapping[source_file] = object_file

        # Build object files

        self.project_configuration.object_directory.mkdir(exist_ok=True)
        for source_file, object_file in source_object_mapping.items():
            relative_source_file = source_file.relative_to(
                self.project_configuration.source_directory
            )
            print(f"Compiling {relative_source_file}...")

            result = self.build_object_file(source_file, object_file)
            if result.returncode != 0:
                print(result.stderr)
                return

        # Build binary

        self.project_configuration.binary_directory.mkdir(exist_ok=True)

        print(f"Building {self.project_configuration.target}...")

        target_path = (
            self.project_configuration.binary_directory
            / self.project_configuration.target
        )
        linker_flags = ["-o", str(target_path)]
        object_files = [
            str(object_file) for object_file in source_object_mapping.values()
        ]

        result = run(
            [self.project_configuration.compiler, *linker_flags, *object_files]
        )
        if result.returncode != 0:
            print(result.stderr)
            return
