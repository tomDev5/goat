from pydantic import BaseModel
from goat.project.configuration.raw.build_configuration import BuildConfiguration
from goat.project.configuration.raw.packages_configuration import PackagesConfiguration


class RawConfiguration(BaseModel):
    build: BuildConfiguration
    packages: PackagesConfiguration
