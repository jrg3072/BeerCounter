from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BACKEND_HOST: str
    BACKEND_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    MONGODB_URL: str
    CRYPT_KEY: str

    class Config:
        env_file = "secrets.env"
        env_file_encoding = "utf-8"

setting = Settings()