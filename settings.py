from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        frozen = True

    OPENAI_API_KEY: str = Field(
        ...,
        description="Your OpenAI API key"
    )

    OLLAMA_MODEL: str = Field(
        default="llama3.2",
        description="Ollama model you choose"
    )

    OLLAMA_URL: str = Field(
        default="http://ollama:11434",
        description="Ollama base url"
    )

    MONGODB_USER: str = Field(
        ...,
        description="Your MongoDB username"
    )

    MONGODB_PASSWORD: str = Field(
        ...,
        description=""
    )

    MONGODB_HOST: str = Field(
        ...,
        description=""
    )

    MONGODB_PORT: int = Field(
        ...,
        description=""
    )

    MONGODB_URI: str = Field(
        ...,
        description=""
    )

    REDIS_HOST: str = Field(
        default="localhost",
        description="Your Redis host"
    )

    REDIS_PORT: int = Field(
        default=6379,
        description="Your Redis port"
    )

    AUTH_SECRET_KEY: str = Field(
        ...,
        description="OAuth2 secret key."
    )

    AUTH_ALGORITHM: str = Field(
        ...,
        description="OAuth2 hash algorithm"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(
        ...,
        description="OAuth2 access token expire minutes"
    )

    BASE_URL: str = Field(
        ...,
        description="Base URL for your FastAPI app"
    )

    BASE_USER_USERNAME: str = Field(
        ...,
        description="Base user username"
    )

    BASE_USER_PASSWORD: str = Field(
        ...,
        description="Base user password"
    )


settings = Settings()