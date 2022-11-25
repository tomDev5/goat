from __future__ import annotations
from pathlib import Path
from typing import Iterable
from goat.command.parameters.link_parameters import LinkParameters


class LinkParametersBuilder:
    link_parameters: LinkParameters

    def __init__(
        self,
        executable: str | Path,
        target_file: Path,
        object_files: list[Path],
    ) -> None:
        self.link_parameters = LinkParameters(
            executable,
            target_file,
            object_files,
        )

    def add_flag(self, flag: str) -> LinkParametersBuilder:
        self.link_parameters.flags.append(flag)
        return self

    def add_flags(self, flags: Iterable[str]) -> LinkParametersBuilder:
        self.link_parameters.flags.extend(flags)
        return self

    def add_library_path(self, library_path: Path) -> LinkParametersBuilder:
        self.link_parameters.library_paths.append(library_path)
        return self

    def add_library_paths(
        self,
        library_paths: Iterable[Path],
    ) -> LinkParametersBuilder:
        self.link_parameters.library_paths.extend(library_paths)
        return self

    def add_library(self, library: str) -> LinkParametersBuilder:
        self.link_parameters.libraries.append(library)
        return self

    def add_libraries(self, libraries: Iterable[str]) -> LinkParametersBuilder:
        self.link_parameters.libraries.extend(libraries)
        return self

    def build(self) -> LinkParameters:
        return self.link_parameters
