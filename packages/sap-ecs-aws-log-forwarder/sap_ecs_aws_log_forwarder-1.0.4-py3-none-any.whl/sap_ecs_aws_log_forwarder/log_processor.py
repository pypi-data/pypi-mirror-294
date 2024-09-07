import os
import requests
import gzip
import logging
from botocore.exceptions import ClientError
from .config import OUTPUT_METHOD, HTTP_ENDPOINT, TLS_CERT_PATH, TLS_KEY_PATH, AUTH_METHOD, AUTH_TOKEN, API_KEY, OUTPUT_DIR

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(s3_client, bucket_name, object_key):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read()
    except ClientError as e:
        logging.error(f"Failed to download file: s3://{bucket_name}/{object_key}, error: {e}")
        raise

def process_log_file(s3_client, bucket_name, object_key):
    compressed_content = download_file(s3_client, bucket_name, object_key)
    decompressed_content = gzip.decompress(compressed_content).decode('utf-8')
    logs = decompressed_content.split('\n')

    if OUTPUT_METHOD == 'files':
        normalized_output_dir_path = OUTPUT_DIR if OUTPUT_DIR.endswith('/') else OUTPUT_DIR + '/'
        local_path = os.path.join(normalized_output_dir_path, object_key)
        local_dir = os.path.dirname(local_path)

        os.makedirs(local_dir, exist_ok=True)
        with gzip.open(local_path, 'at') as file:
            for log in logs:
                if log.strip():
                    write_log_to_file(log, file)
    else:
        for log in logs:
            if log.strip():
                send_log_to_http(log)

def send_log_to_http(log):
    try:
        headers = {'Content-Type': 'application/json'}
        cert = None

        if TLS_CERT_PATH and TLS_KEY_PATH:
            cert = (TLS_CERT_PATH, TLS_KEY_PATH)

        if AUTH_METHOD == 'token' and AUTH_TOKEN:
            headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
        elif AUTH_METHOD == 'api_key' and API_KEY:
            headers['X-API-Key'] = API_KEY

        response = requests.post(HTTP_ENDPOINT, data=log, headers=headers, cert=cert)
        response.raise_for_status()
        logging.info(f"Log forwarded successfully to HTTP endpoint: {log}")
    except Exception as e:
        logging.error(f"Failed to forward log to HTTP endpoint, error: {e}")

def write_log_to_file(log, file):
    try:
        file.write(log + '\n')
        logging.info(f"Log written successfully to file: {log}")
    except Exception as e:
        logging.error(f"Failed to write log to file, error: {e}")
