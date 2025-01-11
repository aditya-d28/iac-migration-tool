from enum import Enum
from pydantic import Field, model_validator
from app.core.logger import get_logger
from app.model.iac_migration_base_model import IacMigrationBaseModel

logger = get_logger(__name__)

class CloudService(str, Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"

class MigrationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    IN_PROGRESS = "IN_PROGRESS"

class MigrateRequestModel(IacMigrationBaseModel):
    source_repo_path: str = Field(
        ...,
        title="Source Repository Path",
        description="Local file path where the existing Infrastructure as Code (IaC) repository is stored. This path should point to the directory containing the IaC configurations."
    )
    entrypoint_file: str = Field(
        ...,
        title="Entrypoint File Name",
        description=""
    )
    source_cloud_service: CloudService = Field(
        ...,
        title="Source Cloud Service",
        description="The cloud service provider (e.g., AWS, Azure, GCP) of the existing IaC configuration. This indicates the platform the current IaC is designed for."
    )
    target_cloud_service: CloudService = Field(
        ...,
        title="Target Cloud Service",
        description="The cloud service provider (e.g., AWS, Azure, GCP) to which the IaC should be converted. This specifies the platform for which the IaC will be generated."
    )

    @model_validator(mode="before")
    def check_cloud_services_different(cls, values):
        source_service = values.get('sourceCloudService')
        target_service = values.get('targetCloudService')
        
        # Check if source and target cloud services are different
        if source_service == target_service:
            logger.error('Source and target cloud services must be different.')
            raise ValueError('Source and target cloud services must be different.')
        
        return values

class MigrateResponseModel(IacMigrationBaseModel):
    status: MigrationStatus = Field(
        ...,
        title="Status",
        description="The result of the IaC migration process, indicating whether the conversion was successful or encountered issues."
    )
    message: str = Field(
        ...,
        title="Message",
        description="A detailed message about the migration process, including any error or success information. It provides additional context for the status."
    )
    output_path: str = Field(
        ...,
        title="Output Path",
        description="The file path where the converted IaC files are saved. This is the location of the IaC repository for the target cloud service."
    )
