from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
from goat.project.snapshot.project_file_snapshot import ProjectFileSnapshot


@dataclass
class ProjectSnapshot:
    file_snapshots: list[ProjectFileSnapshot]
    target_file_modified: float | None

    @property
    def source_files(self) -> list[Path]:
        return [file_snapshot.source_file for file_snapshot in self.file_snapshots]

    @property
    def object_files(self) -> list[Path]:
        return [file_snapshot.object_file for file_snapshot in self.file_snapshots]

    @property
    def target_updated(self) -> bool:
        if self.target_file_modified is None:
            return False

        return all(
            file_snapshot.object_file_modified is not None
            and file_snapshot.object_file_modified < self.target_file_modified
            for file_snapshot in self.file_snapshots
        )

    @property
    def target_outdated(self) -> bool:
        return not self.target_updated
