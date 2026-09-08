import io
from fastapi.testclient import TestClient
from main import app
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.ppdb import PPDBAccount, PPDBRegistration
from app.core.security import get_password_hash

client = TestClient(app)

def run_test():
    print("=== MULAI PENGUJIAN ALUR PPDB END-TO-END ===")
    
    # 0. Buat Admin jika belum ada
    db = SessionLocal()
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@sekolah.sch.id",
            password=get_password_hash("admin123"),
            role=UserRole.ADMIN.value,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
    db.close()

    # Login Admin SIAKAD
    admin_login_res = client.post("/api/auth/login", data={"username": "admin", "password": "admin123"})
    assert admin_login_res.status_code == 200, f"Admin login failed: {admin_login_res.text}"
    admin_token = admin_login_res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("[OK] 0. Login Admin SIAKAD berhasil")

    # 1. Register Akun Calon Siswa
    unique_suffix = "0001"
    nik_test = f"320101234567{unique_suffix}"
    email_test = f"ahmad.fauzi.{unique_suffix}@gmail.com"

    # Bersihkan jika sisa tes sebelumnya
    db = SessionLocal()
    existing_acc = db.query(PPDBAccount).filter(PPDBAccount.nik == nik_test).first()
    if existing_acc:
        db.delete(existing_acc)
        db.commit()
    existing_std = db.query(Student).filter(Student.nik == nik_test).first()
    if existing_std:
        db.delete(existing_std)
        db.commit()
    existing_usr = db.query(User).filter(User.username == "0051234567").first()
    if existing_usr:
        db.delete(existing_usr)
        db.commit()
    db.close()

    reg_payload = {
        "nik": nik_test,
        "full_name": "Ahmad Fauzi Rahman",
        "email": email_test,
        "password": "PasswordPendaftar123!"
    }
    res_reg = client.post("/api/ppdb/register-account", json=reg_payload)
    assert res_reg.status_code == 201, f"Register account failed: {res_reg.text}"
    print("[OK] 1. POST /api/ppdb/register-account berhasil")

    # 2. Login Calon Siswa
    login_payload = {
        "nik": nik_test,
        "password": "PasswordPendaftar123!"
    }
    res_login = client.post("/api/ppdb/login", json=login_payload)
    assert res_login.status_code == 200, f"PPDB login failed: {res_login.text}"
    ppdb_token = res_login.json()["access_token"]
    ppdb_headers = {"Authorization": f"Bearer {ppdb_token}"}
    print("[OK] 2. POST /api/ppdb/login berhasil (JWT token role 'ppdb_applicant' diterima)")

    # 3. GET /my-registration
    res_my_reg = client.get("/api/ppdb/my-registration", headers=ppdb_headers)
    assert res_my_reg.status_code == 200, f"Get my registration failed: {res_my_reg.text}"
    reg_data = res_my_reg.json()
    registration_id = reg_data["id"]
    assert reg_data["payment_status"] == "unpaid"
    print(f"[OK] 3. GET /api/ppdb/my-registration berhasil (Registration ID: {registration_id})")

    # 4. Upload Bukti Pembayaran
    dummy_file = io.BytesIO(b"dummy image bytes for receipt")
    files = {"file": ("bukti_transfer.jpg", dummy_file, "image/jpeg")}
    res_upload = client.post("/api/ppdb/upload-payment", headers=ppdb_headers, files=files)
    assert res_upload.status_code == 200, f"Upload payment failed: {res_upload.text}"
    assert res_upload.json()["payment_status"] == "pending_verification"
    assert res_upload.json()["payment_proof_path"].startswith("/uploads/ppdb_payments/")
    print("[OK] 4. POST /api/ppdb/upload-payment berhasil (Status bayar: pending_verification)")

    # 5. PUT /registration-form (Format Nested JSON sesuai spesifikasi)
    form_payload = {
        "nik": nik_test,
        "nisn": "0051234567",
        "full_name": "Ahmad Fauzi Rahman",
        "first_name": "Ahmad",
        "last_name": "Fauzi Rahman",
        "identity": {
            "family_card_number": "3201010000000001",
            "gender": "Laki-laki",
            "religion": "Islam",
            "place_of_birth": "Jakarta",
            "date_of_birth": "2008-05-14"
        },
        "address": {
            "street_address": "Jl. Merdeka No. 45",
            "rt": "002",
            "rw": "005",
            "village": "Sukamaju",
            "district": "Cilodong",
            "postal_code": "16415",
            "residence_type": "Bersama Orang Tua",
            "transportation_mode": "Sepeda Motor"
        },
        "contact": {
            "phone_number": "021-77889900",
            "mobile_number": "081234567890",
            "whatsapp_number": "081234567890",
            "email": "ahmad.fauzi@student.sch.id"
        },
        "student_parents": [
            {
                "relationship_type": 1,
                "parent": {
                    "nik": "3201011122330001",
                    "full_name": "Bambang Sudarsono",
                    "birth_year": "1978",
                    "education_code": "05",
                    "occupation_code": "02",
                    "income_code": "03",
                    "phone_number": "081311223344",
                    "whatsapp_number": "081311223344"
                }
            }
        ]
    }
    res_form = client.put("/api/ppdb/registration-form", headers=ppdb_headers, json=form_payload)
    assert res_form.status_code == 200, f"Submit form failed: {res_form.text}"
    assert res_form.json()["form_data"]["nik"] == nik_test
    print("[OK] 5. PUT /api/ppdb/registration-form berhasil (Nested JSON tersimpan di JSONB form_data)")

    # 6. Admin Memeriksa Daftar Registrasi
    res_admin_list = client.get("/api/ppdb/registrations", headers=admin_headers)
    assert res_admin_list.status_code == 200, f"Admin list registrations failed: {res_admin_list.text}"
    assert len(res_admin_list.json()) >= 1
    print(f"[OK] 6. GET /api/ppdb/registrations berhasil (Ditemukan {len(res_admin_list.json())} pendaftar)")

    # 7. Admin Verifikasi Pembayaran
    verify_payload = {"payment_status": "paid", "payment_amount": 250000.00}
    res_verify = client.put(f"/api/ppdb/verify-payment/{registration_id}", headers=admin_headers, json=verify_payload)
    assert res_verify.status_code == 200, f"Verify payment failed: {res_verify.text}"
    assert res_verify.json()["payment_status"] == "paid"
    print("[OK] 7. PUT /api/ppdb/verify-payment/{id} berhasil (Status bayar: paid, Rp 250.000)")

    # 8. Admin Menerima Siswa & Melakukan Migrasi Data (Staging -> Master SIAKAD)
    res_accept = client.post(f"/api/ppdb/accept/{registration_id}", headers=admin_headers)
    assert res_accept.status_code == 200, f"Accept and migrate failed: {res_accept.text}"
    accept_data = res_accept.json()
    new_student_id = accept_data["student_id"]
    new_user_id = accept_data["user_id"]
    new_username = accept_data["username"]
    print(f"[OK] 8. POST /api/ppdb/accept/{id} berhasil!")
    print(f"       -> Student ID  : {new_student_id}")
    print(f"       -> User ID     : {new_user_id}")
    print(f"       -> Username    : {new_username}")

    # 9. Verifikasi Data Terdistribusi Sempurna di Tabel Master SIAKAD
    res_student_detail = client.get(f"/api/students/{new_student_id}", headers=admin_headers)
    assert res_student_detail.status_code == 200, f"Get migrated student detail failed: {res_student_detail.text}"
    std_json = res_student_detail.json()
    assert std_json["nik"] == nik_test
    assert std_json["nisn"] == "0051234567"
    assert std_json["identity"]["gender"] == "Laki-laki"
    assert std_json["address"]["street_address"] == "Jl. Merdeka No. 45"
    assert std_json["contact"]["phone_number"] == "021-77889900"
    assert len(std_json["student_parents"]) == 1
    assert std_json["student_parents"][0]["parent"]["full_name"] == "Bambang Sudarsono"
    print("[OK] 9. Verifikasi GET /api/students/{new_student_id} sukses: Biodata, identitas, alamat, kontak, orang tua terhubung sempurna!")

    # 10. Verifikasi Siswa Baru Bisa Langsung Login ke SIAKAD Utama
    res_student_login = client.post("/api/auth/login", data={"username": new_username, "password": "PasswordPendaftar123!"})
    assert res_student_login.status_code == 200, f"New student login failed: {res_student_login.text}"
    assert res_student_login.json()["role"] == "student"
    print(f"[OK] 10. Login Siswa Baru ke /api/auth/login sukses dengan username '{new_username}' dan role 'student'!")

    # 11. Verifikasi Penguncian Formulir Setelah Diterima
    res_locked_form = client.put("/api/ppdb/registration-form", headers=ppdb_headers, json=form_payload)
    assert res_locked_form.status_code == 400, "Formulir seharusnya terkunci setelah diterima!"
    print("[OK] 11. Verifikasi Penguncian Formulir sukses: Formulir terkunci dan tidak dapat diubah lagi!")

    print("\n[SUCCESS] SEMUA 11 TAHAP PENGUJIAN MODUL PPDB BERHASIL DENGAN SEMPURNA!")

if __name__ == "__main__":
    run_test()
