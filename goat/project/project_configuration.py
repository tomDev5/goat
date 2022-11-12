from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from goat.configuration.configuration_root import ConfigurationRoot
from toml import loads as toml_to_dict


@dataclass
class ProjectConfiguration:
    root_path: Path
    binary: str
    compiler: str
    compiler_flags: list[str]
    include_paths: list[Path]

    CONFIGURATION_FILE_NAME = "goat.toml"
    SOURCE_DIRECTORY_NAME = "source"
    INCLUDE_DIRECTORY_NAME = "include"
    TEST_DIRECTORY_NAME = "test"
    BUILD_DIRECTORY_NAME = "build"
    OBJECT_DIRECTORY_NAME = "object"
    BINARY_DIRECTORY_NAME = "binary"

    @classmethod
    def default(self, root_path: Path) -> ProjectConfiguration:
        return ProjectConfiguration.from_configuration(root_path, ConfigurationRoot())

    @classmethod
    def from_configuration(
        cls, root_path: Path, configuration: ConfigurationRoot
    ) -> ProjectConfiguration:
        return cls(
            root_path,
            configuration.compilation.TARGET,
            configuration.compilation.CXX,
            configuration.compilation.CXX_FLAGS,
            [Path(include_path) for include_path in configuration.compilation.INCLUDES],
        )

    @classmethod
    def from_path(
        cls, root_path: Path, configuration_path: Path
    ) -> ProjectConfiguration:
        return cls.from_configuration(
            root_path,
            ConfigurationRoot.parse_obj(toml_to_dict(configuration_path.read_text())),
        )

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
