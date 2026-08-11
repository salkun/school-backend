from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.employee import EmployeeContact, Employee
from app.schemas.employee_contact import EmployeeContactCreate, EmployeeContactUpdate, EmployeeContactResponse
from app.dependencies import require_admin, require_staff

router = APIRouter(
    prefix="/api/employee-contacts",
    tags=["Employee Contacts"],
    dependencies=[Depends(require_admin)]
)

@router.post("/", response_model=EmployeeContactResponse, status_code=status.HTTP_201_CREATED)
def create_employee_contact(data: EmployeeContactCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_contact = EmployeeContact(**data.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.get("/", response_model=List[EmployeeContactResponse], dependencies=[Depends(require_staff)])
def get_all_employee_contacts(db: Session = Depends(get_db)):
    return db.query(EmployeeContact).all()

@router.get("/{contact_id}", response_model=EmployeeContactResponse, dependencies=[Depends(require_staff)])
def get_contact_by_id(contact_id: UUID, db: Session = Depends(get_db)):
    contact = db.query(EmployeeContact).filter(EmployeeContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Employee contact not found")
    return contact

# Mengambil semua kontak milik satu pegawai (One-to-Many)
@router.get("/employee/{employee_id}", response_model=List[EmployeeContactResponse], dependencies=[Depends(require_staff)])
def get_contacts_by_employee_id(employee_id: UUID, db: Session = Depends(get_db)):
    contacts = db.query(EmployeeContact).filter(EmployeeContact.employee_id == employee_id).all()
    return contacts

@router.put("/{contact_id}", response_model=EmployeeContactResponse)
def update_employee_contact(contact_id: UUID, data: EmployeeContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(EmployeeContact).filter(EmployeeContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Employee contact not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_contact(contact_id: UUID, db: Session = Depends(get_db)):
    contact = db.query(EmployeeContact).filter(EmployeeContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Employee contact not found")

    db.delete(contact)
    db.commit()
    return None