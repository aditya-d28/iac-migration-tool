import os
import uuid
from fastapi import APIRouter
from app.core.logger import get_logger
from app.core.config import settings
from app.model.migrate_model import MigrateRequestModel, MigrateResponseModel, MigrationStatus
from app.service.migrate_services import get_resource_list, get_resource_mapping

router = APIRouter()
logger = get_logger("system")

@router.post("/migrate",
             response_model=MigrateResponseModel,
             summary="Migrates the IAC from one cloud service to another.")
def generate_response(request: MigrateRequestModel):

    logger.info("Request recieved.")
    request_id = str(uuid.uuid4())
    output_dir = os.path.join(settings.OUTPUT_DIR, request_id + "_REPORT.md")
    resources = get_resource_list(request.source_repo_path, request.entrypoint_file, request_id)
    get_resource_mapping(request.source_repo_path, resources, request.source_cloud_service, request.target_cloud_service, request_id)
    
    responseData = MigrateResponseModel(
        status=MigrationStatus.SUCCESS,
        message="IAC converted successfully",
        output_path=output_dir
    )

    return responseData