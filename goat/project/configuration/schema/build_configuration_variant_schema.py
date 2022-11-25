from pydantic import BaseModel, Field


class BuildConfigurationVariantSchema(BaseModel):
    target: str | None = None
    linker: str | None = None
    linker_flags: list[str] = Field(default_factory=list)
    library_paths: list[str] = Field(default_factory=list)
    libraries: list[str] = Field(default_factory=list)

    compiler: str | None = None
    compiler_flags: list[str] = Field(default_factory=list)
    include_paths: list[str] = Field(default_factory=list)
    defines: list[str] = Field(default_factory=list)
