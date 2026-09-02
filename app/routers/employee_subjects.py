from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.employee import Employee
from app.models.master import Subject
from app.schemas.master import SubjectResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/employees",
    tags=["Employee Subjects"],
    dependencies=[Depends(require_admin)]
)

@router.post("/{employee_id}/subjects/{subject_id}", status_code=status.HTTP_201_CREATED)
def assign_subject(employee_id: UUID, subject_id: UUID, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    if subject in employee.subjects:
        raise HTTPException(status_code=400, detail="Subject already assigned")

    employee.subjects.append(subject)
    db.commit()
    return {"detail": "Subject assigned"}

@router.delete("/{employee_id}/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassign_subject(employee_id: UUID, subject_id: UUID, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject or subject not in employee.subjects:
        raise HTTPException(status_code=404, detail="Subject not assigned to this employee")

    employee.subjects.remove(subject)
    db.commit()

@router.get("/{employee_id}/subjects", response_model=List[SubjectResponse], dependencies=[Depends(require_staff)])
def get_employee_subjects(employee_id: UUID, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.subjects
