from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.employee import EmployeeChild, Employee
from app.schemas.employee_child import EmployeeChildCreate, EmployeeChildUpdate, EmployeeChildResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/employee-children",
    tags=["Employee Children"],
    dependencies=[Depends(require_admin)]
)

@router.post("/", response_model=EmployeeChildResponse, status_code=status.HTTP_201_CREATED)
def create_employee_child(data: EmployeeChildCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_child = EmployeeChild(**data.model_dump())
    db.add(new_child)
    db.commit()
    db.refresh(new_child)
    return new_child

@router.get("/", response_model=List[EmployeeChildResponse], dependencies=[Depends(require_staff)])
def get_all_employee_children(db: Session = Depends(get_db)):
    return db.query(EmployeeChild).all()

@router.get("/{child_id}", response_model=EmployeeChildResponse, dependencies=[Depends(require_staff)])
def get_child_by_id(child_id: UUID, db: Session = Depends(get_db)):
    child = db.query(EmployeeChild).filter(EmployeeChild.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Employee child not found")
    return child

# Ambil daftar anak berdasarkan ID Pegawai (Berguna untuk Profil Pegawai di Frontend)
@router.get("/employee/{employee_id}", response_model=List[EmployeeChildResponse], dependencies=[Depends(require_staff)])
def get_children_by_employee_id(employee_id: UUID, db: Session = Depends(get_db)):
    children = db.query(EmployeeChild).filter(EmployeeChild.employee_id == employee_id).all()
    return children

@router.put("/{child_id}", response_model=EmployeeChildResponse)
def update_employee_child(child_id: UUID, data: EmployeeChildUpdate, db: Session = Depends(get_db)):
    child = db.query(EmployeeChild).filter(EmployeeChild.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Employee child not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(child, key, value)

    db.commit()
    db.refresh(child)
    return child

@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_child(child_id: UUID, db: Session = Depends(get_db)):
    child = db.query(EmployeeChild).filter(EmployeeChild.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Employee child not found")

    db.delete(child)
    db.commit()
    return None