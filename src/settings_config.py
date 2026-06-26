import os
from pathlib import Path

from pydantic_settings import SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = ".env"


def resolve_env_file_path(
    env_file: str | Path | None = None,
    *,
    project_root: Path = PROJECT_ROOT,
) -> Path | None:
    """Resolve the shared settings env file from the project root."""
    raw_env_file = env_file if env_file is not None else os.getenv("ENV_FILE")
    env_file_path = (
        Path(raw_env_file).expanduser()
        if raw_env_file
        else project_root / DEFAULT_ENV_FILE
    )

    if not env_file_path.is_absolute():
        env_file_path = project_root / env_file_path

    resolved_env_file_path = env_file_path.resolve()
    return resolved_env_file_path if resolved_env_file_path.exists() else None


def build_settings_config(
    env_prefix: str,
    *,
    env_file_path: Path | None = None,
) -> SettingsConfigDict:
    resolved_env_file_path = (
        env_file_path if env_file_path is not None else resolve_env_file_path()
    )
    return SettingsConfigDict(
        env_prefix=env_prefix,
        env_file=str(resolved_env_file_path) if resolved_env_file_path else None,
        extra="ignore",
    )
