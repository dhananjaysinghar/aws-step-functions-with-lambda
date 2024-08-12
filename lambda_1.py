import json
import boto3
import tempfile
import os
import math
from datetime import datetime, timedelta


def upload_list_in_chunks(data_list, bucket_name, s3_key, base_file_name, aws_access_key_id, aws_secret_access_key,
                          chunk_size=200):
    # Create a boto3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Calculate the number of chunks needed
    number_of_chunks = math.ceil(len(data_list) / chunk_size)
    for i in range(number_of_chunks):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size
        chunk = data_list[start_index:end_index]

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write("\n".join(map(str, chunk)))
            temp_file_path = temp_file.name

        # Define a unique key for each chunk
        s3_file_key = f"{s3_key}{base_file_name}_part_{i}.txt"
        buffer_size_kb = os.path.getsize(temp_file_path) / 1024

        # Upload the chunk to S3
        s3_client.upload_file(temp_file_path, bucket_name, s3_file_key)

        print(
            f"Chunk {i} uploaded to s3://{bucket_name}/{s3_file_key} with records: {len(chunk)}, size: {round(buffer_size_kb, 2)} KB")
        os.remove(temp_file_path)


def get_date(dateformat):
    return (datetime.now() - timedelta(1)).strftime(dateformat)


# Example usage
def lambda_handler(event, context):
    # Create a list of 500,000 numbers
    data_list = list(range(1, 400))

    # AWS S3 configuration
    bucket_name = 'dhananjayasamantasinghar'
    bucket_dir = f'period={get_date("%Y-%m-%d")}/'

    s3_key = f'data/classification/{bucket_dir}'
    base_file_name = f'test-{get_date("%H%M%S")}'

    aws_access_key_id = '<aws_access_key_id>'
    aws_secret_access_key = '<aws_secret_access_key>'

    # Upload list to S3 as text file
    upload_list_in_chunks(data_list, bucket_name, s3_key, base_file_name, aws_access_key_id, aws_secret_access_key,
                          200)
    return {
        'statusCode': 200,
        'body': json.dumps('Completed')
    }
