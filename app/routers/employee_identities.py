from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.employee import EmployeeIdentity, Employee
from app.schemas.employee_identity import EmployeeIdentityCreate, EmployeeIdentityUpdate, EmployeeIdentityResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/employee-identities",
    tags=["Employee Identities"],
    dependencies=[Depends(require_admin)]  # Default kunci Admin
)

# 1. CREATE EMPLOYEE IDENTITY (POST)
@router.post("/", response_model=EmployeeIdentityResponse, status_code=status.HTTP_201_CREATED)
def create_employee_identity(data: EmployeeIdentityCreate, db: Session = Depends(get_db)):
    # Cek apakah Employee (Pegawai) ada
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Cek apakah pegawai tersebut sudah punya data identitas (Mencegah duplikasi One-to-One)
    existing_identity = db.query(EmployeeIdentity).filter(EmployeeIdentity.employee_id == data.employee_id).first()
    if existing_identity:
        raise HTTPException(status_code=400, detail="Identity for this employee already exists")

    new_identity = EmployeeIdentity(**data.model_dump())
    db.add(new_identity)
    db.commit()
    db.refresh(new_identity)
    return new_identity


# 2. GET ALL IDENTITIES (GET)
@router.get("/", response_model=List[EmployeeIdentityResponse], dependencies=[Depends(require_staff)])
def get_all_employee_identities(db: Session = Depends(get_db)):
    return db.query(EmployeeIdentity).all()


# 3. GET IDENTITY BY ID (GET)
@router.get("/{identity_id}", response_model=EmployeeIdentityResponse, dependencies=[Depends(require_staff)])
def get_identity_by_id(identity_id: UUID, db: Session = Depends(get_db)):
    identity = db.query(EmployeeIdentity).filter(EmployeeIdentity.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Employee identity not found")
    return identity


# 4. GET IDENTITY BY EMPLOYEE ID (GET) - Sangat berguna untuk di Frontend!
@router.get("/employee/{employee_id}", response_model=EmployeeIdentityResponse, dependencies=[Depends(require_staff)])
def get_identity_by_employee_id(employee_id: UUID, db: Session = Depends(get_db)):
    identity = db.query(EmployeeIdentity).filter(EmployeeIdentity.employee_id == employee_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Identity for this employee not found")
    return identity


# 5. UPDATE IDENTITY (PUT)
@router.put("/{identity_id}", response_model=EmployeeIdentityResponse)
def update_employee_identity(identity_id: UUID, data: EmployeeIdentityUpdate, db: Session = Depends(get_db)):
    identity = db.query(EmployeeIdentity).filter(EmployeeIdentity.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Employee identity not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(identity, key, value)

    db.commit()
    db.refresh(identity)
    return identity


# 6. DELETE IDENTITY (DELETE)
@router.delete("/{identity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_identity(identity_id: UUID, db: Session = Depends(get_db)):
    identity = db.query(EmployeeIdentity).filter(EmployeeIdentity.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Employee identity not found")

    db.delete(identity)
    db.commit()
    return None