import os

THESTAGE_CONFIG_DIR = os.getenv('THESTAGE_CONFIG_DIR', '.thestage')
THESTAGE_CONFIG_FILE = os.getenv('THESTAGE_CONFIG_FILE', 'config.json')
THESTAGE_AUTH_TOKEN = os.getenv('THESTAGE_AUTH_TOKEN', None)
THESTAGE_API_URL = os.getenv('THESTAGE_API_URL', 'https://backend.thestage.ai')
THESTAGE_DAEMON_ENV_PATH = os.getenv('THESTAGE_DAEMON_ENV_PATH', '/etc/thestage-daemon-environment')
THESTAGE_DAEMON_TOKEN_PATH = os.getenv('THESTAGE_DAEMON_TOKEN_PATH', '/etc/thestage-daemon-token')

THESTAGE_DAEMON_TOKEN = os.getenv('THESTAGE_DAEMON_TOKEN', None)
THESTAGE_DAEMON_BACKEND = os.getenv('THESTAGE_DAEMON_BACKEND', None)
