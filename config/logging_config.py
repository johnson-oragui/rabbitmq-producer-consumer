import logging.config

# Define the logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'app.log',
            'mode': 'a',
        },
        'error_file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'error.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'error_logger': {
            'handlers': ['error_file_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
