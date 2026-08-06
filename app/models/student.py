import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, Integer, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    nik = Column(String, unique=True, nullable=False)
    nisn = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relasi 1-to-1 ke tabel identity & address (cascade hapus otomatis jika student dihapus)
    identity = relationship("StudentIdentity", back_populates="student", uselist=False, cascade="all, delete-orphan")
    address = relationship("StudentAddress", back_populates="student", uselist=False, cascade="all, delete-orphan")


class StudentIdentity(Base):
    __tablename__ = "student_identities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), unique=True, nullable=False)
    gender = Column(String(1), nullable=False)  # 'M' atau 'F'
    religion = Column(String, nullable=False)
    family_card_number = Column(String, nullable=False)
    place_of_birth = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    birth_certificate_number = Column(String, nullable=True)
    nationality = Column(String, default="IDN")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="identity")


class StudentAddress(Base):
    __tablename__ = "student_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), unique=True, nullable=False)
    street_address = Column(Text, nullable=False)
    rt = Column(String(5), nullable=False)
    rw = Column(String(5), nullable=False)
    hamlet = Column(String, nullable=True)  # Dusun
    village = Column(String, nullable=False)  # Kelurahan/Desa
    district = Column(String, nullable=False)  # Kecamatan
    postal_code = Column(String(10), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    residence_type = Column(Integer, nullable=False)  # 1=Orang Tua, 2=Wali, 3=Kos, 4=Asrama, 5=Panti
    transportation_mode = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="address")