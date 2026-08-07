from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.school import SchoolIdentity
from app.schemas.school import SchoolIdentityCreate, SchoolIdentityResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/schools",
    tags=["School Identity"]
)

# 1. CREATE OR UPDATE SCHOOL IDENTITY (Admin Only)
@router.post(
    "/",
    response_model=SchoolIdentityResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
def create_or_update_school_identity(
    data: SchoolIdentityCreate,
    db: Session = Depends(get_db)
):
    # Check if a school identity already exists
    existing_school = db.query(SchoolIdentity).first()

    if existing_school:
        for key, value in data.model_dump().items():
            setattr(existing_school, key, value)
        db.commit()
        db.refresh(existing_school)
        return existing_school
    else:
        new_school = SchoolIdentity(**data.model_dump())
        db.add(new_school)
        db.commit()
        db.refresh(new_school)
        return new_school


# 2. GET SCHOOL IDENTITY (Staff & Admin)
@router.get(
    "/",
    response_model=SchoolIdentityResponse,
    dependencies=[Depends(require_staff)]
)
def get_school_identity(db: Session = Depends(get_db)):
    school = db.query(SchoolIdentity).first()
    if not school:
        raise HTTPException(status_code=404, detail="School identity not found")
    return school