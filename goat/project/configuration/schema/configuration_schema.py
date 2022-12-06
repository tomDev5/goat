from pydantic import BaseModel
from goat.project.configuration.schema.build_configuration_schema import (
    BuildConfigurationSchema,
)


class ConfigurationSchema(BaseModel):
    build: BuildConfigurationSchema
