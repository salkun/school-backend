from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.master import Position
from app.models.employee import EmployeePosition, Employee
from app.schemas.master import PositionCreate, PositionUpdate, PositionResponse
from app.schemas.employee import EmployeePositionCreate, EmployeePositionUpdate, EmployeePositionResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/positions",
    tags=["Positions & Employee Roles"]
)

# ==========================================================
# 1. MASTER POSITION (JABATAN) CRUD
# ==========================================================
@router.post("/", response_model=PositionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_position(data: PositionCreate, db: Session = Depends(get_db)):
    new_pos = Position(**data.model_dump())
    db.add(new_pos)
    db.commit()
    db.refresh(new_pos)
    return new_pos

@router.get("/", response_model=List[PositionResponse], dependencies=[Depends(require_staff)])
def get_all_positions(db: Session = Depends(get_db)):
    return db.query(Position).order_by(Position.name.asc()).all()

@router.get("/{position_id}", response_model=PositionResponse, dependencies=[Depends(require_staff)])
def get_position_detail(position_id: UUID, db: Session = Depends(get_db)):
    pos = db.query(Position).filter(Position.id == position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Jabatan tidak ditemukan")
    return pos

@router.put("/{position_id}", response_model=PositionResponse, dependencies=[Depends(require_admin)])
def update_position(position_id: UUID, data: PositionUpdate, db: Session = Depends(get_db)):
    pos = db.query(Position).filter(Position.id == position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Jabatan tidak ditemukan")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pos, key, value)
    
    db.commit()
    db.refresh(pos)
    return pos

@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_position(position_id: UUID, db: Session = Depends(get_db)):
    pos = db.query(Position).filter(Position.id == position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Jabatan tidak ditemukan")
    
    db.delete(pos)
    db.commit()
    return None


# ==========================================================
# 2. EMPLOYEE POSITIONS (RIWAYAT JABATAN PEGAWAI) CRUD
# ==========================================================
@router.post("/employee/", response_model=EmployeePositionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def assign_employee_position(data: EmployeePositionCreate, db: Session = Depends(get_db)):
    # Validate employee
    if not db.query(Employee).filter(Employee.id == data.employee_id).first():
        raise HTTPException(status_code=404, detail="Employee not found")
    # Validate position
    if not db.query(Position).filter(Position.id == data.position_id).first():
        raise HTTPException(status_code=404, detail="Position not found")
    
    new_assign = EmployeePosition(**data.model_dump())
    db.add(new_assign)
    db.commit()
    db.refresh(new_assign)
    return new_assign

@router.get("/employee/{employee_id}", response_model=List[EmployeePositionResponse], dependencies=[Depends(require_staff)])
def get_employee_positions(employee_id: UUID, db: Session = Depends(get_db)):
    return db.query(EmployeePosition).filter(EmployeePosition.employee_id == employee_id).all()

@router.put("/employee/{assign_id}", response_model=EmployeePositionResponse, dependencies=[Depends(require_admin)])
def update_employee_position(assign_id: UUID, data: EmployeePositionUpdate, db: Session = Depends(get_db)):
    assign = db.query(EmployeePosition).filter(EmployeePosition.id == assign_id).first()
    if not assign:
        raise HTTPException(status_code=404, detail="Penugasan jabatan tidak ditemukan")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(assign, key, value)
    
    db.commit()
    db.refresh(assign)
    return assign

@router.delete("/employee/{assign_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_employee_position(assign_id: UUID, db: Session = Depends(get_db)):
    assign = db.query(EmployeePosition).filter(EmployeePosition.id == assign_id).first()
    if not assign:
        raise HTTPException(status_code=404, detail="Penugasan jabatan tidak ditemukan")
    
    db.delete(assign)
    db.commit()
    return None
