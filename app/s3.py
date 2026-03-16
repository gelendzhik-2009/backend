"""MinIO S3 client for file storage"""

import uuid
from io import BytesIO
from minio import Minio
from minio.error import S3Error
from app.config import settings

_client = None


def get_s3_client() -> Minio:
    """Get or create singleton MinIO client"""
    global _client
    if _client is None:
        _client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
    return _client


def ensure_bucket() -> None:
    """Create the default bucket if it does not exist"""
    client = get_s3_client()
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)


def upload_file(file_data: bytes, original_filename: str, content_type: str) -> dict:
    """Upload file to MinIO, return dict with object_name and url"""
    client = get_s3_client()
    ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "bin"
    object_name = f"{uuid.uuid4().hex}.{ext}"
    client.put_object(
        settings.MINIO_BUCKET,
        object_name,
        BytesIO(file_data),
        length=len(file_data),
        content_type=content_type,
    )
    if settings.MINIO_PUBLIC_URL:
        url = f"{settings.MINIO_PUBLIC_URL.rstrip('/')}/{settings.MINIO_BUCKET}/{object_name}"
    else:
        scheme = "https" if settings.MINIO_SECURE else "http"
        url = f"{scheme}://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{object_name}"
    return {"object_name": object_name, "url": url}


def delete_file(object_name_or_url: str) -> bool:
    """Delete file from MinIO by object name or full URL"""
    client = get_s3_client()
    key = object_name_or_url
    bucket_prefix = f"/{settings.MINIO_BUCKET}/"
    if bucket_prefix in key:
        key = key.split(bucket_prefix, 1)[1]
    try:
        client.remove_object(settings.MINIO_BUCKET, key)
        return True
    except S3Error:
        return False
