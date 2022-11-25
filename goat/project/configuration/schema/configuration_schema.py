from pydantic import BaseModel
from goat.project.configuration.schema.build_configuration_schema import (
    BuildConfigurationSchema,
)
from goat.project.configuration.schema.packages_configuration_schema import (
    PackagesConfigurationSchema,
)


class ConfigurationSchema(BaseModel):
    build: BuildConfigurationSchema
    packages: PackagesConfigurationSchema
