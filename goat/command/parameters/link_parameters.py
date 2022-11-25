from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LinkParameters:
    executable: str | Path
    target_file: Path
    object_files: list[Path]
    flags: list[str] = field(default_factory=list)
    library_paths: list[Path] = field(default_factory=list)
    libraries: list[str] = field(default_factory=list)
