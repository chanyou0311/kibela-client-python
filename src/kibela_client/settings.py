from pydantic import BaseSettings

class Settings(BaseSettings):
    kibela_team: str
    kibela_access_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
