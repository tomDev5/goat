from pydantic import BaseModel


class PackagesConfigurationSchema(BaseModel):
    requirements: dict[str, str] | None = None
