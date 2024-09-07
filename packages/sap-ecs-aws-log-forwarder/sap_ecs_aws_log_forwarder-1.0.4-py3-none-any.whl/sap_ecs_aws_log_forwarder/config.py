import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
TIMEOUT_DURATION = None if os.getenv('TIMEOUT_DURATION') is None else int(os.getenv('TIMEOUT_DURATION'))  # Timeout duration in seconds
OUTPUT_METHOD = os.getenv('OUTPUT_METHOD', 'http')  # 'http' or 'files'

HTTP_ENDPOINT = os.getenv('HTTP_ENDPOINT')
TLS_CERT_PATH = os.getenv('TLS_CERT_PATH')
TLS_KEY_PATH = os.getenv('TLS_KEY_PATH')
AUTH_METHOD = os.getenv('AUTH_METHOD', 'token')  # 'token' or 'api_key'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
API_KEY = os.getenv('API_KEY')

OUTPUT_DIR = os.getenv('OUTPUT_DIR')
