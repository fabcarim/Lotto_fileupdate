from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Lotto Tracking"
    database_url: str = Field(default_factory=lambda: f"sqlite:///{Path('storage') / 'lotto.db'}")
    api_base_url: Optional[str] = Field(default=None, description="External tracking API base URL")
    api_token: Optional[str] = Field(default=None, description="Token for the tracking API")

    imap_host: Optional[str] = None
    imap_username: Optional[str] = None
    imap_password: Optional[str] = None
    imap_folder: str = "INBOX"

    excel_source_one: Optional[Path] = None
    excel_source_two: Optional[Path] = None

    bearer_token: str = Field(..., alias="LOTTO_BEARER_TOKEN")
    refresh_interval_days: int = Field(2, alias="REFRESH_INTERVAL_DAYS")

    storage_dir: Path = Field(default_factory=lambda: Path("storage"))
    exports_dir: Path = Field(default_factory=lambda: Path("storage/exports"))
    uploads_dir: Path = Field(default_factory=lambda: Path("storage/uploads"))


settings = Settings()

# Ensure directories exist at import time for first run setups
settings.storage_dir.mkdir(parents=True, exist_ok=True)
settings.exports_dir.mkdir(parents=True, exist_ok=True)
settings.uploads_dir.mkdir(parents=True, exist_ok=True)
