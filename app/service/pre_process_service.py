import os
from app.core.logger import get_logger
from app.genai.prompts import COMMUNITY_MODULE_DESCRIPTION_PROMPT_TEMPLATE
from app.service.migrate_services import generate_module_description

logger = get_logger("system")

def clean_tf_dir(dir_path:str):
    retain_files = {"main.tf", "outputs.tf", "variables.tf", "README.md", "DESCRIPTION.md"}

    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name in retain_files or file_path.endswith(".tf"):
                continue
            else:
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted: {file_path}")
                except Exception as e:
                    logger.info(f"Error deleting {file_path}: {e}")

def create_desc_file(dir_path:str):
    for root, dirs, files in os.walk(dir_path):
        if "main.tf" in files and "DESCRIPTION.md" not in files:
            try:
                file_path = os.path.join(root, "DESCRIPTION.md")
                description = generate_module_description(root, COMMUNITY_MODULE_DESCRIPTION_PROMPT_TEMPLATE)
                with open(file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(description)
                logger.info(f"Description successfully written to {file_path}")
            except Exception as err:
                logger.error(f"An error occurred while creating description file for module {root}: {err}")
