import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


# ==========================================
# 1. TABEL PARENTS (DATA MASTER ORANG TUA)
# ==========================================
class Parent(Base):
    __tablename__ = "parents"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nik = Column(String(16), nullable=True)
    full_name = Column(String(100), nullable=False)
    place_of_birth = Column(String(50), nullable=True)
    birth_year = Column(String(4), nullable=True)
    education_code = Column(String(2), nullable=True)
    occupation_code = Column(String(2), nullable=True)
    income_code = Column(String(2), nullable=True)
    special_need_code = Column(String(2), nullable=True)
    address = Column(Text, nullable=True)
    phone_number = Column(String(20), nullable=True)
    whatsapp_number = Column(String(20), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relasi ke tabel pivot
    student_relations = relationship("StudentParentRelation", back_populates="parent", cascade="all, delete-orphan")


# ==========================================
# 2. TABEL PIVOT: STUDENT_PARENT_RELATIONS
# ==========================================
class StudentParentRelation(Base):
    __tablename__ = "student_parent_relations"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    
    # 1 = Ayah, 2 = Ibu, 3 = Wali (atau sesuai konvensi sekolahmu)
    relationship_type = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relasi balik
    student = relationship("app.models.student.Student", back_populates="student_parents")
    parent = relationship("Parent", back_populates="student_relations")