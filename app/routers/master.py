from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.dependencies import require_admin, require_staff

# Import Models & Schemas
from app.models.master import AcademicYear, Semester, Building, Classroom, Subject
from app.schemas.master import (
    AcademicYearCreate, AcademicYearResponse,
    SemesterCreate, SemesterResponse,
    BuildingCreate, BuildingResponse,
    ClassroomCreate, ClassroomResponse,
    SubjectCreate, SubjectResponse
)

router = APIRouter(
    prefix="/api/master",
    dependencies=[Depends(require_admin)]  # Kunci Global: Hanya Admin yang bisa memodifikasi Data Master
)

# ==========================================
# 1. ACADEMIC YEAR (Tahun Pelajaran)
# ==========================================
@router.post("/academic-years/", response_model=AcademicYearResponse, status_code=status.HTTP_201_CREATED, tags=["Master - Academic Year"])
def create_academic_year(data: AcademicYearCreate, db: Session = Depends(get_db)):
    new_data = AcademicYear(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/academic-years/", response_model=List[AcademicYearResponse], tags=["Master - Academic Year"])
def get_all_academic_years(db: Session = Depends(get_db)):
    return db.query(AcademicYear).all()

@router.put("/academic-years/{id}", response_model=AcademicYearResponse, tags=["Master - Academic Year"])
def update_academic_year(id: UUID, data: AcademicYearCreate, db: Session = Depends(get_db)):
    item = db.query(AcademicYear).filter(AcademicYear.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Academic Year not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/academic-years/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Master - Academic Year"])
def delete_academic_year(id: UUID, db: Session = Depends(get_db)):
    item = db.query(AcademicYear).filter(AcademicYear.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Academic Year not found")
    db.delete(item)
    db.commit()


# ==========================================
# 2. SEMESTER
# ==========================================
@router.post("/semesters/", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED, tags=["Master - Semester"])
def create_semester(data: SemesterCreate, db: Session = Depends(get_db)):
    new_data = Semester(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/semesters/", response_model=List[SemesterResponse], tags=["Master - Semester"])
def get_all_semesters(db: Session = Depends(get_db)):
    return db.query(Semester).all()

@router.put("/semesters/{id}", response_model=SemesterResponse, tags=["Master - Semester"])
def update_semester(id: UUID, data: SemesterCreate, db: Session = Depends(get_db)):
    item = db.query(Semester).filter(Semester.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Semester not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/semesters/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Master - Semester"])
def delete_semester(id: UUID, db: Session = Depends(get_db)):
    item = db.query(Semester).filter(Semester.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Semester not found")
    db.delete(item)
    db.commit()


# ==========================================
# 3. BUILDING (Gedung)
# ==========================================
@router.post("/buildings/", response_model=BuildingResponse, status_code=status.HTTP_201_CREATED, tags=["Master - Building"])
def create_building(data: BuildingCreate, db: Session = Depends(get_db)):
    new_data = Building(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/buildings/", response_model=List[BuildingResponse], tags=["Master - Building"])
def get_all_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()

@router.put("/buildings/{id}", response_model=BuildingResponse, tags=["Master - Building"])
def update_building(id: UUID, data: BuildingCreate, db: Session = Depends(get_db)):
    item = db.query(Building).filter(Building.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Building not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/buildings/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Master - Building"])
def delete_building(id: UUID, db: Session = Depends(get_db)):
    item = db.query(Building).filter(Building.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Building not found")
    db.delete(item)
    db.commit()


# ==========================================
# 4. CLASSROOM (Kelas)
# ==========================================
@router.post("/classrooms/", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED, tags=["Master - Classroom"])
def create_classroom(data: ClassroomCreate, db: Session = Depends(get_db)):
    new_data = Classroom(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/classrooms/", response_model=List[ClassroomResponse], tags=["Master - Classroom"])
def get_all_classrooms(db: Session = Depends(get_db)):
    return db.query(Classroom).all()

@router.put("/classrooms/{id}", response_model=ClassroomResponse, tags=["Master - Classroom"])
def update_classroom(id: UUID, data: ClassroomCreate, db: Session = Depends(get_db)):
    item = db.query(Classroom).filter(Classroom.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Classroom not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/classrooms/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Master - Classroom"])
def delete_classroom(id: UUID, db: Session = Depends(get_db)):
    item = db.query(Classroom).filter(Classroom.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Classroom not found")
    db.delete(item)
    db.commit()


# ==========================================
# 5. SUBJECT (Mata Pelajaran)
# ==========================================
@router.post("/subjects/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED, tags=["Master - Subject"])
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    new_data = Subject(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

@router.get("/subjects/", response_model=List[SubjectResponse], tags=["Master - Subject"])
def get_all_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.put("/subjects/{id}", response_model=SubjectResponse, tags=["Master - Subject"])
def update_subject(id: UUID, data: SubjectCreate, db: Session = Depends(get_db)):
    item = db.query(Subject).filter(Subject.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/subjects/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Master - Subject"])
def delete_subject(id: UUID, db: Session = Depends(get_db)):
    item = db.query(Subject).filter(Subject.id == id).first()
    if not item: raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(item)
    db.commit()