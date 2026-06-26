from pathlib import Path
from types import SimpleNamespace

import logging_config


class FakeLogger:
    def __init__(self):
        self.add_calls = []
        self.complete_calls = 0
        self.remove_calls = []

    def add(self, sink, **kwargs):
        self.add_calls.append((sink, kwargs))
        return len(self.add_calls)

    def complete(self):
        self.complete_calls += 1

    def remove(self, sink_id=None):
        self.remove_calls.append(sink_id)


def make_settings(log_file_path: Path, *, log_file_enabled: bool):
    return SimpleNamespace(
        log_console_level="INFO",
        log_file_enabled=log_file_enabled,
        log_file_path=log_file_path,
        log_file_level="DEBUG",
        log_file_rotation="1 MB",
        log_file_retention="1 day",
        log_file_compression="zip",
    )


def test_setup_logging_uses_console_only_when_file_logging_disabled(
    tmp_path, monkeypatch
):
    fake_logger = FakeLogger()
    monkeypatch.setattr(logging_config, "logger", fake_logger)
    log_file_path = tmp_path / "logs" / "app.log"

    shutdown = logging_config.setup_logging(
        make_settings(log_file_path, log_file_enabled=False)
    )

    assert len(fake_logger.add_calls) == 1
    assert fake_logger.add_calls[0][1]["level"] == "INFO"
    assert not log_file_path.parent.exists()

    shutdown()

    assert fake_logger.remove_calls == [None, 1]
    assert fake_logger.complete_calls == 1


def test_setup_logging_adds_file_sink_only_when_enabled(tmp_path, monkeypatch):
    fake_logger = FakeLogger()
    monkeypatch.setattr(logging_config, "logger", fake_logger)
    log_file_path = tmp_path / "logs" / "app.log"

    shutdown = logging_config.setup_logging(
        make_settings(log_file_path, log_file_enabled=True)
    )

    assert log_file_path.parent.exists()
    assert len(fake_logger.add_calls) == 2
    assert fake_logger.add_calls[1][0] == log_file_path
    assert fake_logger.add_calls[1][1]["rotation"] == "1 MB"
    assert fake_logger.add_calls[1][1]["retention"] == "1 day"

    shutdown()

    assert fake_logger.remove_calls == [None, 1, 2]
    assert fake_logger.complete_calls == 1
