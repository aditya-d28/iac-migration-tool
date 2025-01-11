import os
import hcl
import json
from app.core.logger import get_logger
from app.genai.prompts import RESOURCE_LIST_EXTRACTION_PROMPT
from app.genai.output_parser import ModuleType, ResourceObject, ResourceList, resource_list_parser
from app.genai.llm_handler import LLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

logger = get_logger("system")

def display_tree_structure(dir_path, indent="", is_last=True):
    """Recursively display the tree structure of a given directory."""
    try:
        dir_name = os.path.basename(dir_path) or dir_path
        connector = "└── " if is_last else "├── "
        print(f"{indent}{connector}{dir_name}")
        indent += "    " if is_last else "│   "

        # Get all items in the directory
        items = sorted(os.listdir(dir_path))
        item_count = len(items)

        for index, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last_item = index == item_count - 1

            if os.path.isdir(item_path):
                # Recursively display directories
                display_tree_structure(item_path, indent, is_last_item)
            else:
                # Display files
                connector = "└── " if is_last_item else "├── "
                print(f"{indent}{connector}{item}")
    except PermissionError:
        print(f"{indent}└── [Permission Denied]")


def load_file(file_path: str):
    if not os.path.isfile(file_path):
        logger.error(f"The file {file_path} does not exist.")
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    try:
        with open(file_path, 'r') as file:
            if file_path.endswith(".tf"):
                return hcl.load(file)
            if file_path.endswith(".json"):
                return json.load(file)
    except Exception as err:
        logger.error(f"Error while loading file: {file_path} : {str(err)}")
        raise Exception(f"Error while loading file: {file_path}")


def get_resource_list(dir_path: str, entrypoint_file: str):
    try:
        file_path = dir_path + "/" + entrypoint_file
        file_content = load_file(file_path)
        logger.debug(f"File loaded: {file_path}")

        #Extracting Using LLM
        # prompt = ChatPromptTemplate.from_template(RESOURCE_LIST_EXTRACTION_PROMPT).partial(
        #     file_name = entrypoint_file,
        #     instructions = resource_list_parser.get_format_instructions()
        # )
        # llm_model = LLM(temperature = 0.5, max_retries=1)
        # chain = prompt | RunnableLambda(llm_model.invoke) | resource_list_parser
        # resource_list = chain.invoke({"file_content": file_content})
        # return resource_list

        #Extracting Programatically
        results = []
        if "module" in file_content:
            for module_name, module_details in file_content["module"].items():
                source = module_details.get("source", "")
                resource = module_name if entrypoint_file.endswith(".tf") else source.split("/")[-1]
                module_type = (
                    ModuleType.CUSTOM if source.startswith("./") else ModuleType.COMMUNITY
                )
                results.append(
                    ResourceObject(
                        resource=resource,
                        module=source,
                        type=module_type,
                    )
                )
        if "resource" in file_content:
            for resource_type, resource_instances in file_content["resource"].items():
                for resource_name in resource_instances.keys():
                    results.append(
                        ResourceObject(
                            resource=f"{resource_type}.{resource_name}",
                            module=None,
                            type=None,
                        )
                    )
        return ResourceList(items=results)
    except Exception as err:
        logger.error(f"Error while extracting resource details: {str(err)}")
        raise Exception("Error while extracting resource details.")
