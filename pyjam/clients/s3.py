"""S3 Client for PyJam"""

from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from pyjam.utils.s3 import (
    set_bucket_policy,
    set_website_config,
    delete_objects,
    upload_file
)


class S3Client:
    """Class for S3 Client"""
    def __init__(self, **kwargs):
        """Setup session and s3 ServiceResource"""
        params = {k:v for k, v in kwargs.items() if v is not None}

        self.session = boto3.Session(**params)
        self.s3 = self.session.resource('s3')


    def create_bucket(self, bucket_name):
        """Creates new S3 bucket in given region"""
        try:
            if self.session.region_name == 'us-east-1':
                print('\nCreating S3 bucket {0}.\n'.format(bucket_name))
                return self.s3.create_bucket(Bucket=bucket_name)

            print('\nCreating S3 bucket {0}.\n'.format(bucket_name))
            return self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.session.region_name
                }
            )

        except ClientError as err:
            if err.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print('{0} already exists. Continuing...'.format(bucket_name))
                return self.s3.Bucket(bucket_name)

            print('Unable to create bucket: {0}.'.format(bucket_name) + str(err))
            raise err


    def print_buckets(self):
        """Lists all S3 buckets"""
        for bucket in self.s3.buckets.all():
            print('s3://' + bucket.name)



    def print_objects(self, bucket_name):
        """Lists all objects in the given bucket"""
        try:
            for obj in self.s3.Bucket(bucket_name).objects.all():
                print(obj.key)

        except ClientError as err:
            print('Unable to list bucket: {0}. '.format(bucket_name) + str(err) + '\n')


    def setup_hosting_bucket(self, bucket_name):
        """Setup S3 bucket for website hosting"""
        try:
            bucket = self.create_bucket(bucket_name)
            set_bucket_policy(bucket)
            set_website_config(bucket)
            print('\nSuccess!')

        except ClientError:
            print('\nFailed to setup bucket {0}. '.format(bucket_name))


    def sync_to_bucket(self, path, bucket_name):
        """Sync path recursively to the given bucket"""
        bucket = self.s3.Bucket(bucket_name)
        root_path = Path(path).expanduser().resolve()

        def recursive_upload(bucket, target_path):
            """Uploads files recursively from root path to S3 bucket"""
            for path in target_path.iterdir():
                if path.is_dir():
                    recursive_upload(bucket, path)

                if path.is_file():
                    upload_file(bucket, str(path), str(path.relative_to(root_path)))

        try:
            print('\nBegin syncing {0} to bucket {1}...'.format(path, bucket_name))
            delete_objects(bucket)
            recursive_upload(bucket, root_path)
            print('\nSuccess!')

        except ClientError:
            print('\nFailed to sync path: {0} to bucket: {1}. '.format(path, bucket_name))