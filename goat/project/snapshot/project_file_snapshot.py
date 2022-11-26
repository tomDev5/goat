from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectFileSnapshot:
    source_file: Path
    object_file: Path
