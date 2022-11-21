from pydantic import BaseModel, Field


class LinkageConfigurationValues(BaseModel):
    target: str | None = None
    linker: str | None = None
    linker_flags: list[str] = Field(default_factory=list)
    library_paths: list[str] = Field(default_factory=list)
    libraries: list[str] = Field(default_factory=list)
