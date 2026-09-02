import os
import uuid
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.communication import MediaFile
from app.schemas.communication import MediaFileResponse
from app.dependencies import get_current_user, require_all

router = APIRouter(
    prefix="/api/uploads",
    tags=["Uploads & Media Management"]
)

UPLOAD_DIR = "uploads"
os.makedirs(f"{UPLOAD_DIR}/avatars", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/documents", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/materials", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/submissions", exist_ok=True)

def save_upload_file(upload_file: UploadFile, subfolder: str) -> str:
    ext = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, subfolder, unique_filename)
    
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return f"/{UPLOAD_DIR}/{subfolder}/{unique_filename}".replace("\\", "/")

@router.post("/avatar", response_model=MediaFileResponse, dependencies=[Depends(require_all)])
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar (JPG, PNG, WebP)")
        
    saved_url = save_upload_file(file, "avatars")
    
    # Hitung size
    file_size = 0
    try:
        file_size = os.path.getsize(saved_url.lstrip("/"))
    except Exception:
        pass

    media = MediaFile(
        uploaded_by=current_user.id,
        original_name=file.filename,
        stored_path=saved_url,
        mime_type=file.content_type,
        file_size=file_size,
        category="avatar"
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media

@router.post("/document", response_model=MediaFileResponse, dependencies=[Depends(require_all)])
async def upload_document(
    file: UploadFile = File(...),
    category: str = "document",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subfolder = "documents"
    if category in ["material", "assignment", "submission"]:
        subfolder = category + "s"

    saved_url = save_upload_file(file, subfolder)
    
    file_size = 0
    try:
        file_size = os.path.getsize(saved_url.lstrip("/"))
    except Exception:
        pass

    media = MediaFile(
        uploaded_by=current_user.id,
        original_name=file.filename,
        stored_path=saved_url,
        mime_type=file.content_type or "application/octet-stream",
        file_size=file_size,
        category=category
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media
