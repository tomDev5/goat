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
    CONAN_DIRECTORY_NAME = ".conan"

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

    @property
    def object_directory(self) -> Path:
        return self.build_directory / self.OBJECT_DIRECTORY_NAME

    @property
    def binary_directory(self) -> Path:
        return self.build_directory / self.BINARY_DIRECTORY_NAME

    @property
    def conan_directory(self) -> Path:
        return self.build_directory / self.CONAN_DIRECTORY_NAME
