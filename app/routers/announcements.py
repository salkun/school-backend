from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.communication import Announcement
from app.schemas.communication import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from app.dependencies import get_current_user, require_admin, require_staff, require_all

router = APIRouter(
    prefix="/api/announcements",
    tags=["Announcements & Pengumuman"]
)

@router.post("/", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_staff)])
def create_announcement(data: AnnouncementCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    school_id = data.school_id or current_user.school_id
    new_announcement = Announcement(
        **data.model_dump(exclude={"school_id"}),
        user_id=current_user.id,
        school_id=school_id
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

@router.get("/", response_model=List[AnnouncementResponse], dependencies=[Depends(require_all)])
def get_announcements(
    classroom_id: Optional[UUID] = None,
    target_role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Announcement)
    if classroom_id:
        query = query.filter((Announcement.classroom_id == classroom_id) | (Announcement.classroom_id.is_(None)))
    if target_role and target_role != "all":
        query = query.filter((Announcement.target_role == target_role) | (Announcement.target_role == "all"))
    return query.order_by(Announcement.created_at.desc()).all()

@router.get("/{announcement_id}", response_model=AnnouncementResponse, dependencies=[Depends(require_all)])
def get_announcement_detail(announcement_id: UUID, db: Session = Depends(get_db)):
    item = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return item

@router.put("/{announcement_id}", response_model=AnnouncementResponse, dependencies=[Depends(require_staff)])
def update_announcement(announcement_id: UUID, data: AnnouncementUpdate, db: Session = Depends(get_db)):
    item = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_staff)])
def delete_announcement(announcement_id: UUID, db: Session = Depends(get_db)):
    item = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(item)
    db.commit()
    return None
