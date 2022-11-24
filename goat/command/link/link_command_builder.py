from pathlib import Path
from typing import Iterable, TypeVar
from goat.command.command_builder import CommandBuilder

T = TypeVar("T", bound="LinkCommandBuilder")


class LinkCommandBuilder(CommandBuilder):
    target_file: Path
    object_files: list[Path]
    flags: list[str]
    library_paths: list[Path]
    libraries: list[str]

    def __init__(self, program: str | Path, target_file: Path) -> None:
        super().__init__(program)
        self.target_file = target_file
        self.object_files = []
        self.flags = []
        self.library_paths = []
        self.libraries = []

    def add_object_file(self: T, object_file: Path) -> T:
        self.object_files.append(object_file)
        return self

    def add_object_files(self: T, object_files: Iterable[Path]) -> T:
        self.object_files.extend(object_files)
        return self

    def add_flag(self: T, flag: str) -> T:
        self.flags.append(flag)
        return self

    def add_flags(self: T, flags: Iterable[str]) -> T:
        self.flags.extend(flags)
        return self

    def add_library_path(self: T, library_path: Path) -> T:
        self.library_paths.append(library_path)
        return self

    def add_library_paths(self: T, library_paths: Iterable[Path]) -> T:
        self.library_paths.extend(library_paths)
        return self

    def add_library(self: T, library: str) -> T:
        self.libraries.append(library)
        return self

    def add_libraries(self: T, libraries: Iterable[str]) -> T:
        self.libraries.extend(libraries)
        return self
