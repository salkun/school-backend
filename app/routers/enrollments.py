from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.student import StudentEnrollment, Student
from app.schemas.student import StudentEnrollmentCreate, StudentEnrollmentResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/enrollments",
    tags=["Student Enrollments"],
    dependencies=[Depends(require_admin)]
)

@router.post("/", response_model=StudentEnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: StudentEnrollmentCreate, db: Session = Depends(get_db)):
    if not db.query(Student).filter(Student.id == data.student_id).first():
        raise HTTPException(status_code=404, detail="Student not found")
        
    new_enrollment = StudentEnrollment(**data.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

@router.get("/", response_model=List[StudentEnrollmentResponse], dependencies=[Depends(require_staff)])
def get_all_enrollments(db: Session = Depends(get_db)):
    return db.query(StudentEnrollment).all()

@router.get("/student/{student_id}", response_model=List[StudentEnrollmentResponse], dependencies=[Depends(require_staff)])
def get_student_enrollments(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(StudentEnrollment).filter(StudentEnrollment.student_id == student_id).all()

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: UUID, db: Session = Depends(get_db)):
    enrollment = db.query(StudentEnrollment).filter(StudentEnrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return None
