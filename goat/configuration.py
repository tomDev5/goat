from typing import List
from pydantic import BaseModel, Field


class CompilationConfiguration(BaseModel):
    TARGET: str = "Application"
    CXX: str = "g++"
    CXX_FLAGS: List[str] = Field(default_factory=list)
    INCLUDES: List[str] = Field(default_factory=list)


class PackagesConfiguration(BaseModel):
    pass


class Configuration(BaseModel):
    compilation: CompilationConfiguration = Field(
        default_factory=CompilationConfiguration
    )
    packages: PackagesConfiguration = Field(
        default_factory=PackagesConfiguration,
    )
