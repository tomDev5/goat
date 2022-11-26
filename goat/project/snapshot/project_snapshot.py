from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
from goat.project.snapshot.project_file_snapshot import ProjectFileSnapshot


@dataclass
class ProjectSnapshot:
    outdated_file_snapshots: list[ProjectFileSnapshot]
    updated_file_snapshots: list[ProjectFileSnapshot]
    target_file_updated: bool

    @property
    def target_file_outdated(self) -> bool:
        return not self.target_file_updated

    @property
    def file_snapshots(self) -> list[ProjectFileSnapshot]:
        return self.outdated_file_snapshots + self.updated_file_snapshots

    @property
    def object_files(self) -> Iterator[Path]:
        for file_snapshot in self.file_snapshots:
            yield file_snapshot.object_file
