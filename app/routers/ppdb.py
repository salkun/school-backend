import os
import uuid
import shutil
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.config import settings
from app.core.security import verify_password, create_access_token, get_password_hash
from app.dependencies import require_admin, get_current_user
from app.models.user import User, UserRole
from app.models.student import Student, StudentIdentity, StudentAddress, StudentContact
from app.models.parent import Parent, StudentParentRelation
from app.models.ppdb import PPDBAccount, PPDBRegistration
from app.schemas.ppdb import (
    PPDBAccountRegister,
    PPDBAccountResponse,
    PPDBLoginRequest,
    PPDBTokenResponse,
    PPDBRegistrationFormInput,
    PPDBRegistrationResponse,
    PPDBPaymentVerifyRequest,
    PPDBAcceptResponse
)

router = APIRouter(
    prefix="/api/ppdb",
    tags=["PPDB (Penerimaan Peserta Didik Baru)"]
)

# Folder penyimpanan bukti pembayaran PPDB
UPLOAD_PPDB_DIR = "uploads/ppdb_payments"
os.makedirs(UPLOAD_PPDB_DIR, exist_ok=True)

# OAuth2 Scheme khusus untuk token calon siswa PPDB
ppdb_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/ppdb/login")


# ==========================================================
# DEPENDENCY KHUSUS AUTENTIKASI CALON SISWA PPDB
# ==========================================================
def get_current_ppdb_account(
    token: str = Depends(ppdb_oauth2_scheme),
    db: Session = Depends(get_db)
) -> PPDBAccount:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesi login PPDB tidak valid atau telah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        account_id_str: str = payload.get("account_id")
        role: str = payload.get("role")
        if not account_id_str or role != "ppdb_applicant":
            raise credentials_exception
        account_id = UUID(account_id_str)
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    account = db.query(PPDBAccount).filter(PPDBAccount.id == account_id).first()
    if not account:
        raise credentials_exception
    if not account.is_active:
        raise HTTPException(status_code=400, detail="Akun pendaftaran dinonaktifkan")

    return account


# ==========================================================
# 1. ENDPOINT PUBLIK (REGISTRASI & LOGIN PPDB)
# ==========================================================
@router.post(
    "/register-account",
    response_model=PPDBAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrasi Akun Calon Siswa Baru"
)
def register_ppdb_account(data: PPDBAccountRegister, db: Session = Depends(get_db)):
    """
    Pendaftaran akun awal untuk calon siswa baru menggunakan NIK, Nama, Email, dan Password.
    Sistem otomatis menginisialisasi tabel staging ppdb_registrations dengan status 'unpaid'.
    """
    # 1. Validasi duplikasi NIK atau Email di tabel ppdb_accounts
    existing_nik = db.query(PPDBAccount).filter(PPDBAccount.nik == data.nik).first()
    if existing_nik:
        raise HTTPException(status_code=400, detail="NIK sudah pernah didaftarkan pada sistem PPDB")

    existing_email = db.query(PPDBAccount).filter(PPDBAccount.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email sudah digunakan oleh calon pendaftar lain")

    # 2. Hash password
    hashed_password = get_password_hash(data.password)

    # 3. Simpan akun ke ppdb_accounts
    new_account = PPDBAccount(
        nik=data.nik,
        full_name=data.full_name,
        email=data.email,
        password_hash=hashed_password,
        is_active=True
    )
    db.add(new_account)
    db.flush()

    # 4. Inisialisasi entri pendaftaran di ppdb_registrations
    registration = PPDBRegistration(
        account_id=new_account.id,
        payment_status="unpaid",
        payment_amount=0.00,
        registration_status="pending",
        form_data=None
    )
    db.add(registration)

    db.commit()
    db.refresh(new_account)
    return new_account


@router.post(
    "/login",
    response_model=PPDBTokenResponse,
    summary="Login Akun Calon Siswa (Mendapatkan JWT PPDB)"
)
def login_ppdb(data: PPDBLoginRequest, db: Session = Depends(get_db)):
    """
    Autentikasi akun calon siswa menggunakan NIK atau Email dan Password.
    Mengembalikan token JWT khusus dengan role 'ppdb_applicant'.
    """
    if not data.nik and not data.email:
        raise HTTPException(status_code=400, detail="Masukkan NIK atau Email untuk login")

    # Cari akun berdasarkan NIK atau Email
    query = db.query(PPDBAccount)
    if data.nik:
        account = query.filter(PPDBAccount.nik == data.nik).first()
    else:
        account = query.filter(PPDBAccount.email == data.email).first()

    if not account or not verify_password(data.password, account.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="NIK/Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not account.is_active:
        raise HTTPException(status_code=400, detail="Akun pendaftaran ini tidak aktif")

    # Generate Token JWT khusus PPDB
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {
        "sub": account.nik,
        "account_id": str(account.id),
        "email": account.email,
        "role": "ppdb_applicant"
    }
    token = create_access_token(data=token_payload, expires_delta=access_token_expires)

    return PPDBTokenResponse(
        access_token=token,
        token_type="bearer",
        account_id=account.id,
        nik=account.nik,
        full_name=account.full_name,
        email=account.email
    )


@router.get(
    "/my-registration",
    response_model=PPDBRegistrationResponse,
    summary="Lihat Status Pendaftaran Sendiri (Calon Siswa)"
)
def get_my_registration(
    current_account: PPDBAccount = Depends(get_current_ppdb_account),
    db: Session = Depends(get_db)
):
    """
    Mengambil data pendaftaran lengkap milik calon siswa yang sedang login (status bayar, berkas, formulir).
    """
    reg = db.query(PPDBRegistration).options(
        joinedload(PPDBRegistration.account)
    ).filter(PPDBRegistration.account_id == current_account.id).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Data pendaftaran belum ditemukan")

    return reg


# ==========================================================
# 2. ENDPOINT PEMBAYARAN & FORMULIR (CALON SISWA)
# ==========================================================
@router.post(
    "/upload-payment",
    response_model=PPDBRegistrationResponse,
    summary="Unggah Bukti Pembayaran Pendaftaran"
)
async def upload_payment_proof(
    file: UploadFile = File(...),
    current_account: PPDBAccount = Depends(get_current_ppdb_account),
    db: Session = Depends(get_db)
):
    """
    Calon siswa mengunggah foto / PDF bukti pembayaran biaya pendaftaran.
    Status pembayaran otomatis berubah menjadi 'pending_verification'.
    """
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Berkas harus berupa gambar (JPG, PNG, WebP) atau PDF")

    # Ambil entri registrasi
    registration = db.query(PPDBRegistration).filter(
        PPDBRegistration.account_id == current_account.id
    ).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Data pendaftaran tidak ditemukan")

    # Simpan berkas fisik
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    dest_path = os.path.join(UPLOAD_PPDB_DIR, unique_filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    stored_url = f"/{UPLOAD_PPDB_DIR}/{unique_filename}".replace("\\", "/")

    # Update data registrasi
    registration.payment_proof_path = stored_url
    registration.payment_status = "pending_verification"

    db.commit()
    db.refresh(registration)
    return registration


@router.put(
    "/registration-form",
    response_model=PPDBRegistrationResponse,
    summary="Simpan / Perbarui Formulir Pendaftaran Lengkap"
)
def save_registration_form(
    data: PPDBRegistrationFormInput,
    current_account: PPDBAccount = Depends(get_current_ppdb_account),
    db: Session = Depends(get_db)
):
    """
    Menerima JSON bersarang utuh (struktur identik 100% dengan respons GET /api/students/{id}).
    Menyimpan data formulir ke kolom JSONB 'form_data' pada tabel staging ppdb_registrations.
    
    Sistem Penguncian: Jika status pendaftaran sudah 'accepted', formulir terkunci dan tidak dapat diubah lagi.
    """
    registration = db.query(PPDBRegistration).filter(
        PPDBRegistration.account_id == current_account.id
    ).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Data pendaftaran tidak ditemukan")

    # Validasi penguncian setelah diterima
    if registration.registration_status == "accepted":
        raise HTTPException(
            status_code=400,
            detail="Formulir telah dikunci karena Anda telah resmi diterima sebagai siswa"
        )

    # Konversi payload Pydantic menjadi dictionary JSON murni
    form_dict = data.model_dump(mode="json")

    # Simpan ke tabel staging
    registration.form_data = form_dict

    db.commit()
    db.refresh(registration)
    return registration


# ==========================================================
# 3. ENDPOINT ADMINISTRATOR (KHUSUS require_admin)
# ==========================================================
@router.get(
    "/registrations",
    response_model=List[PPDBRegistrationResponse],
    dependencies=[Depends(require_admin)],
    summary="Daftar Seluruh Pendaftar PPDB (Admin)"
)
def get_all_registrations(
    payment_status: Optional[str] = Query(None, description="Filter: unpaid, pending_verification, paid, rejected"),
    registration_status: Optional[str] = Query(None, description="Filter: pending, accepted, rejected"),
    search: Optional[str] = Query(None, description="Cari nama atau NIK calon siswa"),
    db: Session = Depends(get_db)
):
    """
    Admin dapat memantau seluruh pendaftar, memfilter status pembayaran, dan status seleksi.
    """
    query = db.query(PPDBRegistration).options(
        joinedload(PPDBRegistration.account)
    ).join(PPDBAccount, PPDBRegistration.account_id == PPDBAccount.id)

    if payment_status:
        query = query.filter(PPDBRegistration.payment_status == payment_status)
    if registration_status:
        query = query.filter(PPDBRegistration.registration_status == registration_status)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (PPDBAccount.full_name.ilike(search_pattern)) | 
            (PPDBAccount.nik.ilike(search_pattern))
        )

    return query.order_by(PPDBRegistration.created_at.desc()).all()


@router.get(
    "/registrations/{registration_id}",
    response_model=PPDBRegistrationResponse,
    dependencies=[Depends(require_admin)],
    summary="Detail Pendaftar PPDB (Admin)"
)
def get_registration_detail(registration_id: UUID, db: Session = Depends(get_db)):
    """
    Melihat detail berkas, bukti pembayaran, dan seluruh data formulir pendaftar.
    """
    reg = db.query(PPDBRegistration).options(
        joinedload(PPDBRegistration.account)
    ).filter(PPDBRegistration.id == registration_id).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Data pendaftaran tidak ditemukan")

    return reg


@router.put(
    "/verify-payment/{registration_id}",
    response_model=PPDBRegistrationResponse,
    dependencies=[Depends(require_admin)],
    summary="Verifikasi Pembayaran Pendaftar (Admin)"
)
def verify_registration_payment(
    registration_id: UUID,
    payload: PPDBPaymentVerifyRequest,
    current_admin: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Admin memverifikasi bukti bayar dan mengubah status pembayaran menjadi 'paid' atau 'rejected'.
    """
    reg = db.query(PPDBRegistration).filter(PPDBRegistration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Data pendaftaran tidak ditemukan")

    reg.payment_status = payload.payment_status
    reg.payment_verified_at = datetime.now()
    reg.payment_verified_by = current_admin.id

    if payload.payment_amount is not None:
        reg.payment_amount = payload.payment_amount

    db.commit()
    db.refresh(reg)
    return reg


@router.post(
    "/accept/{registration_id}",
    response_model=PPDBAcceptResponse,
    dependencies=[Depends(require_admin)],
    summary="Penerimaan Siswa & Migrasi Data Staging ke Master SIAKAD (Admin)"
)
def accept_and_migrate_student(
    registration_id: UUID,
    current_admin: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint Migrasi Otomatis (Staging Area -> Master Tables):
    1. Memverifikasi bahwa pendaftar berstatus pembayaran 'paid'.
    2. Mengekstrak data dari 'form_data' bersarang.
    3. Membuat akun 'users' baru dengan role 'student' (mewarisi password pendaftaran).
    4. Mendistribusikan data ke tabel 'students', 'student_identities', 'student_addresses',
       'student_contacts', dan 'parents' & 'student_parent_relations'.
    5. Mengubah status pendaftaran menjadi 'accepted' dan mengunci formulir pendaftaran.
    """
    reg = db.query(PPDBRegistration).options(
        joinedload(PPDBRegistration.account)
    ).filter(PPDBRegistration.id == registration_id).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Data pendaftaran tidak ditemukan")

    if reg.registration_status == "accepted":
        raise HTTPException(status_code=400, detail="Pendaftar ini sudah diterima dan dimigrasikan sebelumnya")

    if reg.payment_status != "paid":
        raise HTTPException(
            status_code=400,
            detail=f"Pendaftar belum dapat diterima. Status pembayaran saat ini: '{reg.payment_status}'. Wajib berstatus 'paid'."
        )

    if not reg.form_data:
        raise HTTPException(status_code=400, detail="Formulir pendaftaran calon siswa ini masih kosong")

    form = reg.form_data
    account = reg.account

    # 1. Ekstrak Field Utama Siswa
    nik = form.get("nik") or account.nik
    nisn = form.get("nisn")
    full_name = form.get("full_name") or account.full_name
    first_name = form.get("first_name")
    last_name = form.get("last_name")

    if not first_name:
        parts = full_name.strip().split(maxsplit=1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else None

    # 2. Cek apakah NIK atau NISN sudah ada di tabel master students
    dup_student = db.query(Student).filter(
        (Student.nik == nik) | (Student.nisn == nisn)
    ).first()
    if dup_student:
        raise HTTPException(
            status_code=400,
            detail=f"Siswa dengan NIK '{nik}' atau NISN '{nisn}' sudah terdaftar di database master siswa"
        )

    # 3. Buat Akun Pengguna Utama (users)
    username = nisn or nik
    # Pastikan username unik di tabel users
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        username = f"{nisn}_{str(uuid.uuid4())[:4]}"

    student_email = form.get("contact", {}).get("email") if form.get("contact") else account.email

    # Cek duplikasi email di users jika ada
    if student_email and db.query(User).filter(User.email == student_email).first():
        student_email = None  # Kosongkan email akun jika duplikat untuk mencegah crash

    new_user = User(
        username=username,
        email=student_email,
        password=account.password_hash,  # Siswa dapat langsung login dengan password yang sama saat mendaftar PPDB
        role=UserRole.STUDENT.value,
        school_id=current_admin.school_id,
        is_active=True
    )
    db.add(new_user)
    db.flush()

    # 4. Buat Record Siswa Pokok (students)
    new_student = Student(
        user_id=new_user.id,
        school_id=current_admin.school_id,
        nik=nik,
        nisn=nisn,
        full_name=full_name,
        first_name=first_name,
        last_name=last_name
    )
    db.add(new_student)
    db.flush()

    # 5. Migrasi Identitas Tambahan Siswa (student_identities)
    identity_data = form.get("identity")
    if identity_data:
        dob_str = identity_data.get("date_of_birth")
        dob = datetime.strptime(dob_str, "%Y-%m-%d") if isinstance(dob_str, str) else dob_str

        new_identity = StudentIdentity(
            student_id=new_student.id,
            family_card_number=identity_data.get("family_card_number"),
            gender=identity_data.get("gender") or "Laki-laki",
            religion=identity_data.get("religion") or "Islam",
            place_of_birth=identity_data.get("place_of_birth") or "-",
            date_of_birth=dob or datetime.now()
        )
        db.add(new_identity)

    # 6. Migrasi Alamat Siswa (student_addresses)
    address_data = form.get("address")
    if address_data:
        new_address = StudentAddress(
            student_id=new_student.id,
            street_address=address_data.get("street_address") or "-",
            rt=address_data.get("rt") or "000",
            rw=address_data.get("rw") or "000",
            village=address_data.get("village") or "-",
            district=address_data.get("district") or "-",
            postal_code=address_data.get("postal_code"),
            residence_type=address_data.get("residence_type"),
            transportation_mode=address_data.get("transportation_mode")
        )
        db.add(new_address)

    # 7. Migrasi Kontak Siswa (student_contacts)
    contact_data = form.get("contact")
    if contact_data:
        new_contact = StudentContact(
            student_id=new_student.id,
            phone_number=contact_data.get("phone_number"),
            mobile_number=contact_data.get("mobile_number"),
            whatsapp_number=contact_data.get("whatsapp_number"),
            email=contact_data.get("email")
        )
        db.add(new_contact)

    # 8. Migrasi Data Orang Tua / Wali (parents & student_parent_relations)
    parent_relations = form.get("student_parents") or []
    for item in parent_relations:
        rel_type = item.get("relationship_type", 1)
        p_data = item.get("parent") or {}
        p_nik = p_data.get("nik")

        parent_obj = None
        if p_nik:
            parent_obj = db.query(Parent).filter(Parent.nik == p_nik).first()

        if not parent_obj:
            parent_obj = Parent(
                nik=p_nik,
                full_name=p_data.get("full_name") or "Orang Tua Siswa",
                place_of_birth=p_data.get("place_of_birth"),
                birth_year=p_data.get("birth_year"),
                education_code=p_data.get("education_code"),
                occupation_code=p_data.get("occupation_code"),
                income_code=p_data.get("income_code"),
                special_need_code=p_data.get("special_need_code"),
                address=p_data.get("address"),
                phone_number=p_data.get("phone_number"),
                whatsapp_number=p_data.get("whatsapp_number")
            )
            db.add(parent_obj)
            db.flush()

        # Tautkan relasi
        relation_obj = StudentParentRelation(
            student_id=new_student.id,
            parent_id=parent_obj.id,
            relationship_type=rel_type
        )
        db.add(relation_obj)

    # 9. Update Status Pendaftaran di Staging
    reg.registration_status = "accepted"
    reg.student_id = new_student.id

    db.commit()

    return PPDBAcceptResponse(
        message="Calon siswa berhasil diterima dan seluruh data berhasil dimigrasikan ke database master SIAKAD!",
        registration_id=reg.id,
        student_id=new_student.id,
        user_id=new_user.id,
        username=new_user.username,
        full_name=new_student.full_name,
        role=new_user.role,
        migrated_at=datetime.now()
    )
