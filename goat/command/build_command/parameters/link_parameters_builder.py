from __future__ import annotations
from pathlib import Path
from typing import Iterable
from goat.command.build_command.parameters.link_parameters import LinkParameters


class LinkParametersBuilder:
    executable: str | Path
    target_file: Path
    object_files: list[Path]
    flags: list[str]
    library_paths: list[Path]
    libraries: list[str]

    def __init__(
        self,
        executable: str | Path,
        target_file: Path,
        object_files: list[Path],
    ) -> None:
        self.executable = executable
        self.target_file = target_file
        self.object_files = object_files
        self.flags = []
        self.library_paths = []
        self.libraries = []

    def add_flag(self, flag: str) -> LinkParametersBuilder:
        self.flags.append(flag)
        return self

    def add_flags(self, flags: Iterable[str]) -> LinkParametersBuilder:
        self.flags.extend(flags)
        return self

    def add_library_path(self, library_path: Path) -> LinkParametersBuilder:
        self.library_paths.append(library_path)
        return self

    def add_library_paths(
        self,
        library_paths: Iterable[Path],
    ) -> LinkParametersBuilder:
        self.library_paths.extend(library_paths)
        return self

    def add_library(self, library: str) -> LinkParametersBuilder:
        self.libraries.append(library)
        return self

    def add_libraries(self, libraries: Iterable[str]) -> LinkParametersBuilder:
        self.libraries.extend(libraries)
        return self

    def build(self) -> LinkParameters:
        return LinkParameters(
            self.executable,
            self.target_file,
            self.object_files,
            self.flags,
            self.library_paths,
            self.libraries,
        )
