# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app.database import engine, Base

# 1. IMPORT SEMUA ROUTER (Termasuk auth, users, dan schools)
from app.routers import (
    addresses, 
    auth, 
    schools,
    master,
    contacts, 
    identities, 
    students, 
    parents, 
    users,
    employees,
    employee_identities,
    employee_contacts,
    employee_children,
    employee_subjects,
    enrollments,
    positions,
    schedules
)

# Generate tabel otomatis ke database PostgreSQL di Laragon
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIAKAD API",
    description="Backend API untuk Sistem Master Data Sekolah (FastAPI + PostgreSQL)",
    version="1.0.0"
)

# 2. DAFTARKAN SEMUA ROUTER
app.include_router(auth.router)
app.include_router(users.router) 
app.include_router(schools.router)  
app.include_router(master.router)
app.include_router(students.router)
app.include_router(parents.router)
app.include_router(contacts.router)
app.include_router(identities.router)
app.include_router(addresses.router)
app.include_router(employees.router)
app.include_router(employee_identities.router) 
app.include_router(employee_contacts.router) 
app.include_router(employee_children.router)
app.include_router(employee_subjects.router)
app.include_router(enrollments.router)
app.include_router(positions.router)
app.include_router(schedules.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to School Master Data API",
        "docs_url": "http://127.0.0.1:8000/docs"
    }