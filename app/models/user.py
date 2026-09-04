import uuid
from enum import Enum
from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


# --- 1. ENUM ROLE STANDAR SEKOLAH ---
class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    EMPLOYEE = "employee"
    STAFF = "staff"
    STUDENT = "student"
    PARENT = "parent"


# --- 2. CLASS USER UTAMA ---
class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)  # Set nullable=True kalau boleh kosong
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Gunakan default value string "admin" atau yang lain
    role = Column(String(20), default=UserRole.ADMIN.value, nullable=False)
    school_id = Column(UUID(as_uuid=True), ForeignKey("school_identities.id", ondelete="SET NULL"), nullable=True)
    school = relationship("SchoolIdentity", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relasi balik ke Student
    students = relationship("app.models.student.Student", back_populates="user", cascade="all, delete-orphan")