from pydantic import ConfigDict, field_validator, EmailStr, PydanticUserError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:567234@localhost:5432/web_hw_10"
    SECRET_KEY_JWT: str = "1231321313"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "jHJ1V@example.com"
    MAIL_PASSWORD: str = "postgres"
    MAIL_FROM: str = "postgres"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "postgres"
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = "dkprmxdfc"
    CLD_API_KEY: int = 944274644849464
    CLD_API_SECRET: str = "F1HhaBKtjBsvGNk39O22WH6plcY"

    try:

        @field_validator("ALGORITHM")
        def validate_algorithm(self, v):
            if v not in ["HS256", "HS512"]:
                raise ValueError("ALGORITHM must be HS256 or HS512")
            return v

    except PydanticUserError as exc_info:
        assert exc_info.code == "validator-instance-method"

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )  # noqa


config = Settings()
