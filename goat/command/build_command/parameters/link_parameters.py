from dataclasses import dataclass
from pathlib import Path


@dataclass
class LinkParameters:
    executable: str | Path
    target_file: Path
    object_files: list[Path]
    flags: list[str]
    library_paths: list[Path]
    libraries: list[str]
