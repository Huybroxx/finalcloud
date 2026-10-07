from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="FastAPI DevOps Service", description="Project name")
    VERSION: str = Field(default="1.0.0", description="Application version")
    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")
    ENVIRONMENT: str = Field(default="production", description="Runtime environment")
    DEBUG: bool = Field(default=False, description="Debug flag")
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    COLOR: str = Field(default="blue", description="Active deployment color: blue or green")

    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    DB_NAME: str = Field(default="fastapi_prod", description="Database name")
    DB_USER: str = Field(default="postgres", description="Database username")
    DB_PASSWORD: str = Field(default="", description="Database password")

    AWS_REGION: str = Field(default="ap-southeast-1", description="AWS Region")
    AWS_BUCKET_NAME: str = Field(
        default="fastapi-app-files-huynn69", description="AWS S3 Bucket name"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


settings = Settings()
