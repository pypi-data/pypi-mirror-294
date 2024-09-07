from .logging_pomes import (
    DEBUG, INFO, WARNING, ERROR, CRITICAL,
    PYPOMES_LOGGER, LOGGING_LEVEL, LOGGING_FORMAT,
    LOGGING_STYLE, LOGGING_FILE_PATH, LOGGING_FILE_MODE,
    logging_startup, logging_get_entries, logging_send_entries,
    logging_log_msgs, logging_log_debug, logging_log_error,
    logging_log_info, logging_log_critical, logging_log_warning,
    logging_service
)

__all__ = [
    # logging_pomes
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL",
    "PYPOMES_LOGGER", "LOGGING_LEVEL", "LOGGING_FORMAT",
    "LOGGING_STYLE", "LOGGING_FILE_PATH", "LOGGING_FILE_MODE",
    "logging_startup", "logging_get_entries", "logging_send_entries",
    "logging_log_msgs", "logging_log_debug", "logging_log_error",
    "logging_log_info", "logging_log_critical", "logging_log_warning",
    "logging_service"
]

from importlib.metadata import version
__version__ = version("pypomes_logging")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
