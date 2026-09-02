from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.master import Position
from app.models.employee import EmployeePosition, Employee
from app.schemas.master import PositionCreate, PositionResponse
from app.schemas.employee import EmployeePositionCreate, EmployeePositionResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/positions",
    tags=["Positions & Employee Roles"],
    dependencies=[Depends(require_admin)]
)

# --- 1. Master Position ---
@router.post("/", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
def create_position(data: PositionCreate, db: Session = Depends(get_db)):
    new_pos = Position(**data.model_dump())
    db.add(new_pos)
    db.commit()
    db.refresh(new_pos)
    return new_pos

@router.get("/", response_model=List[PositionResponse], dependencies=[Depends(require_staff)])
def get_all_positions(db: Session = Depends(get_db)):
    return db.query(Position).all()

# --- 2. Employee Positions (Riwayat Jabatan) ---
@router.post("/employee/", response_model=EmployeePositionResponse, status_code=status.HTTP_201_CREATED)
def assign_employee_position(data: EmployeePositionCreate, db: Session = Depends(get_db)):
    # Validate employee
    if not db.query(Employee).filter(Employee.id == data.employee_id).first():
        raise HTTPException(status_code=404, detail="Employee not found")
    
    new_assign = EmployeePosition(**data.model_dump())
    db.add(new_assign)
    db.commit()
    db.refresh(new_assign)
    return new_assign

@router.get("/employee/{employee_id}", response_model=List[EmployeePositionResponse], dependencies=[Depends(require_staff)])
def get_employee_positions(employee_id: UUID, db: Session = Depends(get_db)):
    return db.query(EmployeePosition).filter(EmployeePosition.employee_id == employee_id).all()
