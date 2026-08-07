import uuid
from sqlalchemy import Column, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {'extend_existing': True}

    # 1. Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 2. Foreign Keys (Relations)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("school_identities.id", ondelete="SET NULL"), nullable=True)

    # 3. Personal Identity (Identitas Pribadi)
    full_name = Column(String(100), nullable=False)
    nik = Column(String(16), unique=True, index=True, nullable=False)
    gender = Column(String(20), nullable=False)               # "Male" / "Female" (atau "Laki-laki" / "Perempuan")
    place_of_birth = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)              # Format: YYYY-MM-DD
    mother_maiden_name = Column(String(100), nullable=False)  # Nama Ibu Kandung

    # 4. Professional Identifiers (Nomor Induk Kepegawaian)
    nip = Column(String(30), unique=True, index=True, nullable=True)    # NIP (PNS)
    niy = Column(String(30), unique=True, index=True, nullable=True)    # NIY / NIGK (Yayasan)
    nuptk = Column(String(20), unique=True, index=True, nullable=True)  # NUPTK

    # 5. Employment Details (Data Kepegawaian)
    employment_status = Column(String(50), nullable=False)       # e.g., "PNS", "GTY", "Honorer Sekolah"
    ptk_type = Column(String(50), nullable=False)                # e.g., "Guru Mapel", "Wali Kelas", "Tenaga Administrasi"
    appointment_decree = Column(String(100), nullable=True)      # SK Pengangkatan
    appointment_start_date = Column(Date, nullable=True)         # TMT Pengangkatan
    appointing_institution = Column(String(100), nullable=True)  # Lembaga Pengangkat (Yayasan/Pemerintah/Kepsek)

    # 6. Civil Servant Details (Data PNS - Nullable jika bukan PNS)
    cpns_decree = Column(String(100), nullable=True)             # SK CPNS
    pns_start_date = Column(Date, nullable=True)                 # TMT PNS
    rank_class = Column(String(50), nullable=True)               # Pangkat / Golongan (e.g., "III/a", "IV/b")
    salary_source = Column(String(50), nullable=True)            # Sumber Gaji (e.g., "APBD", "Yayasan", "BOS")
    employee_card_number = Column(String(50), nullable=True)     # Kartu Pegawai (Karpeg)

    # 7. Status & Audit Trail
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 8. ORM Relationships
    user = relationship("User", back_populates="employee")
    school = relationship("SchoolIdentity", back_populates="employees")