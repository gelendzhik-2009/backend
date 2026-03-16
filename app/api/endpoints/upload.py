"""File upload REST endpoint (multipart form data to MinIO)"""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.security import get_current_active_user
from app.models.user import User
from app.s3 import upload_file, ensure_bucket

router = APIRouter(prefix="/upload", tags=["upload"])

MAX_UPLOAD_SIZE = 10 * 1024 * 1024


@router.post("/", status_code=status.HTTP_201_CREATED)
def upload(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    """Upload a file to S3 and return its URL"""
    ensure_bucket()
    file.file.seek(0, 2)
    size = file.file.tell()
    if size > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large (max 10 MB)")
    file.file.seek(0)
    data = file.file.read()
    result = upload_file(data, file.filename or "file.bin", file.content_type or "application/octet-stream")
    return {"url": result["url"], "object_name": result["object_name"]}
