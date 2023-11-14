import requests
import boto3
from datetime import datetime as dt
from datetime import timedelta as td
import requests, boto3, os
from botocore.errorfactory import ClientError
 
def download_file(file):
  res = requests.get(f'https://data.gharchive.org/{file}')
  return res
 
def get_client():
  return boto3.client('s3')
 
def upload_s3(body, bucket, file):
  s3_client = get_client()
  res = s3_client.put_object(
    Bucket=bucket,
    Key=file,
    Body=body
  )
  return res

  def get_prev_file_name(bucket, file_prefix, bookmark_file, baseline_file):
    s3_client = get_client()
    try:
        bookmark_file = s3_client.get_object(
            Bucket=bucket,
            Key=f'{file_prefix}/{bookmark_file}'
        )
        prev_file = bookmark_file['Body'].read().decode('utf-8')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            prev_file = baseline_file
        else:
            raise
    return prev_file


def upload_bookmark(bucket, file_prefix, bookmark_file, bookmark_contents):
    s3_client = get_client()
    s3_client.put_object(
        Bucket=bucket,
        Key=f'{file_prefix}/{bookmark_file}',
        Body=bookmark_contents.encode('utf-8')
    )


def get_next_file_name(prev_file):
    dt_part = prev_file.split('.')[0]
    next_file = f"{dt.strftime(dt.strptime(dt_part, '%Y-%M-%d-%H') + td(days=1), '%Y-%M-%d-%-H')}.json.gz"
    return next_file
