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
    school_id = Column(UUID(as_uuid=True), ForeignKey("school_identities.id", ondelete="SET NULL"), nullable=True)
    nik = Column(String(16), unique=True, index=True, nullable=False)
    nisn = Column(String(7), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relasi
    user = relationship("User", back_populates="students")
    school = relationship("SchoolIdentity", back_populates="students")
    identity = relationship("StudentIdentity", back_populates="student", uselist=False, cascade="all, delete-orphan")
    address = relationship("StudentAddress", back_populates="student", uselist=False, cascade="all, delete-orphan")
    parent = relationship("StudentParent", back_populates="student", uselist=False, cascade="all, delete-orphan")
    contact = relationship("StudentContact", back_populates="student", uselist=False, cascade="all, delete-orphan")
    student_parents = relationship("StudentParentRelation", back_populates="student", cascade="all, delete-orphan")
    enrollments = relationship("StudentEnrollment", back_populates="student", cascade="all, delete-orphan")

class StudentIdentity(Base):
    __tablename__ = "student_identities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    gender = Column(String(20), nullable=False)
    religion = Column(String(30), nullable=False)
    family_card_number = Column(String(16), nullable=True)
    place_of_birth = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    birth_certificate_number = Column(String(50), nullable=True)
    nationality = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="identity")


class StudentAddress(Base):
    __tablename__ = "student_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    street_address = Column(Text, nullable=False)
    rt = Column(String(5), nullable=False)
    rw = Column(String(5), nullable=False)
    hamlet = Column(String(100), nullable=True)
    village = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=True)
    residence_type = Column(String(50), nullable=True)
    transportation_mode = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

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

class StudentEnrollment(Base):
    __tablename__ = "student_enrollments"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Active", nullable=False) # e.g., "Active", "Moved", "Graduated"

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    classroom = relationship("Classroom")
    academic_year = relationship("AcademicYear")
    semester = relationship("Semester")