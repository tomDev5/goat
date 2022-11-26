from pathlib import Path
from loguru import logger
from goat.command.build_command.builder.build_command_factory import (
    BuildCommandFactory,
)
from goat.command.command_runner import CommandRunner
from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration import ProjectConfiguration
from goat.project.project_path_resolver import ProjectPathResolver
from goat.command.build_command.parameters.compile_parameters_builder import (
    CompileParametersBuilder,
)
from goat.command.build_command.parameters.link_parameters_builder import (
    LinkParametersBuilder,
)


class ProjectBuilder:
    project_configuration: ProjectConfiguration

    def __init__(self, project_configuration: ProjectConfiguration) -> None:
        self.project_configuration = project_configuration

    def build_target_file(self, build_mode: BuildMode) -> None:
        object_mapping = self.get_object_mapping(build_mode)

        for source_file, object_file in object_mapping.items():
            object_file.parent.mkdir(parents=True, exist_ok=True)
            self.compile_object_file(source_file, object_file, build_mode)

        self.project_configuration.target(build_mode).parent.mkdir(
            parents=True, exist_ok=True
        )
        self.link_object_files(list(object_mapping.values()), build_mode)

    def compile_object_file(
        self,
        source_file: Path,
        object_file: Path,
        build_mode: BuildMode,
    ) -> None:
        logger.trace(
            f"Compiling {source_file.relative_to(self.path_resolver.root_path)}"
        )

        executable = self.project_configuration.compiler(build_mode)
        include_directory = self.path_resolver.include_directory
        include_paths = self.project_configuration.include_paths(build_mode)
        defines = self.project_configuration.defines(build_mode)
        flags = self.project_configuration.compiler_flags(build_mode)

        compile_parameters = (
            CompileParametersBuilder(
                executable,
                source_file,
                object_file,
            )
            .add_include_path(include_directory)
            .add_include_paths(include_paths)
            .add_defines(defines)
            .add_flags(flags)
            .build()
        )

        command = BuildCommandFactory.create_compile(executable, compile_parameters)
        command_results = CommandRunner.run(command)
        if command_results.failure:
            raise Exception(command_results.standard_error)

    def link_object_files(
        self,
        object_files: list[Path],
        build_mode: BuildMode,
    ) -> None:
        logger.trace(
            f"Linking {self.project_configuration.target(build_mode).relative_to(self.path_resolver.root_path)}"
        )

        executable = self.project_configuration.linker(build_mode)
        target_file = self.project_configuration.target(build_mode)
        library_paths = self.project_configuration.library_paths(build_mode)
        libraries = self.project_configuration.libraries(build_mode)
        flags = self.project_configuration.linker_flags(build_mode)

        link_parameters = (
            LinkParametersBuilder(
                executable,
                target_file,
                object_files,
            )
            .add_library_paths(library_paths)
            .add_libraries(libraries)
            .add_flags(flags)
            .build()
        )

        command = BuildCommandFactory.create_link(executable, link_parameters)
        command_results = CommandRunner.run(command)
        if command_results.failure:
            raise Exception(command_results.standard_error)

    def get_object_mapping(self, build_mode: BuildMode) -> dict[Path, Path]:
        object_mapping: dict[Path, Path] = {}

        for source_file in self.get_source_files(build_mode):
            relative_source_file = source_file.relative_to(self.path_resolver.root_path)
            object_file_name = f"{relative_source_file.stem}.o"
            relative_object_file = relative_source_file.parent / object_file_name
            object_file = self.path_resolver.object_directory / relative_object_file
            object_mapping[source_file] = object_file

        return object_mapping

    def get_source_files(self, build_mode: BuildMode) -> list[Path]:
        files = list(self.path_resolver.source_directory.glob("**/*.cc"))

        if build_mode == BuildMode.TEST:
            files.extend(self.path_resolver.test_directory.glob("**/*.cc"))

        return files

    @property
    def path_resolver(self) -> ProjectPathResolver:
        return self.project_configuration.path_resolver
