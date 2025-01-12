from fastapi import APIRouter
from app.core.logger import get_logger
from app.model.pre_process_model import PreProcessRequestModel
from app.service.pre_process_service import clean_tf_dir, create_desc_file

router = APIRouter()
logger = get_logger("system")

@router.post("/preProcess",
             summary="Migrates the IAC from one cloud service to another.")
def pre_process_modules(request: PreProcessRequestModel):

    logger.info("Pre processing request recieved.")
    clean_tf_dir(request.tf_dir_path)
    create_desc_file(request.tf_dir_path)
    logger.info("Pre-processing of Terraform modules and examples completed.")


    
