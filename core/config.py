from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    api_key: str = "your_default_api_key"
    temperature: float = 0.7

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("temperature must be between 0.0 and 1.0")
        return v

settings = Settings()
