import os
from pathlib import Path
from typing import ClassVar

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class GlobalSettings(BaseSettings):
    env_file_path: ClassVar[Path] = Path(
        os.getenv("ENV_FILE", str(Path(__file__).resolve().parents[1] / ".env"))
    ).expanduser()
    model_config = ConfigDict(
        env_prefix="GLOBAL_",
        env_file=str(env_file_path) if env_file_path.exists() else None,
        extra="ignore",
    )
    database_url: str | None = None
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800


global_settings = GlobalSettings()
