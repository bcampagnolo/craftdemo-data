from os import path, makedirs
import boto3
from botocore.exceptions import ClientError


def s3_pull_file(bucket_name, filepath, local_dir):
    s3_client = boto3.client(service_name='s3')
    local_dirname = path.dirname(local_dir)

    if not path.exists(local_dirname):
        makedirs(local_dirname)
    try:
        s3_client.download_file(Bucket=bucket_name, Key=filepath,
                                Filename=local_dir)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
