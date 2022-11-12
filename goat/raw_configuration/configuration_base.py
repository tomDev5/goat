from typing import List
from pydantic import BaseModel, Field

from goat.raw_configuration.compilation_configuration import CompilationConfiguration
from goat.raw_configuration.packages_configuration import PackagesConfiguration


class ConfigurationRoot(BaseModel):
    compilation: CompilationConfiguration = Field(
        default_factory=CompilationConfiguration
    )
    packages: PackagesConfiguration = Field(
        default_factory=PackagesConfiguration,
    )
