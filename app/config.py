from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

settings = Settings(database_url="postgresql://igor:0997471990@o.breeze.ua:5544/test_erp")
