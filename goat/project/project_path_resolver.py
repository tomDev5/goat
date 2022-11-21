from pathlib import Path


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
    def configuration_file(this) -> Path:
        return this.root_path / this.CONFIGURATION_FILE_NAME

    @property
    def source_directory(this) -> Path:
        return this.root_path / this.SOURCE_DIRECTORY_NAME

    @property
    def include_directory(this) -> Path:
        return this.root_path / this.INCLUDE_DIRECTORY_NAME

    @property
    def test_directory(this) -> Path:
        return this.root_path / this.TEST_DIRECTORY_NAME

    @property
    def build_directory(this) -> Path:
        return this.root_path / this.BUILD_DIRECTORY_NAME

    @property
    def object_directory(this) -> Path:
        return this.build_directory / this.OBJECT_DIRECTORY_NAME

    @property
    def binary_directory(this) -> Path:
        return this.build_directory / this.BINARY_DIRECTORY_NAME
