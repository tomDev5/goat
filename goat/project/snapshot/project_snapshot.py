from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
from goat.project.snapshot.project_file_snapshot import ProjectFileSnapshot


@dataclass
class ProjectSnapshot:
    file_snapshots: list[ProjectFileSnapshot]
    target_file_time: float | None
    latest_object_file_time: float | None
    latest_include_file_time: float | None
