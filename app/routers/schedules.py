from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.master import TeachingSchedule, HomeroomAssignment
from app.schemas.master import TeachingScheduleCreate, TeachingScheduleResponse, HomeroomAssignmentCreate, HomeroomAssignmentResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/schedules",
    tags=["Teaching & Homeroom Schedules"],
    dependencies=[Depends(require_admin)]
)

# --- 1. Teaching Schedule ---
@router.post("/teaching/", response_model=TeachingScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_teaching_schedule(data: TeachingScheduleCreate, db: Session = Depends(get_db)):
    new_sched = TeachingSchedule(**data.model_dump())
    db.add(new_sched)
    db.commit()
    db.refresh(new_sched)
    return new_sched

@router.get("/teaching/employee/{employee_id}", response_model=List[TeachingScheduleResponse], dependencies=[Depends(require_staff)])
def get_teaching_schedules_by_employee(employee_id: UUID, db: Session = Depends(get_db)):
    return db.query(TeachingSchedule).filter(TeachingSchedule.employee_id == employee_id).all()

# --- 2. Homeroom Assignment ---
@router.post("/homeroom/", response_model=HomeroomAssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_homeroom(data: HomeroomAssignmentCreate, db: Session = Depends(get_db)):
    new_assign = HomeroomAssignment(**data.model_dump())
    db.add(new_assign)
    db.commit()
    db.refresh(new_assign)
    return new_assign

@router.get("/homeroom/classroom/{classroom_id}", response_model=List[HomeroomAssignmentResponse], dependencies=[Depends(require_staff)])
def get_homeroom_history(classroom_id: UUID, db: Session = Depends(get_db)):
    return db.query(HomeroomAssignment).filter(HomeroomAssignment.classroom_id == classroom_id).all()
