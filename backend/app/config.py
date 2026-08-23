from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    db_url: str | None = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "museum"
    db_user: str = "museum"
    db_password: str = ""

    # Application
    app_env: str = "development"
    backend_cors_origins: list[str] = ["http://localhost:5173"]

    @property
    def database_url(self) -> str:
        if self.db_url:
            return self.db_url

        if self.app_env == "development":
            return "sqlite:///./museum.db"

        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()  # type: ignore[call-arg]
