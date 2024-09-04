import logging
from config.logging_config import setup_logging

setup_logging()

warning_logger = logging.getLogger('')

def warning_consumer(body):
    """Logs warning messages to the general log file."""
    try:
        warning_logger.warning(f"Processing WARNING log: {body}")
        print(f"Warning logged: {body}")
    except Exception as exc:
        print(f"Failed to log warning: {exc}")
