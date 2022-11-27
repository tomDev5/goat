from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from pathlib import Path
from goat.project.changes.file_timestamps import FileTimestamps


@dataclass
class ProjectTimestamps:
    files_timestamps: dict[Path, FileTimestamps]
    target_file_time: datetime | None
    latest_include_file_time: datetime | None

    @cached_property
    def latest_object_file_time(self) -> datetime | None:
        return max(
            (
                project_timestamps.object_file_time
                for project_timestamps in self.files_timestamps.values()
                if project_timestamps.object_file_time is not None
            ),
            default=None,
        )
