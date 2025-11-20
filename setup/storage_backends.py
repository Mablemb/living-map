from storages.backends.s3boto3 import S3Boto3Storage
import os

# Uses environment variables defined in settings / .env
STATIC_LOCATION = os.getenv('AWS_STATIC_LOCATION', 'static')
MEDIA_LOCATION = os.getenv('AWS_MEDIA_LOCATION', 'media')

class StaticStorage(S3Boto3Storage):
    """Storage backend for collected static files on S3."""
    location = STATIC_LOCATION
    default_acl = (os.getenv('AWS_DEFAULT_ACL') or None)
    file_overwrite = True

class MediaStorage(S3Boto3Storage):
    """Storage backend for user-uploaded media (maps/images) on S3."""
    location = MEDIA_LOCATION
    default_acl = (os.getenv('AWS_DEFAULT_ACL') or None)
    file_overwrite = False  # keep user uploads distinct
