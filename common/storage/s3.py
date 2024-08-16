import boto3
import logging

from common.storage import StorageService
from environment.variables import EnvironmentVariable


# Creating S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id=EnvironmentVariable.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=EnvironmentVariable.AWS_SECRET_ACCESS_KEY,
    region_name=EnvironmentVariable.AWS_S3_REGION_NAME,
    endpoint_url=EnvironmentVariable.AWS_S3_BASE_URL,
)


class S3StorageService(StorageService):

    def __init__(self, kind, bucket_name=EnvironmentVariable.AWS_STORAGE_BUCKET_NAME):
        super().__init__(kind)
        self.client = s3_client
        self.bucket_name = bucket_name

    def get_key(self, filename):
        key = super().get_key(filename)
        return f'{EnvironmentVariable.AWS_MEDIA_FOLDER}/{key}'

    def upload(self, filename, file_bytes, content_type=None, acl='public-read'):
        kwargs = dict(Bucket=self.bucket_name, Key=self.get_key(filename), Body=file_bytes, ACL=acl)
        if content_type := content_type or self.get_content_type(filename):
            kwargs['ContentType'] = content_type
        logging.info(f'Upload initiated for key {kwargs["Key"]}...')
        self.client.put_object(**kwargs)
        logging.info(f'Upload Completed!')
        return {
            'key': kwargs['Key'],
            'bucket': kwargs['Bucket'],
            'url': self.get_url(kwargs['Key'], acl == 'private')
        }

    def get_pre_signed_url(self, key):
        return self.client.generate_presigned_url(ClientMethod='get_object', Params={
            'Bucket': EnvironmentVariable.AWS_STORAGE_BUCKET_NAME, 'Key': key
        })

    def get_url(self, key, signed=False):
        if not signed:
            return f'{EnvironmentVariable.AWS_S3_BASE_URL}/{EnvironmentVariable.AWS_STORAGE_BUCKET_NAME}/{key}'
        return self.get_pre_signed_url(key)
