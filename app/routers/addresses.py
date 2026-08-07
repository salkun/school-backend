from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.student import Student, StudentAddress
from app.schemas.student import StudentAddressCreate, StudentAddressResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/addresses",
    tags=["Student Addresses"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/{student_id}", response_model=StudentAddressResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_address(student_id: UUID, data: StudentAddressCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_address = db.query(StudentAddress).filter(StudentAddress.student_id == student_id).first()
    if existing_address:
        for key, value in data.model_dump().items():
            setattr(existing_address, key, value)
        db.commit()
        db.refresh(existing_address)
        return existing_address

    new_address = StudentAddress(student_id=student_id, **data.model_dump())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

@router.get("/{student_id}", response_model=StudentAddressResponse)
def get_address(student_id: UUID, db: Session = Depends(get_db)):
    address = db.query(StudentAddress).filter(StudentAddress.student_id == student_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found for this student")
    return address