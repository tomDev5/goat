from dataclasses import dataclass


@dataclass
class CommandResults:
    return_code: int
    standard_output: str
    standard_error: str

    @property
    def success(self) -> bool:
        return self.return_code == 0

    @property
    def failure(self) -> bool:
        return self.return_code != 0
