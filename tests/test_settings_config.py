from typing import get_type_hints

from pydantic_settings import SettingsConfigDict

from settings_config import build_settings_config, resolve_env_file_path


def test_resolve_default_env_file_from_project_root(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("GLOBAL_DATABASE_URL=postgresql+psycopg://example\n")
    monkeypatch.delenv("ENV_FILE", raising=False)

    assert resolve_env_file_path(project_root=tmp_path) == env_file.resolve()


def test_resolve_relative_env_file_override_from_project_root(tmp_path, monkeypatch):
    env_dir = tmp_path / "config"
    env_dir.mkdir()
    env_file = env_dir / "local.env"
    env_file.write_text("GLOBAL_DATABASE_URL=postgresql+psycopg://example\n")
    monkeypatch.setenv("ENV_FILE", "config/local.env")

    assert resolve_env_file_path(project_root=tmp_path) == env_file.resolve()


def test_resolve_missing_env_file_returns_none(tmp_path, monkeypatch):
    monkeypatch.setenv("ENV_FILE", "missing.env")

    assert resolve_env_file_path(project_root=tmp_path) is None


def test_build_settings_config_uses_shared_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("FEATURE_ENABLED=true\n")

    config = build_settings_config("FEATURE_", env_file_path=env_file)

    assert config["env_prefix"] == "FEATURE_"
    assert config["env_file"] == str(env_file)
    assert config["extra"] == "ignore"


def test_build_settings_config_is_typed_for_base_settings():
    assert get_type_hints(build_settings_config)["return"] is SettingsConfigDict
