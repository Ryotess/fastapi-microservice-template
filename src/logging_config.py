# src/logging_config.py
import sys
from collections.abc import Callable
from pathlib import Path

from loguru import logger

from config import GlobalSettings, global_settings
from settings_config import PROJECT_ROOT


def _resolve_log_file_path(log_file_path: Path) -> Path:
    if log_file_path.is_absolute():
        return log_file_path
    return PROJECT_ROOT / log_file_path


def setup_logging(settings: GlobalSettings = global_settings) -> Callable[[], None]:
    """
    Configure loguru sinks and return a shutdown hook that flushes/tears down
    the async queue created by enqueue=True.
    """
    logger.remove()

    sinks = [
        logger.add(
            sys.stdout,
            level=settings.log_console_level,
            enqueue=True,
        )
    ]

    if settings.log_file_enabled:
        log_file_path = _resolve_log_file_path(settings.log_file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        sinks.append(
            logger.add(
                log_file_path,
                rotation=settings.log_file_rotation,
                retention=settings.log_file_retention,
                compression=settings.log_file_compression,
                level=settings.log_file_level,
                enqueue=True,
            )
        )

    def shutdown() -> None:
        for sink_id in sinks:
            logger.remove(sink_id)
        logger.complete()

    return shutdown


# Initialize logging once at import and expose shutdown hook
shutdown_logging = setup_logging()
