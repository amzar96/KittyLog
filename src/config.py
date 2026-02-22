from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    HOST: str = "http://localhost:8000"
    SESSION_SECRET_KEY: str = Field(default="change-me-in-production")

    GOOGLE_CLIENT_ID: str = Field(
        default="",
        validation_alias=AliasChoices("GOOGLE_CLIENT_ID", "CLIENT_ID"),
    )
    GOOGLE_CLIENT_SECRET: str = Field(
        default="",
        validation_alias=AliasChoices("GOOGLE_CLIENT_SECRET", "CLIENT_SECRET"),
    )
    GOOGLE_REDIRECT_PATH: str = Field(
        default="auth",
        validation_alias=AliasChoices("GOOGLE_REDIRECT_PATH", "CLIENT_REDIRECT_PATH"),
    )

    SUPABASE_DB_URL: str = Field(
        default="sqlite:///kittylog-dev.db",
        validation_alias=AliasChoices("SUPABASE_DB_URL", "DB_URL"),
    )

    DB_SCHEMA: str = Field(default="kittylog")

    FRONTEND_URL: str = "http://localhost:5173" # TODO: make this configurable

    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    @property
    def GOOGLE_REDIRECT_URL(self) -> str:
        return f"{self.HOST}/{self.GOOGLE_REDIRECT_PATH}"


settings = Settings()
