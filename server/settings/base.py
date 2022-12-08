import os
from urllib.parse import urljoin

# Basic
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
DATA_PROVIDER = os.environ.get('DATA_PROVIDER', 'house_canary')

# House Canary
HOUSE_CANARY_API_URL = 'https://api.housecanary.com'
HOUSE_CANARY_API_PROPERTY_URL = urljoin(HOUSE_CANARY_API_URL, 'v2/property/details')
HOUSE_CANARY_API_USER = os.environ.get('HOUSE_CANARY_API_USER', '')
HOUSE_CANARY_API_PASSWORD = os.environ.get('HOUSE_CANARY_API_PASSWORD', '')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': (
                '[%(asctime)s] '
                '%(levelname)s '
                '%(message)s. '
                'Place: %(pathname)s %(funcName)s %(lineno)d'
            ),
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'server': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'werkzeug': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'py.warnings': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
    },
}
