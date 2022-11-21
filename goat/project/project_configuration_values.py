from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from goat.configuration.compilation_configuration_values import (
    CompilationConfigurationValues,
)
from goat.configuration.configuration import Configuration
from goat.configuration.linkage_configuration_values import LinkageConfigurationValues
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
    def compilation_configuration_values(
        configuration: Configuration,
        build_mode: BuildMode,
    ) -> CompilationConfigurationValues:
        match build_mode:
            case BuildMode.RELEASE:
                return configuration.compilation.release

            case BuildMode.DEBUG:
                return configuration.compilation.debug

            case BuildMode.TEST:
                return configuration.compilation.test

    @staticmethod
    def linkage_configuration_values(
        configuration: Configuration,
        build_mode: BuildMode,
    ) -> LinkageConfigurationValues:
        match build_mode:
            case BuildMode.RELEASE:
                return configuration.linkage.release

            case BuildMode.DEBUG:
                return configuration.linkage.debug

            case BuildMode.TEST:
                return configuration.linkage.test

    def __init__(self, configuration: Configuration, build_mode: BuildMode) -> None:
        linkage_values = self.linkage_configuration_values(configuration, build_mode)
        compilation_values = self.compilation_configuration_values(
            configuration, build_mode
        )

        target = linkage_values.target or configuration.linkage.target
        if target is None:
            raise Exception(f"'target' is missing for {build_mode.name}")

        linker = linkage_values.linker or configuration.linkage.linker
        if linker is None:
            raise Exception(f"'linker' is missing for {build_mode.name}")

        linker_flags = [
            *configuration.linkage.linker_flags,
            *linkage_values.linker_flags,
        ]

        library_paths = [
            Path(string)
            for string in (
                *configuration.linkage.library_paths,
                *linkage_values.library_paths,
            )
        ]

        libraries = [
            *configuration.linkage.libraries,
            *linkage_values.libraries,
        ]

        compiler = compilation_values.compiler or configuration.compilation.compiler
        if compiler is None:
            raise Exception(f"'compiler' is missing for {build_mode.name}")

        compiler_flags = [
            *configuration.compilation.compiler_flags,
            *compilation_values.compiler_flags,
        ]

        include_paths = [
            Path(string)
            for string in (
                *configuration.compilation.include_paths,
                *compilation_values.include_paths,
            )
        ]

        defines = [
            *configuration.compilation.defines,
            *compilation_values.defines,
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
