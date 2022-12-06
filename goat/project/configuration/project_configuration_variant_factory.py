from pathlib import Path
from goat.project.configuration.schema.configuration_schema import ConfigurationSchema
from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration_variant import (
    ProjectConfigurationVariant,
)


class ProjectConfigurationVariantFactory:
    @staticmethod
    def create(
        configuration_schema: ConfigurationSchema,
        build_mode: BuildMode,
    ) -> ProjectConfigurationVariant:
        match build_mode:
            case BuildMode.RELEASE:
                configuration_variant = configuration_schema.build.release

            case BuildMode.DEBUG:
                configuration_variant = configuration_schema.build.debug

            case BuildMode.TEST:
                configuration_variant = configuration_schema.build.test

        toolchain = (
            configuration_variant.toolchain or configuration_schema.build.all.toolchain
        )
        if toolchain is None:
            raise Exception(f"'toolchain' is missing for {build_mode.name}")

        target = configuration_variant.target or configuration_schema.build.all.target
        if target is None:
            raise Exception(f"'target' is missing for {build_mode.name}")

        linker = (
            configuration_variant.linker
            or configuration_schema.build.all.linker
            or toolchain
        )

        linker_flags = [
            *configuration_schema.build.all.linker_flags,
            *configuration_variant.linker_flags,
        ]

        library_paths = [
            Path(string)
            for string in (
                *configuration_schema.build.all.library_paths,
                *configuration_variant.library_paths,
            )
        ]

        libraries = [
            *configuration_schema.build.all.libraries,
            *configuration_variant.libraries,
        ]

        compiler = (
            configuration_variant.compiler
            or configuration_schema.build.all.compiler
            or toolchain
        )

        compiler_flags = [
            *configuration_schema.build.all.compiler_flags,
            *configuration_variant.compiler_flags,
        ]

        include_paths = [
            Path(string)
            for string in (
                *configuration_schema.build.all.include_paths,
                *configuration_variant.include_paths,
            )
        ]

        defines = [
            *configuration_schema.build.all.defines,
            *configuration_variant.defines,
        ]

        return ProjectConfigurationVariant(
            toolchain,
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
