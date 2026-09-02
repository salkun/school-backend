import uuid
from sqlalchemy import Column, String, Text, BigInteger, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ==========================================
# 1. ANNOUNCEMENTS (Pengumuman Sekolah & Kelas)
# ==========================================
class Announcement(Base):
    __tablename__ = "announcements"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("school_identities.id", ondelete="SET NULL"), nullable=True)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=True) # Null jika untuk seluruh sekolah

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default="normal", nullable=False) # low, normal, high, urgent
    target_role = Column(String(20), default="all", nullable=False) # all, teacher, student, parent

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    author = relationship("User")
    school = relationship("SchoolIdentity")
    classroom = relationship("Classroom")


# ==========================================
# 2. MEDIA FILES (Manajemen Berkas Unggahan)
# ==========================================
class MediaFile(Base):
    __tablename__ = "media_files"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    original_name = Column(String(255), nullable=False)
    stored_path = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False) # Bytes
    category = Column(String(50), nullable=False) # avatar, material, assignment, submission, document

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    uploader = relationship("User")


# ==========================================
# 3. ACTIVITY LOGS (Audit Log Sistem)
# ==========================================
class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    activity = Column(String(255), nullable=False) # LOGIN, UPDATE_GRADE, DELETE_USER, etc.
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User")


# ==========================================
# 4. SYSTEM SETTINGS (Konfigurasi Dinamis)
# ==========================================
class SystemSetting(Base):
    __tablename__ = "system_settings"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
