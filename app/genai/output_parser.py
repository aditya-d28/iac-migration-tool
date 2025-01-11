from enum import Enum
from pydantic import BaseModel
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