from pathlib import Path
from subprocess import PIPE, run
from loguru import logger
from goat.project.build_mode import BuildMode
from goat.project.project_configuration import ProjectConfiguration
from goat.project.project_path_resolver import ProjectPathResolver


class ProjectBuilder:
    configuration: ProjectConfiguration

    def __init__(self, configuration: ProjectConfiguration) -> None:
        self.configuration = configuration

    def build_target_file(self, build_mode: BuildMode) -> None:
        object_mapping = self.get_object_mapping(build_mode)

        for source_file, object_file in object_mapping.items():
            object_file.parent.mkdir(parents=True, exist_ok=True)
            self.compile_object_file(source_file, object_file, build_mode)

        self.configuration.target(build_mode).parent.mkdir(parents=True, exist_ok=True)
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

        include_paths = [
            f"-I{include_path}"
            for include_path in (
                self.configuration.include_paths(build_mode)
                + [self.path_resolver.include_directory]
            )
        ]

        compiler_flags = (
            self.configuration.compiler_flags(build_mode)
            + [f"-D{define}" for define in self.configuration.defines(build_mode)]
            + [
                "-c",
                "-o",
                str(object_file),
            ]
        )

        result = run(
            [
                self.configuration.compiler(build_mode),
                source_file,
                *include_paths,
                *compiler_flags,
            ],
            stderr=PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

    def link_object_files(
        self,
        object_files: list[Path],
        build_mode: BuildMode,
    ) -> None:
        logger.trace(
            f"Linking {self.configuration.target(build_mode).relative_to(self.path_resolver.root_path)}"
        )

        library_paths = self.configuration.library_paths(build_mode)

        linker_flags = (
            self.configuration.linker_flags(build_mode)
            + [f"-l{library}" for library in self.configuration.libraries(build_mode)]
            + [
                "-o",
                str(self.configuration.target(build_mode)),
            ]
        )

        result = run(
            [
                self.configuration.linker(build_mode),
                *object_files,
                *library_paths,
                *linker_flags,
            ],
            stderr=PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

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
        return self.configuration.path_resolver
