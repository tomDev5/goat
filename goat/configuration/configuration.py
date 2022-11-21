from pydantic import BaseModel
from goat.configuration.build_configuration import BuildConfiguration
from goat.configuration.packages_configuration import PackagesConfiguration


class Configuration(BaseModel):
    build: BuildConfiguration
    packages: PackagesConfiguration
