from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings

from settings_config import build_settings_config, resolve_env_file_path


class GlobalSettings(BaseSettings):
    env_file_path: ClassVar[Path | None] = resolve_env_file_path()
    model_config = build_settings_config("GLOBAL_", env_file_path=env_file_path)

    database_url: str | None = None
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800
    log_console_level: str = "DEBUG"
    log_file_enabled: bool = False
    log_file_path: Path = Path("logs/app.log")
    log_file_level: str = "DEBUG"
    log_file_rotation: str = "10 MB"
    log_file_retention: str = "10 days"
    log_file_compression: str | None = "zip"


global_settings = GlobalSettings()
