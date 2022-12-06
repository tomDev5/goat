from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectConfigurationVariant:
    toolchain: str

    target: str
    linker: str
    linker_flags: list[str]
    library_paths: list[Path]
    libraries: list[str]

    compiler: str
    compiler_flags: list[str]
    include_paths: list[Path]
    defines: list[str]
