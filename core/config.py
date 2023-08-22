from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DESCRIPTION: str
    VERSION: str
    API_V1_PREFIX: str

    AUTHJWT_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    DEBUG: bool = False
    SENTRY_DSN: str = None
    ECP_SERVICE_URL: str = None

    GENERATE_IP: str = None
    SQLALCHEMY_ECHO: bool = False

    SENTRY_ENABLED: bool = False

    class Config:
        env_file = ".env"


configs = Settings()
