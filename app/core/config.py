import os
from typing import Annotated, Any

from pydantic import (
    AnyUrl,
    BeforeValidator
)
from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = os.path.join(os.path.dirname(__file__), '../../.env')

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path, env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str
    CONSOLE_LOG_LEVEL: str
    FILE_LOG_LEVEL: str
    DEV_MODE: str
    LLM_PROVIDER: str
    LLM_MODEL_NAME: str
    ALLOWED_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @property
    def ALLOWED_ORIGINS_LIST(self) -> list[str]:
        if self.DEV_MODE == "Y":
            return ["*"]
        return self.ALLOWED_ORIGINS


settings = Settings()  # type: ignore