import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenOCR API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # OCR Settings
    USE_GPU: bool = False
    OCR_LANG: str = "en"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
