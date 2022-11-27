from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectChanges:
    changed_files: list[Path]
    unchanged_files: list[Path]
    target_file_changed: bool

    @property
    def target_file_unchanged(self) -> bool:
        return not self.target_file_changed
