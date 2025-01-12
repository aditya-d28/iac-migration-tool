import os
import hcl
import json
from rich.console import Console
from rich.markdown import Markdown
from app.core.logger import get_logger
from app.genai.prompts import RESOURCE_LIST_EXTRACTION_PROMPT_TEMPLATE, RELEVANT_MODULE_EXTRACTION_PROMPT_TEMPLATE, MODULE_MAPPING_PROMPT_TEMPLATE
from app.genai.output_parser import ModuleType, ResourceObject, ResourceList, resource_list_parser, relevant_module_list_parser
from app.genai.llm_handler import LLM
from app.core.config import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

logger = get_logger("system")

def get_tree_structure(dir_path: str, indent="", is_last=True, output=None):
    if output is None:
        output = []

    try:
        dir_name = os.path.basename(dir_path) or dir_path
        connector = "└── " if is_last else "├── "
        output.append(f"{indent}{connector}{dir_name}")
        indent += "    " if is_last else "│   "
        items = sorted(os.listdir(dir_path))
        item_count = len(items)

        for index, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last_item = index == item_count - 1

            if os.path.isdir(item_path):
                get_tree_structure(item_path, indent, is_last_item, output)
            else:
                connector = "└── " if is_last_item else "├── "
                output.append(f"{indent}{connector}{item}")
    except PermissionError:
        output.append(f"{indent}└── [Permission Denied]")
    
    return "\n".join(output)


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


def get_resource_list(dir_path: str, entrypoint_file: str, request_id: str):
    try:
        file_path = dir_path + "/" + entrypoint_file
        file_content = load_file(file_path)
        logger.debug(f"File loaded: {file_path}")

        #Extracting Using LLM
        # prompt = ChatPromptTemplate.from_template(RESOURCE_LIST_EXTRACTION_PROMPT_TEMPLATE).partial(
        #     file_name = entrypoint_file,
        #     instructions = resource_list_parser.get_format_instructions()
        # )
        # llm_model = LLM(temperature = settings.LLM_TEMPERATURE, max_retries=settings.LLM_MAX_RETRIES)
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
        output = "# Migration Report: <br>\nResources found in the terraform repository: <br>\n | Resource | Module |\n |-------|-------|\n"
        for result in results:
            output = f"{output} | {result.resource} | {result.module} |\n"
        write_to_output(output, request_id)
        logger.info(f"Extracted the list of resources from {entrypoint_file}.")
        return ResourceList(items=results)
    except Exception as err:
        logger.error(f"Error while extracting resource details: {str(err)}")
        raise Exception("Error while extracting resource details.")
    
def write_to_output(output: str, uuid: str):
    try:
        file_path = os.path.join(settings.OUTPUT_DIR, uuid + "_REPORT.md")
        with open(file_path, "a") as file:
            file.write(output)
    except Exception as err:
        logger.error(f"Error while writing to the report file: {str(err)}")
        raise Exception("Error while writing to the report file.")


def get_module_content(module_path: str):
    files_content = ""
    for file_name in os.listdir(module_path):
        file_path = os.path.join(module_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                files_content = files_content + "**" + file_name + ":**<br>\n```<br>\n" + content + "```<br>\n<br>\n"
    return files_content
    

def generate_module_description(module_path: str, prompt_template: str):
    try:
        module_content = get_module_content
        prompt = ChatPromptTemplate.from_template(prompt_template)
        llm_model = LLM(temperature = settings.LLM_TEMPERATURE, max_retries=settings.LLM_MAX_RETRIES)
        chain = prompt | RunnableLambda(llm_model.invoke)
        description = chain.invoke({"files": module_content}).content
        logger.info(f"Generated description of {module_path} module.")
        console = Console()
        console.print(Markdown(description))
        return description
    except Exception as err:
        logger.error(f"Error while generating module description: {str(err)}")
        raise Exception("Error while generating module description")


def get_relevant_modules_and_examples(dir_path:str, source_module: ResourceObject, source_cloud_service: str, target_cloud_service: str, request_id: str):
    try:
        module_path = os.path.abspath(os.path.join(dir_path, source_module.module))
        module_content = get_module_content(module_path)
        target_tf_tree_structure = get_tree_structure(settings.TF_COMMUNITY_MODULES_PATH)
        prompt = ChatPromptTemplate.from_template(RELEVANT_MODULE_EXTRACTION_PROMPT_TEMPLATE).partial(
            source_cloud_service = source_cloud_service,
            target_cloud_service = target_cloud_service,
            target_tf_tree_structure = target_tf_tree_structure,
            instructions = relevant_module_list_parser.get_format_instructions()
        )
        llm_model = LLM(temperature = settings.LLM_TEMPERATURE, max_retries=settings.LLM_MAX_RETRIES)
        chain = prompt | RunnableLambda(llm_model.invoke) | relevant_module_list_parser
        relevant_module_list = chain.invoke({"module_content": module_content})
        logger.info(f"Obtained relevant modules and examples for {source_module.resource}.")
        output = f"\n## {source_module.resource} ```({source_module.module})``` <br>\n### List of relevant modules:<br>\n"
        for item in  relevant_module_list.items:
            output = f"{output} - Module: {item.module_name}<br>\n   Path: {item.path}<br>\n"
        output = f"{output} <br>\n \n**Remarks:** {relevant_module_list.comments}<br>\n<br>\n"
        write_to_output(output, request_id)
        return relevant_module_list
    except Exception as err:
        logger.error(f"Error while extracting relevant modules: {str(err)}")
        raise Exception("Error while extracting relevant modules.")


def get_resource_mapping(dir_path:str, resources: ResourceList, source_cloud_service: str, target_cloud_service: str, request_id: str):
    try:
        for source_module in resources.items:
            relevant_modules = get_relevant_modules_and_examples(dir_path, source_module, source_cloud_service, target_cloud_service, request_id)
            source_module_content = get_module_content(os.path.abspath(os.path.join(dir_path, source_module.module)))
            relevant_module_descriptions = ""
            for module in relevant_modules.items:
                description_file_path = os.path.join(settings.TF_COMMUNITY_MODULES_PATH, module.path, "DESCRIPTION.md")
                if os.path.isfile(description_file_path):
                    with open(description_file_path, 'r') as file:
                        content = file.read()
                    relevant_module_descriptions = f"{relevant_module_descriptions} **Module Name: {module.module_name}** \n Module Path: {module.path} \n Module Description: \n```{content}```\n\n"

            prompt = ChatPromptTemplate.from_template(MODULE_MAPPING_PROMPT_TEMPLATE).partial(
                source_cloud_service = source_cloud_service,
                target_cloud_service =target_cloud_service,
                relevant_module_descriptions = relevant_module_descriptions,
                instructions = relevant_module_list_parser.get_format_instructions()
            )
            llm_model = LLM(temperature = settings.LLM_TEMPERATURE, max_retries=settings.LLM_MAX_RETRIES)
            chain = prompt | RunnableLambda(llm_model.invoke) | relevant_module_list_parser
            mapped_modules = chain.invoke({"source_module_content": source_module_content})
            logger.info(f"Obtained mapping for {source_module.resource}.")
            output = "\n### Module Mapping:<br>\n"
            for item in  mapped_modules.items:
                output = f"{output} - Module: {item.module_name}<br>\n   Path: {item.path}<br>\n"
            output = f"{output} <br>\n \n**Remarks:** {mapped_modules.comments}<br>\n<br>\n"
            write_to_output(output, request_id)
    except Exception as err:
        logger.error(f"Error while mapping a resource: {str(err)}")
        raise Exception("Error while mapping a resource.")
