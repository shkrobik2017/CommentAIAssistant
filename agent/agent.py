from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from logger.logger import logger
from settings import settings


class CommentAgent:
    def __init__(self):
        self.model = OllamaLLM(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_URL
        )
        self.role_description_file = "agent_role.md"
        self.prompt_template = self._load_agent_role()

    def _load_agent_role(self) -> ChatPromptTemplate:
        with open(f"agent/{self.role_description_file}", "r") as file:
            return ChatPromptTemplate.from_template(file.read())

    async def generate_comment(self, content: str):
        try:
            chain = self.prompt_template | self.model
            result = await chain.ainvoke({"article": content})
            logger.info("Comments generated successfully")
            return result
        except Exception as ex:
            logger.error(f"An error occurred in generating comments: {ex}")
            raise ex
