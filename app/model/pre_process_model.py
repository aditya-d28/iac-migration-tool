from pydantic import Field
from app.model.iac_migration_base_model import IacMigrationBaseModel


class PreProcessRequestModel(IacMigrationBaseModel):
    tf_dir_path: str = Field(
        ...,
        title="Terraform Directory Path",
        description="Local file path where all the terraform community modules and examples are saved."
    )