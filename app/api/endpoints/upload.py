"""File upload REST endpoint (multipart form data to MinIO)"""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.security import get_current_active_user
from app.models.user import User
from app.s3 import upload_file, ensure_bucket

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def upload(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    """Upload a file to S3 and return its URL"""
    ensure_bucket()
    data = file.file.read()
    url = upload_file(data, file.filename or "file.bin", file.content_type or "application/octet-stream")
    return {"url": url}
