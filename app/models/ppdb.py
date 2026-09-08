import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PPDBAccount(Base):
    __tablename__ = "ppdb_accounts"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nik = Column(String(16), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relasi 1-to-1 ke Staging Registrasi
    registration = relationship("PPDBRegistration", back_populates="account", uselist=False, cascade="all, delete-orphan")


class PPDBRegistration(Base):
    __tablename__ = "ppdb_registrations"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("ppdb_accounts.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Status Pembayaran: unpaid, pending_verification, paid, rejected
    payment_status = Column(String(30), default="unpaid", nullable=False)
    payment_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    payment_proof_path = Column(String(500), nullable=True)
    payment_verified_at = Column(DateTime(timezone=True), nullable=True)
    payment_verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Status Pendaftaran Seleksi: pending, accepted, rejected
    registration_status = Column(String(30), default="pending", nullable=False)

    # Seluruh data form pendaftaran bertingkat disimpan dalam format JSONB
    form_data = Column(JSONB, nullable=True)

    # Relasi ke student setelah proses accept / migrasi berhasil
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    account = relationship("PPDBAccount", back_populates="registration")
    verifier = relationship("User")
    student = relationship("Student")
