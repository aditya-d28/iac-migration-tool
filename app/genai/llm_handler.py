from langchain_anthropic import AnthropicLLM
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class LLM:
    def __init__(self, llm_provider: str = settings.LLM_PROVIDER, **kwargs) -> None:
        if llm_provider == "ANTHROPIC":
            self._model = AnthropicLLM(model = settings.LLM_MODEL_NAME, **kwargs)
            logger.debug(f"{llm_provider}:{settings.LLM_MODEL_NAME} instanciated")
        elif llm_provider == "GOOGLE":
            pass
        elif llm_provider == "OPENAI":
            pass
        else:
            logger.error("Unknown model type.")
            raise ValueError("Unknown model type.")
        
    def invoke(self, prompt: str):
        try:
            response = self._model.invoke(prompt)
            logger.debug("Response recieved from LLM.")
            return response
        except Exception as err:
            logger.error(f"Error while calling the LLM: {str(err)}")
            raise Exception("Error while calling the LLM.")
        
    async def ainvoke(self, prompt: str):
        try:
            response = self._model.ainvoke(prompt)
            logger.debug("Response recieved from LLM asynchronously.")
            return response
        except Exception as err:
            logger.error(f"Error while calling the LLM asynchronously: {str(err)}")
            raise Exception("Error while calling the LLM asynchronously.")