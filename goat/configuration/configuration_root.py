from typing import List
from pydantic import BaseModel, Field

from goat.configuration.compilation_configuration import CompilationConfiguration
from goat.configuration.packages_configuration import PackagesConfiguration


class ConfigurationRoot(BaseModel):
    compilation: CompilationConfiguration = Field(
        default_factory=CompilationConfiguration
    )
    packages: PackagesConfiguration = Field(
        default_factory=PackagesConfiguration,
    )
