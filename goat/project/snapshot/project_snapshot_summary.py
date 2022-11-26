from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectSummary:
    updated_files: list[tuple[Path, Path]]
    outdated_files: list[tuple[Path, Path]]
    target_file_outdated: bool

    @property
    def target_file_updated(self) -> bool:
        return not self.target_file_outdated
