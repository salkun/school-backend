import uuid
from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

# ==========================================
# 1. ACADEMIC YEAR (Tahun Pelajaran)
# ==========================================
class AcademicYear(Base):
    __tablename__ = "academic_years"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_year = Column(Integer, nullable=False)  # e.g., 2023
    end_year = Column(Integer, nullable=False)    # e.g., 2024
    is_active = Column(Boolean, default=True, nullable=False)

    # Relasi ke Semester
    semesters = relationship("Semester", back_populates="academic_year", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ==========================================
# 2. SEMESTER
# ==========================================
class Semester(Base):
    __tablename__ = "semesters"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)     # e.g., "Odd" (Ganjil) / "Even" (Genap)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relasi balik
    academic_year = relationship("AcademicYear", back_populates="semesters")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ==========================================
# 3. BUILDING (Gedung)
# ==========================================
class Building(Base):
    __tablename__ = "buildings"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    established_year = Column(Integer, nullable=True) # Tahun Berdiri
    area = Column(Float, nullable=True)               # Luas
    width = Column(Float, nullable=True)              # Lebar
    height = Column(Float, nullable=True)             # Tinggi
    is_active = Column(Boolean, default=True, nullable=False)

    # Relasi ke Kelas
    classrooms = relationship("Classroom", back_populates="building", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ==========================================
# 4. CLASSROOM (Kelas)
# ==========================================
class Classroom(Base):
    __tablename__ = "classrooms"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    building_id = Column(UUID(as_uuid=True), ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    area = Column(Float, nullable=True)               # Luas
    width = Column(Float, nullable=True)              # Lebar
    height = Column(Float, nullable=True)             # Tinggi
    is_active = Column(Boolean, default=True, nullable=False)

    # Relasi balik
    building = relationship("Building", back_populates="classrooms")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# ==========================================
# 5. SUBJECT (Mata Pelajaran)
# ==========================================
class Subject(Base):
    __tablename__ = "subjects"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    lesson_hours = Column(Integer, nullable=False)    # Jam Pelajaran (JP)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)