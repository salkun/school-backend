import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import app.models # Register all models in Base.metadata
from app.database import engine, Base

# Import semua router
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
    schedules,
    backup,
    lms,
    academics,
    attendance,
    announcements,
    uploads,
    profile,
    dashboard,
    ppdb
)

# Generate / sinkronisasi tabel otomatis ke database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend API Sistem Informasi Akademik (SIAKAD)",
    description="Backend API untuk Sistem Informasi Akademik (SIAKAD) Sekolah (FastAPI + PostgreSQL)",
    version="2.0.0"
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ganti domain frontend spesifik saat production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Static Files untuk upload berkas
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 3. Daftarkan Semua Router
app.include_router(auth.router)
app.include_router(users.router) 
app.include_router(profile.router)
app.include_router(dashboard.router)
app.include_router(schools.router)  
app.include_router(master.router)
app.include_router(positions.router)
app.include_router(schedules.router)
app.include_router(enrollments.router)
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

# --- Router Modul Tambahan Baru ---
app.include_router(lms.router)
app.include_router(academics.router)
app.include_router(attendance.router)
app.include_router(announcements.router)
app.include_router(uploads.router)
app.include_router(backup.router)
app.include_router(ppdb.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to EduSphere SIAKAD & LMS API",
        "version": "2.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }