from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileTimestamps:
    source_file_time: datetime
    object_file_time: datetime | None
