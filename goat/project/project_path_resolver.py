from pathlib import Path

from goat.project.build_mode import BuildMode


class ProjectPathResolver:
    root_path: Path

    CONFIGURATION_FILE_NAME = "goat.toml"
    SOURCE_DIRECTORY_NAME = "source"
    INCLUDE_DIRECTORY_NAME = "include"
    TEST_DIRECTORY_NAME = "test"
    BUILD_DIRECTORY_NAME = "build"
    OBJECT_DIRECTORY_NAME = "object"
    BINARY_DIRECTORY_NAME = "binary"

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

    @property
    def configuration_file(self) -> Path:
        return self.root_path / self.CONFIGURATION_FILE_NAME

    @property
    def source_directory(self) -> Path:
        return self.root_path / self.SOURCE_DIRECTORY_NAME

    @property
    def include_directory(self) -> Path:
        return self.root_path / self.INCLUDE_DIRECTORY_NAME

    @property
    def test_directory(self) -> Path:
        return self.root_path / self.TEST_DIRECTORY_NAME

    @property
    def build_directory(self) -> Path:
        return self.root_path / self.BUILD_DIRECTORY_NAME

    def build_mode_directory(self, build_mode: BuildMode) -> Path:
        return self.build_directory / build_mode.value

    def object_directory(self, build_mode: BuildMode) -> Path:
        return self.build_mode_directory(build_mode) / self.OBJECT_DIRECTORY_NAME

    def binary_directory(self, build_mode: BuildMode) -> Path:
        return self.build_mode_directory(build_mode) / self.BINARY_DIRECTORY_NAME

    def object_file(self, source_file: Path, build_mode: BuildMode) -> Path:
        relative_source_file = source_file.relative_to(self.root_path)
        object_file_name = f"{relative_source_file.name}.o"
        relative_object_file = relative_source_file.parent / object_file_name
        return self.object_directory(build_mode) / relative_object_file
