from __future__ import annotations
from pathlib import Path
from typing import Iterable
from goat.command.configuration.link_configuration import LinkConfiguration


class LinkConfigurationBuilder:
    link_configuration: LinkConfiguration

    def __init__(
        self,
        executable: str | Path,
        target_file: Path,
        object_files: list[Path],
    ) -> None:
        self.link_configuration = LinkConfiguration(
            executable,
            target_file,
            object_files,
        )

    def add_flag(self, flag: str):
        self.link_configuration.flags.append(flag)
        return self

    def add_flags(self, flags: Iterable[str]):
        self.link_configuration.flags.extend(flags)
        return self

    def add_library_path(self, library_path: Path):
        self.link_configuration.library_paths.append(library_path)
        return self

    def add_library_paths(self, library_paths: Iterable[Path]):
        self.link_configuration.library_paths.extend(library_paths)
        return self

    def add_library(self, library: str):
        self.link_configuration.libraries.append(library)
        return self

    def add_libraries(self, libraries: Iterable[str]):
        self.link_configuration.libraries.extend(libraries)
        return self

    def build(self) -> LinkConfiguration:
        return self.link_configuration
