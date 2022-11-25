from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CompileParameters:
    executable: str | Path
    source_file: Path
    object_file: Path
    include_paths: list[Path]
    defines: list[str]
    flags: list[str]
