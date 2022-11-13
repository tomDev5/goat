from pydantic import BaseModel, Field


class CompilationConfiguration(BaseModel):
    TARGET: str = "Application"
    CXX: str = "g++"
    CXX_FLAGS: list[str] = Field(default_factory=list)
    INCLUDES: list[str] = Field(default_factory=list)
