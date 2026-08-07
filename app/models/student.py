import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nik = Column(String(16), unique=True, index=True, nullable=False)
    nisn = Column(String(7), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relasi
    user = relationship("User", back_populates="students")
    identity = relationship("StudentIdentity", back_populates="student", uselist=False, cascade="all, delete-orphan")
    address = relationship("StudentAddress", back_populates="student", uselist=False, cascade="all, delete-orphan")
    parent = relationship("StudentParent", back_populates="student", uselist=False, cascade="all, delete-orphan")
    contact = relationship("StudentContact", back_populates="student", uselist=False, cascade="all, delete-orphan")
    # REVISI: Direname jadi student_parents
    student_parents = relationship("StudentParentRelation", back_populates="student", cascade="all, delete-orphan")
    # Tambahkan baris ini di dalam class Student:
    parent_relations = relationship("app.models.parent.StudentParentRelation", back_populates="student", cascade="all, delete-orphan")


class StudentIdentity(Base):
    __tablename__ = "student_identities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    family_card_number = Column(String(16), nullable=True)
    gender = Column(String(10), nullable=False)
    religion = Column(String(30), nullable=False)
    place_of_birth = Column(String(50), nullable=False)
    date_of_birth = Column(String(20), nullable=False)

    student = relationship("Student", back_populates="identity")


class StudentAddress(Base):
    __tablename__ = "student_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    street_address = Column(Text, nullable=False)
    rt = Column(String(5), nullable=False)
    rw = Column(String(5), nullable=False)
    village = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=True)
    residence_type = Column(String(50), nullable=True)
    
    # REVISI: String inputan biasa
    transportation_mode = Column(String(100), nullable=True)

    student = relationship("Student", back_populates="address")

class StudentContact(Base):
    __tablename__ = "student_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    phone_number = Column(String(20), nullable=True)     # No Telepon Rumah
    mobile_number = Column(String(20), nullable=True)    # No HP
    whatsapp_number = Column(String(20), nullable=True)  # No WA
    email = Column(String(100), nullable=True)           # Email

    student = relationship("Student", back_populates="contact")

# --- MODEL STUDENT PARENT ---
class StudentParent(Base):
    __tablename__ = "student_parents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    father_name = Column(String(100), nullable=True)
    father_job = Column(String(50), nullable=True)
    mother_name = Column(String(100), nullable=True)
    mother_job = Column(String(50), nullable=True)
    guardian_name = Column(String(100), nullable=True)
    guardian_job = Column(String(50), nullable=True)
    parent_phone = Column(String(20), nullable=True)

    student = relationship("Student", back_populates="parent")