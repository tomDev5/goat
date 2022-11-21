from pathlib import Path
from goat.configuration.configuration import Configuration
from goat.project.build_mode import BuildMode
from goat.project.project_configuration_variant import ProjectConfigurationVariant


class ProjectConfigurationVariantFactory:
    @staticmethod
    def create(
        configuration: Configuration,
        build_mode: BuildMode,
    ) -> ProjectConfigurationVariant:
        match build_mode:
            case BuildMode.RELEASE:
                configuration_variant = configuration.build.release

            case BuildMode.DEBUG:
                configuration_variant = configuration.build.debug

            case BuildMode.TEST:
                configuration_variant = configuration.build.test

        target = configuration_variant.target or configuration.build.all.target
        if target is None:
            raise Exception(f"'target' is missing for {build_mode.name}")

        linker = configuration_variant.linker or configuration.build.all.linker
        if linker is None:
            raise Exception(f"'linker' is missing for {build_mode.name}")

        linker_flags = [
            *configuration.build.all.linker_flags,
            *configuration_variant.linker_flags,
        ]

        library_paths = [
            Path(string)
            for string in (
                *configuration.build.all.library_paths,
                *configuration_variant.library_paths,
            )
        ]

        libraries = [
            *configuration.build.all.libraries,
            *configuration_variant.libraries,
        ]

        compiler = configuration_variant.compiler or configuration.build.all.compiler
        if compiler is None:
            raise Exception(f"'compiler' is missing for {build_mode.name}")

        compiler_flags = [
            *configuration.build.all.compiler_flags,
            *configuration_variant.compiler_flags,
        ]

        include_paths = [
            Path(string)
            for string in (
                *configuration.build.all.include_paths,
                *configuration_variant.include_paths,
            )
        ]

        defines = [
            *configuration.build.all.defines,
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
