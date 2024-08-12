import json
import boto3
from datetime import datetime, timedelta


def delete_existing_s3_directory(s3_client, bucket_name, s3_key):
    # List all objects with the specified prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_key)
    if 'Contents' in response:
        objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

        # Delete the listed objects
        s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
        print(f"Deleted existing directory: s3://{bucket_name}/{s3_key}, count: {response['KeyCount']}")


def get_date(dateformat):
    return (datetime.now() - timedelta(1)).strftime(dateformat)


# Example usage
def lambda_handler(event, context):
    data_list = list(range(1, 400))

    # AWS S3 configuration
    bucket_name = 'dhananjayasamantasinghar'
    bucket_dir = f'period={get_date("%Y-%m-%d")}/'

    s3_key = f'data/classification/{bucket_dir}'

    aws_access_key_id = '<aws_access_key_id>'
    aws_secret_access_key = '<aws_secret_access_key>'
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    delete_existing_s3_directory(s3_client, bucket_name, s3_key)
    return {
        'statusCode': 200,
        'body': json.dumps('Completed')
    }
