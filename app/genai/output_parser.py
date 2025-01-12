from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain.output_parsers import PydanticOutputParser


class ModuleType(str, Enum):
    COMMUNITY = "COMMUNITY"
    CUSTOM = "CUSTOM"

class ResourceObject(BaseModel):
    resource: str
    module: Optional[str]
    type: Optional[ModuleType]

class ResourceList(BaseModel):
    items: List[ResourceObject]

resource_list_parser = PydanticOutputParser(pydantic_object=ResourceList)

class ModuleObject(BaseModel):
    module_name: str = Field(description="Name of the terraform module or example")
    path: str = Field(description="Directory path of the terraform module or example")

class ModuleList(BaseModel):
    items: List[ModuleObject] = Field(description="List of Module Objects")
    comments: str = Field(description="Remarks about the mapped resources, if required.")

relevant_module_list_parser = PydanticOutputParser(pydantic_object=ModuleList)