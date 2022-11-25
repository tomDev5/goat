from pathlib import Path
from goat.project.configuration.raw.raw_configuration import RawConfiguration
from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration_variant import (
    ProjectConfigurationVariant,
)


class ProjectConfigurationVariantFactory:
    @staticmethod
    def create(
        raw_configuration: RawConfiguration,
        build_mode: BuildMode,
    ) -> ProjectConfigurationVariant:
        match build_mode:
            case BuildMode.RELEASE:
                configuration_variant = raw_configuration.build.release

            case BuildMode.DEBUG:
                configuration_variant = raw_configuration.build.debug

            case BuildMode.TEST:
                configuration_variant = raw_configuration.build.test

        target = configuration_variant.target or raw_configuration.build.all.target
        if target is None:
            raise Exception(f"'target' is missing for {build_mode.name}")

        linker = configuration_variant.linker or raw_configuration.build.all.linker
        if linker is None:
            raise Exception(f"'linker' is missing for {build_mode.name}")

        linker_flags = [
            *raw_configuration.build.all.linker_flags,
            *configuration_variant.linker_flags,
        ]

        library_paths = [
            Path(string)
            for string in (
                *raw_configuration.build.all.library_paths,
                *configuration_variant.library_paths,
            )
        ]

        libraries = [
            *raw_configuration.build.all.libraries,
            *configuration_variant.libraries,
        ]

        compiler = (
            configuration_variant.compiler or raw_configuration.build.all.compiler
        )
        if compiler is None:
            raise Exception(f"'compiler' is missing for {build_mode.name}")

        compiler_flags = [
            *raw_configuration.build.all.compiler_flags,
            *configuration_variant.compiler_flags,
        ]

        include_paths = [
            Path(string)
            for string in (
                *raw_configuration.build.all.include_paths,
                *configuration_variant.include_paths,
            )
        ]

        defines = [
            *raw_configuration.build.all.defines,
            *configuration_variant.defines,
        ]

        return ProjectConfigurationVariant(
            target,
            linker,
            linker_flags,
            library_paths,
            libraries,
            compiler,
            compiler_flags,
            include_paths,
            defines,
        )
