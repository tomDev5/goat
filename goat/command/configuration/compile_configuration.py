from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CompileConfiguration:
    executable: str | Path
    source_file: Path
    object_file: Path
    include_paths: list[Path] = field(default_factory=list)
    defines: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
