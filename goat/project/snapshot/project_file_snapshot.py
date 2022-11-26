from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectFileSnapshot:
    source_file: Path
    source_file_modified: float
    object_file: Path
    object_file_modified: float | None

    @property
    def updated(self) -> bool:
        if self.object_file_modified is None:
            return False

        return self.source_file_modified < self.object_file_modified

    @property
    def outdated(self) -> bool:
        return not self.updated
