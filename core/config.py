from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DESCRIPTION: str
    VERSION: str
    API_V1_PREFIX: str

    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    AUTHJWT_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    class Config:
        env_file = ".env"


configs = Settings()
