from pathlib import Path
from goat.configuration.configuration import Configuration
from goat.project.build_mode import BuildMode
from goat.project.project_configuration_entry import ProjectConfigurationEntry


class ProjectConfigurationEntryFactory:
    @staticmethod
    def create(
        configuration: Configuration,
        build_mode: BuildMode,
    ) -> ProjectConfigurationEntry:
        match build_mode:
            case BuildMode.RELEASE:
                configuration_entry = configuration.build.release

            case BuildMode.DEBUG:
                configuration_entry = configuration.build.debug

            case BuildMode.TEST:
                configuration_entry = configuration.build.test

        target = configuration_entry.target or configuration.build.all.target
        if target is None:
            raise Exception(f"'target' is missing for {build_mode.name}")

        linker = configuration_entry.linker or configuration.build.all.linker
        if linker is None:
            raise Exception(f"'linker' is missing for {build_mode.name}")

        linker_flags = [
            *configuration.build.all.linker_flags,
            *configuration_entry.linker_flags,
        ]

        library_paths = [
            Path(string)
            for string in (
                *configuration.build.all.library_paths,
                *configuration_entry.library_paths,
            )
        ]

        libraries = [
            *configuration.build.all.libraries,
            *configuration_entry.libraries,
        ]

        compiler = configuration_entry.compiler or configuration.build.all.compiler
        if compiler is None:
            raise Exception(f"'compiler' is missing for {build_mode.name}")

        compiler_flags = [
            *configuration.build.all.compiler_flags,
            *configuration_entry.compiler_flags,
        ]

        include_paths = [
            Path(string)
            for string in (
                *configuration.build.all.include_paths,
                *configuration_entry.include_paths,
            )
        ]

        defines = [
            *configuration.build.all.defines,
            *configuration_entry.defines,
        ]

        return ProjectConfigurationEntry(
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
