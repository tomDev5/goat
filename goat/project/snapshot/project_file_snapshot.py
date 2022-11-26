from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectFileSnapshot:
    source_file: Path
    source_file_time: float
    object_file: Path
    object_file_time: float | None
