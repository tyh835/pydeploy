"""Core S3 functionalities for PyJam"""

import mimetypes
from botocore.exceptions import ClientError


def set_bucket_policy(bucket):
    """Configures bucket policy to allow public reads"""
    policy = '''
    {
        "Version":"2012-10-17",
        "Statement":[
            {
                "Sid":"PublicReadGetObject",
                "Effect":"Allow",
                "Principal": "*",
                "Action":["s3:GetObject"],
                "Resource":["arn:aws:s3:::%s/*"]
            }
        ]
    }
    ''' % bucket.name

    policy = policy.strip()

    try:
        print('Applying public read permissions to {0}...'.format(bucket.name))
        return bucket.Policy().put(Policy=policy)

    except ClientError as err:
        print('Unable to apply bucket policy to {0}. '.format(bucket.name) + str(err) + '\n')
        raise err


def set_website_config(bucket):
    """Configures bucket for static site hosting"""
    try:
        print('Applying static site configurations to {0}...'.format(bucket.name))
        return bucket.Website().put(WebsiteConfiguration={
            "ErrorDocument": {
                "Key": "error.html"
            },
            "IndexDocument": {
                "Suffix": "index.html"
            }
        })

    except ClientError as err:
        print('Unable to apply bucket policy to {0}. '.format(bucket.name) + str(err)+ '\n')
        raise err


def delete_objects(bucket):
    """Deletes all object in bucket"""
    try:
        for obj in bucket.objects.all():
            print('Deleting {0} from {1}.'.format(obj.key, bucket.name))
            obj.delete()

    except ClientError as err:
        print('Unable to delete object in {0}. '.format(bucket.name) + str(err) + '\n')


def upload_file(bucket, file_path, key):
    """Uploads file to S3 bucket"""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'

    try:
        print('Uploading {0} to {1} (content-type: {2}).'.format(key, bucket.name, content_type))
        bucket.upload_file(
            file_path,
            key,
            ExtraArgs={
                'ContentType': content_type
            }
        )

    except ClientError as err:
        print('Unable to upload file: {0} to {1}. '.format(file_path, bucket.name) + str(err))
        raise err