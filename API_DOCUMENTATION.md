# 📘 DOKUMENTASI LENGKAP REST API SIAKAD BACKEND

Dokumentasi ini disusun secara rinci dan terstruktur untuk mempermudah integrasi dengan sistem baru (Frontend Web, Mobile App, maupun Microservices/Sistem Eksternal).

---

## 📑 DAFTAR ISI
1. [Ikhtisar & Konvensi Global](#1-ikhtisar--konvensi-global)
2. [Autentikasi & Otorisasi (RBAC)](#2-autentikasi--otorisasi-rbac)
3. [Modul Autentikasi (`/api/auth`)](#3-modul-autentikasi-apiauth)
4. [Modul Pengguna (`/api/users`)](#4-modul-pengguna-apiusers)
5. [Modul Identitas Sekolah (`/api/schools`)](#5-modul-identitas-sekolah-apischools)
6. [Modul Data Master (`/api/master`)](#6-modul-data-master-apimaster)
   - [Tahun Ajaran (Academic Years)](#61-tahun-ajaran)
   - [Semester](#62-semester)
   - [Gedung (Buildings)](#63-gedung)
   - [Ruang Kelas (Classrooms)](#64-ruang-kelas)
   - [Mata Pelajaran (Subjects)](#65-mata-pelajaran)
7. [Modul Jabatan & Peran Pegawai (`/api/positions`)](#7-modul-jabatan--peran-pegawai-apipositions)
8. [Modul Data Siswa (`/api/students`)](#8-modul-data-siswa-apistudents)
   - [Biodata Siswa Utama](#81-biodata-siswa-utama)
   - [Identitas Tambahan Siswa (`/api/identities`)](#82-identitas-tambahan-siswa)
   - [Alamat Siswa (`/api/addresses`)](#83-alamat-siswa)
   - [Kontak Siswa (`/api/contacts`)](#84-kontak-siswa)
   - [Orang Tua / Wali Siswa (`/api/parents`)](#85-orang-tua--wali-siswa)
   - [Riwayat Kelas / Enrollment Siswa (`/api/enrollments`)](#86-riwayat-kelas--enrollment-siswa)
9. [Modul Data Pegawai / Guru (`/api/employees`)](#9-modul-data-pegawai--guru-apiemployees)
   - [Biodata Pegawai Utama](#91-biodata-pegawai-utama)
   - [Identitas Tambahan Pegawai (`/api/employee-identities`)](#92-identitas-tambahan-pegawai)
   - [Kontak Darurat Pegawai (`/api/employee-contacts`)](#93-kontak-darurat-pegawai)
   - [Data Anak Pegawai (`/api/employee-children`)](#94-data-anak-pegawai)
10. [Modul Penjadwalan & Wali Kelas (`/api/schedules`)](#10-modul-penjadwalan--wali-kelas-apischedules)
    - [Jadwal Mengajar (Teaching Schedules)](#101-jadwal-mengajar)
    - [Penugasan Wali Kelas (Homeroom Assignments)](#102-penugasan-wali-kelas)
11. [Modul LMS (Learning Management System) (`/api/lms`)](#11-modul-lms-learning-management-system-apilms)
    - [Materi Belajar (Materials)](#111-materi-belajar-materials)
    - [Penugasan & Submission (Assignments & Submissions)](#112-penugasan--submission-assignments--submissions)
    - [Portofolio Siswa (Portfolios)](#113-portofolio-siswa-portfolios)
12. [Modul Akademik & Rapor (`/api/academics`)](#12-modul-akademik--rapor-apiacademics)
    - [Rapor Semester (Report Cards)](#121-rapor-semester-report-cards)
13. [Modul Presensi & Absensi (`/api/attendance`)](#13-modul-presensi--absensi-apiattendance)
14. [Modul Pengumuman, Media, Profil, & Dashboard](#14-modul-pengumuman-media-profil--dashboard)
    - [Pengumuman (`/api/announcements`)](#141-pengumuman-apiannouncements)
    - [Upload Berkas (`/api/uploads`)](#142-upload-berkas-apiuploads)
    - [Profil Pengguna (`/api/profile`)](#143-profil-pengguna--keamanan-apiprofile)
    - [Statistik Dashboard (`/api/dashboard`)](#144-statistik-dashboard-apidashboard)
    - [Database Backup (`/api/backup`)](#145-database-backup-apibackup)
15. [Format Standar Error Response](#15-format-standar-error-response)

---

## 1. IKHTISAR & KONVENSI GLOBAL

* **Base URL**: `http://127.0.0.1:8000` (atau domain server Anda)
* **Format Data**: JSON (`application/json`) untuk request dan response (kecuali endpoint login menggunakan `application/x-www-form-urlencoded`).
* **Format ID**: UUID v4 (contoh: `3fa85f64-5717-4562-b3fc-2c963f66afa6`).
* **Format Tanggal**: 
  * Tanggal (`Date`): `YYYY-MM-DD` (contoh: `2005-01-15`)
  * Waktu (`Time`): `HH:MM:SS` (contoh: `07:30:00`)
  * Timestamp: ISO 8601 UTC (contoh: `2026-09-02T08:00:00.000Z`)
* **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
* **Redoc Docs**: `http://127.0.0.1:8000/redoc`

---

## 2. AUTENTIKASI & OTORISASI (RBAC)

API ini menggunakan **JWT (JSON Web Token) Bearer Token**.

### Header Request Wajib (Untuk Endpoint Terproteksi):
```http
Authorization: Bearer <access_token>
```

### Role Pengguna:
| Role | Deskripsi | Hak Akses |
|------|-----------|-----------|
| `admin` | Administrator Sistem | Akses penuh (Create, Read, Update, Delete) ke semua data |
| `teacher` | Guru / Tenaga Pendidik | Akses Read ke data siswa, pegawai, jadwal, master data; input nilai |
| `student` | Siswa | Akses ke data profil diri sendiri, jadwal kelas, absensi, nilai |
| `parent` | Orang Tua / Wali | Akses ke riwayat akademik dan informasi anak yang diasuh |

---

## 3. MODUL AUTENTIKASI (`/api/auth`)

### 3.1 Login Pengguna (Mendapatkan JWT Token)
* **Endpoint**: `POST /api/auth/login`
* **Content-Type**: `application/x-www-form-urlencoded`
* **Akses**: Publik

#### Request Body (Form Data):
| Field | Tipe | Wajib | Deskripsi |
|-------|------|-------|-----------|
| `username` | string | Ya | Username pengguna |
| `password` | string | Ya | Password teks biasa |

#### Response (`200 OK`):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Error Response:
* `401 Unauthorized`: Username atau password salah.

---

## 4. MODUL PENGGUNA (`/api/users`)
*Kunci Akses: Khusus `admin`*

### 4.1 Tambah Pengguna Baru
* **Endpoint**: `POST /api/users/`
* **Akses**: Admin

#### Request Body (JSON):
```json
{
  "username": "guru_matematika",
  "email": "guru.math@sekolah.sch.id",
  "password": "PasswordKuat123!",
  "role": "teacher",
  "school_id": "8f7e2c91-9e12-4c28-9d3e-11aa22bb33cc",
  "is_active": true
}
```
*(Catatan: `email` dan `school_id` bersifat opsional)*

#### Response (`201 Created`):
```json
{
  "id": "e6ce8ff7-be4b-47ef-9850-8bf848d58a7e",
  "username": "guru_matematika",
  "email": "guru.math@sekolah.sch.id",
  "role": "teacher",
  "school_id": "8f7e2c91-9e12-4c28-9d3e-11aa22bb33cc",
  "is_active": true,
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z"
}
```

### 4.2 Ambil Semua Pengguna
* **Endpoint**: `GET /api/users/`
* **Response**: `200 OK` (Array of User Objects)

### 4.3 Ambil Detail Pengguna
* **Endpoint**: `GET /api/users/{user_id}`
* **Response**: `200 OK` (User Object)

### 4.4 Update Data Pengguna
* **Endpoint**: `PUT /api/users/{user_id}`
* **Request Body (JSON)**: Field opsional (`username`, `email`, `role`, `is_active`, `school_id`, `password`).

### 4.5 Hapus Pengguna
* **Endpoint**: `DELETE /api/users/{user_id}`
* **Response**: `204 No Content`

---

## 5. MODUL IDENTITAS SEKOLAH (`/api/schools`)

### 5.1 Create / Update Profil Sekolah (Single Identity)
* **Endpoint**: `POST /api/schools/`
* **Akses**: Admin

#### Request Body (JSON):
```json
{
  "name": "SMK Negeri 1 Jakarta",
  "npsn": "20101234",
  "address": "Jl. Budi Utomo No. 7, Sawah Besar, Jakarta Pusat"
}
```

#### Response (`201 Created` / `200 OK`):
```json
{
  "id": "7fa12345-1111-2222-3333-444455556666",
  "name": "SMK Negeri 1 Jakarta",
  "npsn": "20101234",
  "address": "Jl. Budi Utomo No. 7, Sawah Besar, Jakarta Pusat",
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z"
}
```

### 5.2 Ambil Profil Sekolah
* **Endpoint**: `GET /api/schools/`
* **Akses**: Admin & Teacher (`require_staff`)

---

## 6. MODUL DATA MASTER (`/api/master`)
*Kunci Akses: Write (`POST`/`PUT`/`DELETE`) = `admin`; Read (`GET`) = `admin` & `teacher`*

### 6.1 Tahun Ajaran (`/api/master/academic-years/`)
* **Create**: `POST /api/master/academic-years/`
  ```json
  {
    "start_year": 2025,
    "end_year": 2026,
    "is_active": true
  }
  ```
* **List**: `GET /api/master/academic-years/`
* **Update**: `PUT /api/master/academic-years/{id}`
* **Delete**: `DELETE /api/master/academic-years/{id}`

### 6.2 Semester (`/api/master/semesters/`)
* **Create**: `POST /api/master/semesters/`
  ```json
  {
    "academic_year_id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
    "name": "Ganjil",
    "is_active": true
  }
  ```
* **List**: `GET /api/master/semesters/`
* **Update**: `PUT /api/master/semesters/{id}`
* **Delete**: `DELETE /api/master/semesters/{id}`

### 6.3 Gedung (`/api/master/buildings/`)
* **Create**: `POST /api/master/buildings/`
  ```json
  {
    "name": "Gedung Teori A",
    "established_year": 2018,
    "area": 450.5,
    "width": 15.0,
    "height": 30.0,
    "is_active": true
  }
  ```
* **List**: `GET /api/master/buildings/`
* **Update**: `PUT /api/master/buildings/{id}`
* **Delete**: `DELETE /api/master/buildings/{id}`

### 6.4 Ruang Kelas (`/api/master/classrooms/`)
* **Create**: `POST /api/master/classrooms/`
  ```json
  {
    "building_id": "71006039-8458-488d-9868-b2a27fa8fa55",
    "name": "X RPL 1",
    "area": 64.0,
    "width": 8.0,
    "height": 8.0,
    "is_active": true
  }
  ```
* **List**: `GET /api/master/classrooms/`
* **Update**: `PUT /api/master/classrooms/{id}`
* **Delete**: `DELETE /api/master/classrooms/{id}`

### 6.5 Mata Pelajaran (`/api/master/subjects/`)
* **Create**: `POST /api/master/subjects/`
  ```json
  {
    "name": "Pemrograman Web & Perangkat Bergerak",
    "lesson_hours": 6,
    "is_active": true
  }
  ```
* **List**: `GET /api/master/subjects/`
* **Update**: `PUT /api/master/subjects/{id}`
* **Delete**: `DELETE /api/master/subjects/{id}`

---

## 7. MODUL JABATAN & PERAN PEGAWAI (`/api/positions`)

### 7.1 Master Jabatan
* **Create**: `POST /api/positions/` (Admin)
  ```json
  {
    "name": "Kepala Program Keahlian RPL",
    "code": "HEAD_OF_MAJOR",
    "is_structural": true,
    "is_active": true
  }
  ```
  *(Catatan: `code` digunakan oleh sistem RBAC untuk menentukan hak akses spesifik pegawai, contoh: `CURRICULUM`, `PRINCIPAL`, `STAFF_TU`, `TREASURER`, `TEACHER`)*
* **List**: `GET /api/positions/` (Staff & Admin)

### 7.2 Penetapan Riwayat Jabatan Pegawai
* **Assign Position**: `POST /api/positions/employee/` (Admin)
  ```json
  {
    "employee_id": "a2054fda-a7fb-4825-8bfc-a7909aec3d6a",
    "position_id": "4b6c8d1e-2f3a-4e5b-6c7d-8e9f0a1b2c3d",
    "academic_year_id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
    "is_active": true
  }
  ```
* **Get Riwayat Jabatan Pegawai**: `GET /api/positions/employee/{employee_id}` (Staff & Admin)

---

## 8. MODUL DATA SISWA (`/api/students`)

Struktur data siswa dipecah menjadi modul modular untuk memudahkan form multi-step di frontend:

### 8.1 Biodata Siswa Utama
* **Tambah Siswa**: `POST /api/students/` (Admin)
  ```json
  {
    "user_id": "b1545031-4ecb-4b63-b576-bf01a4430aac",
    "school_id": "7fa12345-1111-2222-3333-444455556666",
    "nik": "3201012345670001",
    "nisn": "0051234567",
    "full_name": "Ahmad Fauzi",
    "first_name": "Ahmad",
    "last_name": "Fauzi"
  }
  ```
  *Aturan*: `nik` harus 16 digit unik, `nisn` unik.
* **List Semua Siswa**: `GET /api/students/` (Staff & Admin)
* **Detail Siswa Lengkap**: `GET /api/students/{student_id}` (Staff & Admin)
  *Mengembalikan relasi teragregasi: `identity`, `address`, `contact`, dan `student_parents`.*
* **Hapus Siswa**: `DELETE /api/students/{student_id}` (Admin)

### 8.2 Identitas Tambahan Siswa (`/api/identities`)
* **Create / Update**: `POST /api/identities/{student_id}`
  ```json
  {
    "family_card_number": "3201012345670000",
    "gender": "Laki-laki",
    "religion": "Islam",
    "place_of_birth": "Jakarta",
    "date_of_birth": "2007-05-14"
  }
  ```
* **Get Detail**: `GET /api/identities/{student_id}`

### 8.3 Alamat Siswa (`/api/addresses`)
* **Create / Update**: `POST /api/addresses/{student_id}`
  ```json
  {
    "street_address": "Jl. Merdeka No. 45 RT 02/05",
    "rt": "002",
    "rw": "005",
    "village": "Sukamaju",
    "district": "Cilodong",
    "postal_code": "16415",
    "residence_type": "Bersama Orang Tua",
    "transportation_mode": "Sepeda Motor"
  }
  ```
* **Get Detail**: `GET /api/addresses/{student_id}`

### 8.4 Kontak Siswa (`/api/contacts`)
* **Create / Update**: `POST /api/contacts/{student_id}`
  ```json
  {
    "phone_number": "021-77889900",
    "mobile_number": "081234567890",
    "whatsapp_number": "081234567890",
    "email": "ahmad.fauzi@student.sch.id"
  }
  ```
* **Get Detail**: `GET /api/contacts/{student_id}`

### 8.5 Orang Tua / Wali Siswa (`/api/parents`)
Mendukung relasi multi-anak (jika NIK orang tua sama, otomatis ditautkan tanpa duplikasi data master orang tua).

* **Tambah Orang Tua untuk Siswa**: `POST /api/parents/{student_id}` (Admin)
  ```json
  {
    "relationship_type": 1,
    "full_name": "Bambang Sudarsono",
    "nik": "3201011122330001",
    "place_of_birth": "Semarang",
    "birth_year": "1978",
    "education_code": "05",
    "occupation_code": "02",
    "income_code": "03",
    "special_need_code": "00",
    "address": "Jl. Merdeka No. 45",
    "phone_number": "081311223344",
    "whatsapp_number": "081311223344"
  }
  ```
  *Kamus `relationship_type`*:
  * `1` = Ayah Kandung
  * `2` = Ibu Kandung
  * `3` = Wali
* **Ambil Semua Orang Tua Siswa**: `GET /api/parents/{student_id}` (Staff & Admin)
* **Hapus Hubungan Relasi**: `DELETE /api/parents/relation/{relation_id}` (Admin)

### 8.6 Riwayat Kelas / Enrollment Siswa (`/api/enrollments`)
* **Daftarkan Siswa ke Kelas**: `POST /api/enrollments/` (Admin)
  ```json
  {
    "student_id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
    "classroom_id": "cd65245e-120b-49f5-bde5-41fc13a5f3b5",
    "academic_year_id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
    "semester_id": "8ae202db-fe9d-4661-b4f3-193e8ce3928c",
    "status": "Active"
  }
  ```
* **Ambil Riwayat Kelas Siswa**: `GET /api/enrollments/student/{student_id}` (Staff & Admin)

---

## 9. MODUL DATA PEGAWAI / GURU (`/api/employees`)

### 9.1 Biodata Pegawai Utama
* **Tambah Pegawai**: `POST /api/employees/` (Admin)
  ```json
  {
    "user_id": "02982450-4531-494f-8c4b-27077381ded1",
    "school_id": "7fa12345-1111-2222-3333-444455556666",
    "full_name": "Drs. Hendra Gunawan, M.Pd.",
    "nik": "3276011204750002",
    "gender": "Laki-laki",
    "place_of_birth": "Bandung",
    "date_of_birth": "1975-04-12",
    "mother_maiden_name": "Siti Maryam",
    "nip": "197504122000031001",
    "nuptk": "1234567890123456",
    "employment_status": "PNS",
    "ptk_type": "Guru Mapel",
    "rank_class": "IV/a",
    "salary_source": "APBD",
    "is_active": true
  }
  ```
* **List Semua Pegawai**: `GET /api/employees/` (Staff & Admin)
* **Detail Pegawai**: `GET /api/employees/{employee_id}` (Staff & Admin)
* **Update Data Pegawai**: `PUT /api/employees/{employee_id}` (Admin)
* **Hapus Pegawai**: `DELETE /api/employees/{employee_id}` (Admin)

### 9.2 Identitas Tambahan Pegawai (`/api/employee-identities`)
* **Create**: `POST /api/employee-identities/` (Admin)
  ```json
  {
    "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
    "street_address": "Komp. Guru No. 12",
    "rt": "001",
    "rw": "003",
    "village": "Pasir Putih",
    "district": "Sawangan",
    "postal_code": "16519",
    "family_card_number": "3276010000000001",
    "religion": "Islam",
    "citizenship": "WNI",
    "marital_status": "Kawin",
    "spouse_name": "Dewi Sartika",
    "tax_number": "09.123.456.7-412.000",
    "bank_name": "Bank BJB",
    "bank_account_number": "0012345678901"
  }
  ```
* **Get by Employee ID**: `GET /api/employee-identities/employee/{employee_id}` (Staff & Admin)
* **Update**: `PUT /api/employee-identities/{identity_id}` (Admin)
* **Delete**: `DELETE /api/employee-identities/{identity_id}` (Admin)

### 9.3 Kontak Darurat Pegawai (`/api/employee-contacts`)
* **Create**: `POST /api/employee-contacts/` (Admin)
  ```json
  {
    "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
    "contact_name": "Dewi Sartika",
    "relation": "Istri",
    "phone_number": "081299887766",
    "email": "dewi.sartika@gmail.com",
    "is_emergency_contact": true
  }
  ```
* **List Kontak Milik Pegawai**: `GET /api/employee-contacts/employee/{employee_id}` (Staff & Admin)
* **Update**: `PUT /api/employee-contacts/{contact_id}` (Admin)
* **Delete**: `DELETE /api/employee-contacts/{contact_id}` (Admin)

### 9.4 Data Anak Pegawai (`/api/employee-children`)
* **Create**: `POST /api/employee-children/` (Admin)
  ```json
  {
    "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
    "child_name": "Rizky Gunawan",
    "child_status": "Anak Kandung",
    "gender": "Laki-laki",
    "place_of_birth": "Depok",
    "date_of_birth": "2012-08-10",
    "education_level": "SMP",
    "enrollment_year": "2024"
  }
  ```
* **List Anak Milik Pegawai**: `GET /api/employee-children/employee/{employee_id}` (Staff & Admin)
* **Update**: `PUT /api/employee-children/{child_id}` (Admin)
* **Delete**: `DELETE /api/employee-children/{child_id}` (Admin)

### 9.5 Pengampu Mata Pelajaran Pegawai (Many-to-Many)
* **Assign Mapel ke Guru**: `POST /api/employees/{employee_id}/subjects/{subject_id}` (Admin)
* **List Mapel yang Diampu Guru**: `GET /api/employees/{employee_id}/subjects` (Staff & Admin)
* **Unassign Mapel**: `DELETE /api/employees/{employee_id}/subjects/{subject_id}` (Admin)

---

## 10. MODUL PENJADWALAN & WALI KELAS (`/api/schedules`)
*Kunci Akses: Write = `admin`; Read = `admin` & `teacher`*

### 10.1 Jadwal Mengajar (Teaching Schedules)
* **Tambah Jadwal Mengajar**: `POST /api/schedules/teaching/`
  ```json
  {
    "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
    "subject_id": "63df9d9a-8e34-4812-b95b-fa5f15fc4b90",
    "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
    "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d",
    "semester_id": "ee40b194-5b69-4258-ae43-d882c2470817",
    "day_of_week": "Senin",
    "start_time": "07:00:00",
    "end_time": "09:15:00"
  }
  ```
* **Ambil Jadwal Berdasarkan Guru**: `GET /api/schedules/teaching/employee/{employee_id}`

### 10.2 Penugasan Wali Kelas (Homeroom Assignments)
* **Tugaskan Wali Kelas**: `POST /api/schedules/homeroom/`
  ```json
  {
    "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
    "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
    "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d"
  }
  ```
* **Ambil Riwayat Wali Kelas per Ruang Kelas**: `GET /api/schedules/homeroom/classroom/{classroom_id}`

---

## 11. MODUL LMS (LEARNING MANAGEMENT SYSTEM) (`/api/lms`)

### 11.1 Materi Belajar (Materials)
* **Tambah Materi**: `POST /api/lms/materials/` *(Role: Teacher, Admin)*
  ```json
  {
    "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
    "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
    "title": "Pengenalan Aljabar Linier",
    "content": "Rangkuman bab 1 aljabar...",
    "file_path": "/uploads/materials/aljabar.pdf",
    "video_url": "https://youtube.com/watch?v=xxx",
    "is_active": true
  }
  ```
* **Ambil Materi per Mapel**: `GET /api/lms/materials/subject/{subject_id}`
* **Detail Materi**: `GET /api/lms/materials/{id}`
* **Update Materi**: `PUT /api/lms/materials/{id}`
* **Hapus Materi**: `DELETE /api/lms/materials/{id}`
* **Tandai Selesai (Siswa)**: `POST /api/lms/materials/{id}/toggle-complete`

### 11.2 Penugasan & Submission (Assignments & Submissions)
* **Buat Tugas Baru**: `POST /api/lms/assignments/` *(Role: Teacher, Admin)*
  ```json
  {
    "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
    "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
    "title": "Tugas 1: Menyelesaikan Persamaan Matriks",
    "description": "Kerjakan soal 1-5 dan kumpulkan dalam format PDF.",
    "type": "file",
    "deadline": "2026-09-10T23:59:59Z",
    "max_score": 100.00
  }
  ```
* **Daftar Tugas per Mapel**: `GET /api/lms/assignments/subject/{subject_id}`
* **Daftar Tugas Mendekati Deadline**: `GET /api/lms/assignments/upcoming`
* **Detail Tugas**: `GET /api/lms/assignments/{id}`
* **Kumpulkan Tugas (Siswa)**: `POST /api/lms/submissions/`
  ```json
  {
    "assignment_id": "b8159043-98fe-4a94-b209-661ff97a514d",
    "content": "Berikut tautan lampiran tugas saya.",
    "file_path": "/uploads/submissions/jawaban_siswa.pdf"
  }
  ```
* **Lihat Submission Siswa (Guru)**: `GET /api/lms/assignments/{id}/submissions`
* **Beri Nilai & Feedback**: `POST /api/lms/submissions/{id}/grade`
  ```json
  {
    "score": 92.50,
    "feedback": "Penjelasan di nomor 3 sangat sistematis dan tepat!"
  }
  ```

### 11.3 Portofolio Siswa (Portfolios)
* **Buat Portofolio**: `POST /api/lms/portfolios/` *(Role: Student)*
* **Daftar Portofolio Siswa**: `GET /api/lms/portfolios/student/{student_id}`
* **Hapus Portofolio**: `DELETE /api/lms/portfolios/{id}`

---

## 12. MODUL AKADEMIK & RAPOR (`/api/academics`)

### 12.1 Rapor Semester (Report Cards)
* **Buat Header Rapor**: `POST /api/academics/report-cards/`
  ```json
  {
    "student_id": "18f921d7-2f3b-48aa-b924-d2e8b15d6c82",
    "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
    "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d",
    "semester_id": "4b684da3-0bca-4bc4-9d54-8e1da4d5a371",
    "sick_count": 1,
    "permitted_count": 2,
    "unexcused_count": 0,
    "homeroom_notes": "Siswa sangat berprestasi dan aktif dalam diskusi."
  }
  ```
* **Ambil Rapor Siswa**: `GET /api/academics/report-cards/student/{student_id}`
* **Detail Rapor**: `GET /api/academics/report-cards/{id}`
* **Batch Input Nilai Mata Pelajaran**: `POST /api/academics/report-cards/{id}/items`
  ```json
  {
    "items": [
      {
        "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
        "knowledge_score": 88.00,
        "skill_score": 90.00,
        "final_score": 89.00,
        "letter_grade": "A",
        "competency_description": "Sangat terampil dalam memecahkan soal aljabar dan matriks."
      }
    ]
  }
  ```
* **Terbitkan Rapor (Publish)**: `PUT /api/academics/report-cards/{id}/publish`

---

## 13. MODUL PRESENSI & ABSENSI (`/api/attendance`)

* **Buka Sesi Presensi**: `POST /api/attendance/sessions/`
  ```json
  {
    "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
    "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
    "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d",
    "semester_id": "4b684da3-0bca-4bc4-9d54-8e1da4d5a371",
    "session_date": "2026-09-02",
    "start_time": "07:30:00",
    "end_time": "09:00:00",
    "topic": "Pengenalan Vektor 2D"
  }
  ```
* **Riwayat Sesi Kelas**: `GET /api/attendance/sessions/classroom/{classroom_id}`
* **Detail Sesi**: `GET /api/attendance/sessions/{session_id}`
* **Simpan Kehadiran Siswa (Batch)**: `POST /api/attendance/sessions/{session_id}/records`
  ```json
  {
    "records": [
      { "student_id": "18f921d7-2f3b-48aa-b924-d2e8b15d6c82", "status": "present", "remarks": "Hadir tepat waktu" },
      { "student_id": "78a911d2-11bb-49cc-a924-a1e8b15d6c99", "status": "sick", "remarks": "Surat dokter" }
    ]
  }
  ```
* **Rekap Kehadiran Siswa (Summary)**: `GET /api/attendance/summary/student/{student_id}`

---

## 14. MODUL PENGUMUMAN, MEDIA, PROFIL, & DASHBOARD

### 14.1 Pengumuman (`/api/announcements`)
* `POST /api/announcements/` — Buat pengumuman baru (Sekolah/Kelas).
* `GET /api/announcements/` — Ambil daftar pengumuman.
* `GET /api/announcements/{id}` — Detail pengumuman.
* `PUT /api/announcements/{id}` & `DELETE /api/announcements/{id}` — Edit / hapus pengumuman.

### 14.2 Upload Berkas (`/api/uploads`)
* `POST /api/uploads/avatar` — Upload avatar foto profil (Multipart Form).
* `POST /api/uploads/document` — Upload file materi/tugas/jawaban (Multipart Form).

### 14.3 Profil Pengguna & Keamanan (`/api/profile`)
* `GET /api/profile/me` — Ambil data pengguna login (termasuk profil guru/siswa yang terhubung).
* `PUT /api/profile/me` — Update data dasar profil (email/nama).
* `PUT /api/profile/change-password` — Ganti password akun.

### 14.4 Statistik Dashboard (`/api/dashboard`)
* `GET /api/dashboard/stats` — Rekap total siswa, guru, kelas, mapel, materi, tugas, dan pengumuman.

### 14.5 Database Backup (`/api/backup`)
* `GET /api/backup/export-json` — *(Role: Admin)* Download seluruh data tabel database dalam format `.json`.

---

## 15. FORMAT STANDAR ERROR RESPONSE

Semua error mengikuti format baku FastAPI:

```json
{
  "detail": "Pesan deskripsi kesalahan yang jelas dan spesifik"
}
```

### Daftar HTTP Status Code yang Digunakan:
* `200 OK`: Permintaan GET/PUT berhasil.
* `201 Created`: Data baru berhasil dibuat (POST).
* `204 No Content`: Data berhasil dihapus (DELETE).
* `400 Bad Request`: Validasi data gagal atau terjadi duplikasi (misal NIK/NISN sudah terdaftar).
* `401 Unauthorized`: Token JWT tidak ada, kedaluwarsa, atau kredensial salah.
* `403 Forbidden`: Role akun pengguna tidak memiliki izin mengakses endpoint ini.
* `404 Not Found`: Data dengan ID yang diminta tidak ditemukan di database.
* `422 Unprocessable Entity`: Tipe data payload tidak valid (gagal validasi schema Pydantic).
* `500 Internal Server Error`: Terjadi kesalahan pada internal server/database.
