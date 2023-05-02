from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

settings = Settings(database_url="sqlite:///./app/DB.db")
