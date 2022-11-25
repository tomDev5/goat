from pydantic import BaseModel
from goat.project.configuration.schema.build_configuration_variant_schema import (
    BuildConfigurationVariantSchema,
)


class BuildConfigurationSchema(BaseModel):
    all: BuildConfigurationVariantSchema
    release: BuildConfigurationVariantSchema
    debug: BuildConfigurationVariantSchema
    test: BuildConfigurationVariantSchema
