from __future__ import annotations
from enum import Enum
from shutil import rmtree
from typing import List
from pathlib import Path
from goat.configuration import Configuration
from toml import loads as toml_to_dict, dumps as dict_to_toml
from subprocess import CompletedProcess, run


TEMPLATE_DIRECTORY = Path(__file__).parent / "templates"


class Template(Enum):
    MAIN = "main"
    TEST = "test"

    def read(self) -> str:
        return (TEMPLATE_DIRECTORY / f"{self.value}.template").read_text()


class Project:
    root_path: Path
    target: str
    compiler: str
    compiler_flags: List[str]
    include_paths: List[Path]

    CONFIGURATION_FILE_NAME = "goat.toml"
    SOURCE_DIRECTORY_NAME = "source"
    INCLUDE_DIRECTORY_NAME = "include"
    TEST_DIRECTORY_NAME = "test"
    BUILD_DIRECTORY_NAME = "build"
    OBJECT_DIRECTORY_NAME = "object"
    BINARY_DIRECTORY_NAME = "binary"

    TEMPLATE_MAIN_FILE_NAME = "main.cc"
    TEMPLATE_TEST_FILE_NAME = "test.cc"

    @classmethod
    def from_path(cls, path: Path) -> Project:
        content = (path / cls.CONFIGURATION_FILE_NAME).read_text()
        return cls.from_configuration(
            path,
            Configuration.parse_obj(toml_to_dict(content)),
        )

    @classmethod
    def from_default_configuration(cls, path: Path) -> Project:
        return cls.from_configuration(path, Configuration())

    @classmethod
    def from_configuration(cls, path: Path, configuration: Configuration) -> Project:
        return cls(
            path,
            configuration.compilation.TARGET,
            configuration.compilation.CXX,
            configuration.compilation.CXX_FLAGS,
            [Path(include_path) for include_path in configuration.compilation.INCLUDES],
        )

    def __init__(
        self,
        root_path: Path,
        target: str,
        compiler: str,
        compiler_flags: List[str],
        include_paths: List[Path],
    ) -> None:
        self.root_path = root_path
        self.target = target
        self.compiler = compiler
        self.compiler_flags = compiler_flags
        self.include_paths = include_paths

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

    def to_configuration(self) -> Configuration:
        return Configuration(
            TARGET=self.target,
            CXX=self.compiler,
            CXX_FLAGS=self.compiler_flags,
            INCLUDES=[str(path) for path in self.include_paths],
        )

    def initialize(self) -> None:
        assert not self.root_path.exists(), "Project root directory already exists"

        self.root_path.mkdir()
        self.source_directory.mkdir()
        self.include_directory.mkdir()
        self.test_directory.mkdir()

        template_main_path = self.source_directory / self.TEMPLATE_MAIN_FILE_NAME
        template_test_path = self.test_directory / self.TEMPLATE_TEST_FILE_NAME

        self.configuration_file.write_text(dict_to_toml(self.to_configuration().dict()))
        template_main_path.write_text(Template.MAIN.read())
        template_test_path.write_text(Template.TEST.read())

    def build_object_file(
        self,
        source_file: Path,
        object_file: Path,
    ) -> CompletedProcess:
        include_flags = [
            f"-I{include_path}"
            for include_path in (self.include_paths + [self.include_directory])
        ]
        compiler_flags = self.compiler_flags + ["-c", "-o", str(object_file)]

        return run([self.compiler, *include_flags, *compiler_flags, str(source_file)])

    def build(self) -> None:
        self.build_directory.mkdir(exist_ok=True)

        # Collect source and object files

        source_object_mapping = {}
        for source_file in self.source_directory.glob("**/*.cc"):
            relative_source_file = source_file.relative_to(self.source_directory)
            object_file = (
                self.object_directory
                / relative_source_file.parent
                / f"{relative_source_file.name}.o"
            )

            source_object_mapping[source_file] = object_file

        # Build object files

        self.object_directory.mkdir(exist_ok=True)
        for source_file, object_file in source_object_mapping.items():
            relative_source_file = source_file.relative_to(self.source_directory)
            print(f"Compiling {relative_source_file}...")

            result = self.build_object_file(source_file, object_file)
            if result.returncode != 0:
                print(result.stderr)
                return

        # Build binary

        self.binary_directory.mkdir(exist_ok=True)

        print(f"Building {self.target}...")

        linker_flags = ["-o", str(self.binary_directory / self.target)]
        object_files = [
            str(object_file) for object_file in source_object_mapping.values()
        ]

        result = run([self.compiler, *linker_flags, *object_files])
        if result.returncode != 0:
            print(result.stderr)
            return
