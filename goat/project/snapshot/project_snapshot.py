from dataclasses import dataclass
from goat.project.snapshot.project_snapshot_entry import ProjectSnapshotEntry


@dataclass
class ProjectSnapshot:
    file_snapshots: list[ProjectSnapshotEntry]
    target_file_time: float | None
    latest_object_file_time: float | None
    latest_include_file_time: float | None
