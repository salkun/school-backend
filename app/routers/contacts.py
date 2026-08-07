from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.student import Student, StudentContact
from app.schemas.student import StudentContactCreate, StudentContactResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/contacts",
    tags=["Student Contacts"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/{student_id}", response_model=StudentContactResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_contact(student_id: UUID, data: StudentContactCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_contact = db.query(StudentContact).filter(StudentContact.student_id == student_id).first()
    if existing_contact:
        for key, value in data.model_dump().items():
            setattr(existing_contact, key, value)
        db.commit()
        db.refresh(existing_contact)
        return existing_contact

    new_contact = StudentContact(student_id=student_id, **data.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.get("/{student_id}", response_model=StudentContactResponse)
def get_contact(student_id: UUID, db: Session = Depends(get_db)):
    contact = db.query(StudentContact).filter(StudentContact.student_id == student_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found for this student")
    return contact