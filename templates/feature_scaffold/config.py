from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings

from settings_config import build_settings_config, resolve_env_file_path


class FeatureSettings(BaseSettings):
    """Feature-scoped settings from shared env sources; replace FEATURE_ prefix."""

    env_file_path: ClassVar[Path | None] = resolve_env_file_path()
    model_config = build_settings_config("FEATURE_", env_file_path=env_file_path)


feature_settings = FeatureSettings()
