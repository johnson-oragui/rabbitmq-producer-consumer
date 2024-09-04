import logging
from config.logging_config import setup_logging

# Setup logging
setup_logging()

# Get specific loggers
error_logger = logging.getLogger('error_logger')

def error_consumer(body):
    """Logs error messages to a specific error log file."""
    try:
        error_logger.error(f"Processing ERROR log: {body}")
        print(f"Error logged: {body}")
    except Exception as exc:
        print(f"Failed to log error: {exc}")
