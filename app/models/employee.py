import uuid
from sqlalchemy import Column, String, Boolean, Date, DateTime, ForeignKey, Numeric, Text
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
    identity = relationship("EmployeeIdentity", back_populates="employee", uselist=False, cascade="all, delete")
    contacts = relationship("EmployeeContact", back_populates="employee", cascade="all, delete-orphan")
    children = relationship("EmployeeChild", back_populates="employee", cascade="all, delete-orphan")

class EmployeeIdentity(Base):
    __tablename__ = "employee_identities"
    __table_args__ = {'extend_existing': True}

    # 1. Primary Key & Relation
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), unique=True, nullable=False)

    # 2. Address Details (Alamat Domisili / Sesuai KK)
    street_address = Column(String(255), nullable=False)  # Alamat Jalan
    rt = Column(String(5), nullable=True)                 # RT
    rw = Column(String(5), nullable=True)                 # RW
    hamlet = Column(String(100), nullable=True)           # Nama Dusun / Kampung
    village = Column(String(100), nullable=False)         # Desa / Kelurahan
    district = Column(String(100), nullable=False)        # Kecamatan
    postal_code = Column(String(10), nullable=True)       # Kode Pos
    
    # Coordinates (Titik Koordinat untuk Dapodik/Pemetaan)
    latitude = Column(Numeric(10, 8), nullable=True)      # Lintang
    longitude = Column(Numeric(11, 8), nullable=True)     # Bujur

    # 3. Family & Personal Data
    family_card_number = Column(String(20), nullable=True) # No. KK (Kartu Keluarga)
    religion = Column(String(50), nullable=False)          # Agama
    citizenship = Column(String(50), default="ID", nullable=False) # Kewarganegaraan (e.g., "WNI" / "WNA")
    
    marital_status = Column(String(50), nullable=False)    # Status Perkawinan (e.g., "Kawin", "Belum Kawin")
    spouse_name = Column(String(100), nullable=True)       # Nama Pasangan (Suami/Istri)
    
    # 4. Financial & Tax Details (Keuangan & Pajak)
    tax_number = Column(String(30), unique=True, nullable=True)     # NPWP
    tax_holder_name = Column(String(100), nullable=True)            # Nama Wajib Pajak (sesuai NPWP)
    bank_name = Column(String(50), nullable=True)                   # Nama Bank (e.g., "BRI", "Bank Mandiri")
    bank_account_number = Column(String(50), nullable=True)         # No. Rekening Bank

    # 6. Audit Trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 7. ORM Relationship
    employee = relationship("Employee", back_populates="identity")

class EmployeeContact(Base):
    __tablename__ = "employee_contacts"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)

    # Detail Kontak
    contact_name = Column(String(100), nullable=False)
    relation = Column(String(50), nullable=False)       # Contoh: "Spouse", "Parent", "Sibling"
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    is_emergency_contact = Column(Boolean, default=True) # Penanda apakah ini kontak darurat utama

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relasi balik ke Employee
    employee = relationship("Employee", back_populates="contacts")

class EmployeeChild(Base):
    __tablename__ = "employee_children"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)

    # Identitas Anak
    child_name = Column(String(100), nullable=False)
    child_status = Column(String(50), nullable=False)   # e.g., "Biological" (Kandung), "Adopted" (Angkat), "Stepchild" (Tiri)
    gender = Column(String(20), nullable=False)         # "Male" / "Female"
    place_of_birth = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)

    # Data Pendidikan (Opsional, karena bisa jadi belum sekolah)
    education_level = Column(String(50), nullable=True) # e.g., "TK", "SD", "SMP", "SMA", "S1"
    nisn = Column(String(20), nullable=True)            # Nomor Induk Siswa Nasional
    enrollment_year = Column(String(4), nullable=True)  # Tahun Masuk (e.g., "2023")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relasi balik ke Employee
    employee = relationship("Employee", back_populates="children")