from fastapi import APIRouter
from app.core.logger import get_logger
from app.model.migrate_model import MigrateRequestModel, MigrateResponseModel, MigrationStatus
from app.service.migrate_services import display_tree_structure

router = APIRouter()
logger = get_logger(__name__)

@router.post("/migrate",
             response_model=MigrateResponseModel,
             summary="Migrates the IAC from one cloud service to another.")
def generate_response(request: MigrateRequestModel):

    logger.info("Request recieved.")

    display_tree_structure(dir_path=request.source_repo_path)

    responseData = MigrateResponseModel(
        status=MigrationStatus.SUCCESS,
        message="IAC converted successfully",
        output_path=""
    )

    return responseData