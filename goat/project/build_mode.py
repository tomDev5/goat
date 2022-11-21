from enum import Enum


class BuildMode(Enum):
    RELEASE = "release"
    DEBUG = "debug"
    TEST = "test"

    def __str__(self) -> str:
        return self.value
