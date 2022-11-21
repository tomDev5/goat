from pydantic import BaseModel, Field


class CompilationConfigurationValues(BaseModel):
    compiler: str | None = None
    compiler_flags: list[str] = Field(default_factory=list)
    include_paths: list[str] = Field(default_factory=list)
    defines: list[str] = Field(default_factory=list)
