from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from goat.configuration.build_configuration_values import (
    BuildConfigurationValues,
)
from goat.configuration.configuration import Configuration
from goat.project.build_mode import BuildMode


@dataclass
class ProjectConfigurationValues:
    target: str
    linker: str
    linker_flags: list[str]
    library_paths: list[Path]
    libraries: list[str]

    compiler: str
    compiler_flags: list[str]
    include_paths: list[Path]
    defines: list[str]

    @staticmethod
    def build_configuration_values(
        configuration: Configuration,
        build_mode: BuildMode,
    ) -> BuildConfigurationValues:
        match build_mode:
            case BuildMode.RELEASE:
                return configuration.build.release

            case BuildMode.DEBUG:
                return configuration.build.debug

            case BuildMode.TEST:
                return configuration.build.test

    def __init__(self, configuration: Configuration, build_mode: BuildMode) -> None:
        configuration_values = self.build_configuration_values(
            configuration, build_mode
        )

        target = configuration_values.target or configuration.build.all.target
        if target is None:
            raise Exception(f"'target' is missing for {build_mode.name}")

        linker = configuration_values.linker or configuration.build.all.linker
        if linker is None:
            raise Exception(f"'linker' is missing for {build_mode.name}")

        linker_flags = [
            *configuration.build.all.linker_flags,
            *configuration_values.linker_flags,
        ]

        library_paths = [
            Path(string)
            for string in (
                *configuration.build.all.library_paths,
                *configuration_values.library_paths,
            )
        ]

        libraries = [
            *configuration.build.all.libraries,
            *configuration_values.libraries,
        ]

        compiler = configuration_values.compiler or configuration.build.all.compiler
        if compiler is None:
            raise Exception(f"'compiler' is missing for {build_mode.name}")

        compiler_flags = [
            *configuration.build.all.compiler_flags,
            *configuration_values.compiler_flags,
        ]

        include_paths = [
            Path(string)
            for string in (
                *configuration.build.all.include_paths,
                *configuration_values.include_paths,
            )
        ]

        defines = [
            *configuration.build.all.defines,
            *configuration_values.defines,
        ]

        self.target = target
        self.linker = linker
        self.linker_flags = linker_flags
        self.library_paths = library_paths
        self.libraries = libraries

        self.compiler = compiler
        self.compiler_flags = compiler_flags
        self.include_paths = include_paths
        self.defines = defines
