from pydantic import BaseModel
from goat.configuration.compilation_configuration import CompilationConfiguration
from goat.configuration.linkage_configuration import LinkageConfiguration
from goat.configuration.packages_configuration import PackagesConfiguration


class Configuration(BaseModel):
    compilation: CompilationConfiguration
    linkage: LinkageConfiguration
    packages: PackagesConfiguration
