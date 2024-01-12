from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = "http://127.0.0.1:8000"
