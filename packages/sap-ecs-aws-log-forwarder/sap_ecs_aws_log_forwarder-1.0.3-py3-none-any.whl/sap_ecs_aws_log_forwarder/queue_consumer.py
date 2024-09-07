import time
import json
import logging
import boto3
from .config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SQS_QUEUE_URL, TIMEOUT_DURATION, OUTPUT_METHOD, HTTP_ENDPOINT, AUTH_METHOD, AUTH_TOKEN, API_KEY, OUTPUT_DIR
from .log_processor import process_log_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize SQS and S3 clients
sqs_client = boto3.client('sqs', region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3_client = boto3.client('s3', region_name=AWS_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

MAX_RETRIES = 5  # Maximum number of retries for a message

def validate_inputs():
    errors = []

    def validate_string(var_name, var_value):
        if not var_value or not isinstance(var_value, str):
            errors.append(f"{var_name} is required and must be a string.")

    validate_string("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID)
    validate_string("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
    validate_string("AWS_REGION", AWS_REGION)
    validate_string("SQS_QUEUE_URL", SQS_QUEUE_URL)
    validate_string("OUTPUT_METHOD", OUTPUT_METHOD)

    if OUTPUT_METHOD not in ['http', 'files']:
        errors.append("OUTPUT_METHOD must be either 'http' or 'files'.")

    if OUTPUT_METHOD == 'http':
        validate_string("HTTP_ENDPOINT", HTTP_ENDPOINT)
        validate_string("AUTH_METHOD", AUTH_METHOD)
        if AUTH_METHOD not in ['token', 'api_key']:
            errors.append("AUTH_METHOD must be either 'token' or 'api_key' when OUTPUT_METHOD is 'http'.")
        if AUTH_METHOD == 'token':
            validate_string("AUTH_TOKEN", AUTH_TOKEN)
        elif AUTH_METHOD == 'api_key':
            validate_string("API_KEY", API_KEY)
    elif OUTPUT_METHOD == 'files':
        validate_string("OUTPUT_DIR", OUTPUT_DIR)

    if errors:
        raise ValueError("Input validation failed with the following errors:\n" + "\n".join(errors))

def is_relevant_event(object_key):
    """Filter relevant events based on the message body."""
    relevant_identifier = 'logserv'
    return relevant_identifier in object_key

def process_message(record, message_id, message_body, receipt_handle):
    event_type = record.get('eventName', '')
    s3_info = record.get('s3', {})
    bucket_name = s3_info.get('bucket', {}).get('name', '')
    object_key = s3_info.get('object', {}).get('key', '')

    if event_type != 'ObjectCreated:Put' or not is_relevant_event(object_key):
        logging.debug(f"Irrelevant message: event_type={event_type}, object_key={object_key}. Skipping message.")
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
        return

    # Extract or initialize retry count
    retry_count = int(record.get('retry_count', 0))

    if retry_count >= MAX_RETRIES:
        logging.error(f"Max retries reached for message: {message_id}. Deleting message.")
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
        return

    if not bucket_name or not object_key:
        logging.error(f"No bucket name or object key found in message: {message_id} - {record}")
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
        return

    try:
        logging.info(f"Processing message: {message_id} - s3://{bucket_name}/{object_key}")
        process_log_file(s3_client, bucket_name, object_key)
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
        logging.info(f"Message processed and deleted: {message_id}")
    except Exception as e:
        logging.error(f"Error processing message {message_id}: {e}")
        # Increment retry count and update the record
        retry_count += 1
        record['retry_count'] = retry_count
        message_body['Records'] = [record]
        updated_message = json.dumps(message_body)
        # Repost the entire message back to the queue
        sqs_client.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=updated_message)
        # Delete the original message to avoid loops
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)

def consume_queue():
    # Validate inputs before starting the queue consumer
    validate_inputs()
    start_time = time.time()

    try:
        while True:
            elapsed_time = time.time() - start_time
            if TIMEOUT_DURATION and elapsed_time > TIMEOUT_DURATION:
                logging.info("Timeout reached. Exiting.")
                break

            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
                VisibilityTimeout=10
            )
            messages = response.get('Messages', [])
            if not messages:
                logging.info("No messages in the queue. Waiting...")
                continue

            for message in messages:
                message_id = message['MessageId']
                message_body = json.loads(message['Body'])
                records = message_body.get('Records', [])
                receipt_handle = message['ReceiptHandle']

                for record in records:
                    process_message(record, message_id, message_body, receipt_handle)

    except KeyboardInterrupt:
        logging.info("Forwarder stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    consume_queue()