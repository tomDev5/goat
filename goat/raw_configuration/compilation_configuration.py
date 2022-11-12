from typing import List
from pydantic import BaseModel, Field


class CompilationConfiguration(BaseModel):
    TARGET: str = "Application"
    CXX: str = "g++"
    CXX_FLAGS: List[str] = Field(default_factory=list)
    INCLUDES: List[str] = Field(default_factory=list)
