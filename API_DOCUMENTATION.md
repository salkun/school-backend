# 📘 DOKUMENTASI LENGKAP REST API SISTEM INFORMASI AKADEMIK (SIAKAD) & LMS

Dokumentasi resmi ini disusun secara komprehensif, terstruktur, dan mendalam untuk menjadi acuan utama integrasi pengembang Frontend (Web Admin, Web Guru, Web Siswa/Orang Tua), Mobile App (Android/iOS), serta layanan pihak ketiga.

---

## 📑 DAFTAR ISI

1. [Ikhtisar & Konvensi Global](#1-ikhtisar--konvensi-global)
2. [Autentikasi & Otorisasi Berbasis Peran (RBAC)](#2-autentikasi--otorisasi-berbasis-peran-rbac)
3. [Root Endpoint](#3-root-endpoint)
4. [Modul Autentikasi (`/api/auth`)](#4-modul-autentikasi-apiauth)
5. [Modul Pengguna / User Management (`/api/users`)](#5-modul-pengguna--user-management-apiusers)
6. [Modul Profil Pengguna & Keamanan Akun (`/api/profile`)](#6-modul-profil-pengguna--keamanan-akun-apiprofile)
7. [Modul Statistik Dashboard (`/api/dashboard`)](#7-modul-statistik-dashboard-apidashboard)
8. [Modul Identitas Sekolah (`/api/schools`)](#8-modul-identitas-sekolah-apischools)
9. [Modul Data Master (`/api/master`)](#9-modul-data-master-apimaster)
   - [9.1 Tahun Ajaran (Academic Years)](#91-tahun-ajaran-academic-years)
   - [9.2 Semester](#92-semester)
   - [9.3 Gedung (Buildings)](#93-gedung-buildings)
   - [9.4 Ruang Kelas (Classrooms)](#94-ruang-kelas-classrooms)
   - [9.5 Mata Pelajaran (Subjects)](#95-mata-pelajaran-subjects)
10. [Modul Jabatan Pegawai (`/api/positions`)](#10-modul-jabatan-pegawai-apipositions)
    - [10.1 Master Jabatan](#101-master-jabatan)
    - [10.2 Penugasan Jabatan Pegawai (Employee Positions)](#102-penugasan-jabatan-pegawai-employee-positions)
11. [Modul Penjadwalan & Wali Kelas (`/api/schedules`)](#11-modul-penjadwalan--wali-kelas-apischedules)
    - [11.1 Jadwal Mengajar (Teaching Schedules)](#111-jadwal-mengajar-teaching-schedules)
    - [11.2 Penugasan Wali Kelas (Homeroom Assignments)](#112-penugasan-wali-kelas-homeroom-assignments)
12. [Modul Data Siswa](#12-modul-data-siswa)
    - [12.1 Biodata Pokok Siswa (`/api/students`)](#121-biodata-pokok-siswa-apistudents)
    - [12.2 Identitas Tambahan Siswa (`/api/identities`)](#122-identitas-tambahan-siswa-apiidentities)
    - [12.3 Alamat Siswa (`/api/addresses`)](#123-alamat-siswa-apiaddresses)
    - [12.4 Kontak Siswa (`/api/contacts`)](#124-kontak-siswa-apicontacts)
    - [12.5 Orang Tua / Wali Siswa (`/api/parents`)](#125-orang-tua--wali-siswa-apiparents)
    - [12.6 Riwayat Kelas & Enrollment (`/api/enrollments`)](#126-riwayat-kelas--enrollment-apienrollments)
13. [Modul Data Pegawai / Guru](#13-modul-data-pegawai--guru)
    - [13.1 Biodata Pokok Pegawai (`/api/employees`)](#131-biodata-pokok-pegawai-apiemployees)
    - [13.2 Identitas Tambahan Pegawai (`/api/employee-identities`)](#132-identitas-tambahan-pegawai-apiemployee-identities)
    - [13.3 Kontak Darurat Pegawai (`/api/employee-contacts`)](#133-kontak-darurat-pegawai-apiemployee-contacts)
    - [13.4 Data Anak Pegawai (`/api/employee-children`)](#134-data-anak-pegawai-apiemployee-children)
    - [13.5 Pengampu Mata Pelajaran Pegawai (`/api/employees/{id}/subjects`)](#135-pengampu-mata-pelajaran-pegawai-apiemployeesidsubjects)
14. [Modul LMS (Learning Management System) (`/api/lms`)](#14-modul-lms-learning-management-system-apilms)
    - [14.1 Materi Belajar (Materials)](#141-materi-belajar-materials)
    - [14.2 Tugas (Assignments)](#142-tugas-assignments)
    - [14.3 Pengumpulan & Penilaian Tugas (Submissions & Grades)](#143-pengumpulan--penilaian-tugas-submissions--grades)
    - [14.4 Portofolio Siswa (Portfolios)](#144-portofolio-siswa-portfolios)
15. [Modul Akademik & Nilai Rapor (`/api/academics`)](#15-modul-akademik--nilai-rapor-apiacademics)
    - [15.1 Header Rapor Siswa (Report Cards)](#151-header-rapor-siswa-report-cards)
    - [15.2 Rincian Nilai Mata Pelajaran Rapor (Report Card Items)](#152-rincian-nilai-mata-pelajaran-rapor-report-card-items)
16. [Modul Presensi & Absensi (`/api/attendance`)](#16-modul-presensi--absensi-apiattendance)
    - [16.1 Sesi Presensi (Attendance Sessions)](#161-sesi-presensi-attendance-sessions)
    - [16.2 Catatan & Rekap Kehadiran Siswa](#162-catatan--rekap-kehadiran-siswa)
17. [Modul Pengumuman (`/api/announcements`)](#17-modul-pengumuman-apiannouncements)
18. [Modul Unggah Media & Berkas (`/api/uploads`)](#18-modul-unggah-media--berkas-apiuploads)
19. [Modul Database Backup & Maintenance (`/api/backup`)](#19-modul-database-backup--maintenance-apibackup)
20. [Modul PPDB (Penerimaan Peserta Didik Baru) (`/api/ppdb`)](#20-modul-ppdb-penerimaan-peserta-didik-baru-apippdb)
    - [20.1 Konsep Staging Area & Alur Bisnis](#201-konsep-staging-area--alur-bisnis)
    - [20.2 Registrasi Akun Calon Siswa (`POST /api/ppdb/register-account`)](#202-registrasi-akun-calon-siswa)
    - [20.3 Login Calon Siswa (`POST /api/ppdb/login`)](#203-login-calon-siswa)
    - [20.4 Status Pendaftaran Calon Siswa (`GET /api/ppdb/my-registration`)](#204-status-pendaftaran-calon-siswa)
    - [20.5 Unggah Bukti Pembayaran (`POST /api/ppdb/upload-payment`)](#205-unggah-bukti-pembayaran)
    - [20.6 Pengisian Formulir Pendaftaran Bersarang (`PUT /api/ppdb/registration-form`)](#206-pengisian-formulir-pendaftaran-bersarang)
    - [20.7 Monitoring Seluruh Pendaftar PPDB (`GET /api/ppdb/registrations`)](#207-monitoring-seluruh-pendaftar-ppdb-admin)
    - [20.8 Detail Pendaftar PPDB (`GET /api/ppdb/registrations/{id}`)](#208-detail-pendaftar-ppdb-admin)
    - [20.9 Verifikasi Pembayaran (`PUT /api/ppdb/verify-payment/{id}`)](#209-verifikasi-pembayaran-admin)
    - [20.10 Penerimaan Siswa & Migrasi Otomatis ke Master SIAKAD (`POST /api/ppdb/accept/{id}`)](#2010-penerimaan-siswa--migrasi-otomatis-ke-master-siakad-admin)
21. [Standar Format Error Response & HTTP Status Code](#21-standar-format-error-response--http-status-code)

---

## 1. IKHTISAR & KONVENSI GLOBAL

* **Base URL**: `http://127.0.0.1:8000` (development) atau URL domain server produksi.
* **Format Data**: 
  * JSON (`application/json`) untuk mayoritas request body dan seluruh response JSON.
  * Form URL-Encoded (`application/x-www-form-urlencoded`) khusus pada endpoint login (`/api/auth/login`).
  * Multipart Form Data (`multipart/form-data`) pada endpoint unggah berkas (`/api/uploads/*`).
* **Format Identifier (ID)**: UUID v4 standar (contoh: `3fa85f64-5717-4562-b3fc-2c963f66afa6`).
* **Format Tanggal & Waktu**:
  * Tanggal (`Date`): Format `YYYY-MM-DD` (contoh: `2026-09-02`).
  * Waktu (`Time`): Format `HH:MM:SS` (contoh: `07:30:00`).
  * Timestamp: Format ISO 8601 UTC (contoh: `2026-09-02T08:00:00Z` atau dengan mikrodetik).
* **Dokumentasi Interaktif**:
  * Swagger UI: `http://127.0.0.1:8000/docs`
  * Redoc: `http://127.0.0.1:8000/redoc`

---

## 2. AUTENTIKASI & OTORISASI BERBASIS PERAN (RBAC)

API menggunakan protokol **JSON Web Token (JWT) Bearer Token**.

### Header Autentikasi Wajib:
```http
Authorization: Bearer <access_token>
```

### Resolusi Peran (Role Resolution):
Sistem mengimplementasikan resolusi peran dinamis (`resolve_user_roles`):
1. **`admin`**: Akun Administrator Sistem yang secara otomatis mewarisi hak akses `admin`, `staff`, `teacher`, dan `employee`.
2. **`teacher` / `employee` / `staff`**: Pegawai/Guru yang memiliki hak akses membaca data sekolah, mengelola pembelajaran, serta hak akses tambahan sesuai dengan **jabatan aktif** yang diembannya (contoh kode jabatan: `CURRICULUM`, `HEAD_OF_MAJOR`, `PRINCIPAL`, `STAFF_TU`). Jika ditugaskan sebagai wali kelas aktif, pengguna otomatis mendapatkan role tambahan `homeroom_teacher` / `wali_kelas`.
3. **`student`**: Siswa sekolah dengan hak akses ke materi, tugas, portofolio, absensi pribadi, dan nilai rapor pribadi.
4. **`parent`**: Orang tua / wali siswa dengan akses memantau perkembangan akademik dan presensi anak.

### Level Satpam RBAC (Role Checker):
* **`require_admin`**: Hanya boleh diakses oleh pengguna dengan role `admin`.
* **`require_staff`**: Boleh diakses oleh `admin`, `teacher`, `employee`, dan `staff`.
* **`require_teacher`**: Boleh diakses oleh `admin` dan `teacher`.
* **`require_all`**: Boleh diakses oleh semua pengguna yang telah terautentikasi (`admin`, `teacher`, `employee`, `staff`, `student`, `parent`).
* **`get_current_user`**: Memverifikasi token JWT aktif tanpa membatasi role.

---

## 3. ROOT ENDPOINT

### `GET /`
Mengembalikan pesan selamat datang, versi aplikasi, serta tautan dokumentasi OpenAPI.

* **Akses**: Publik
* **Response `200 OK`**:
```json
{
  "message": "Welcome to EduSphere SIAKAD & LMS API",
  "version": "2.0.0",
  "docs_url": "/docs",
  "redoc_url": "/redoc"
}
```

---

## 4. MODUL AUTENTIKASI (`/api/auth`)

### 4.1 Login Pengguna (Mendapatkan JWT Token)
* **Endpoint**: `POST /api/auth/login`
* **Content-Type**: `application/x-www-form-urlencoded`
* **Akses**: Publik

#### Request Body (Form Data):
| Field | Tipe | Wajib | Deskripsi |
|---|---|---|---|
| `username` | string | Ya | Username akun pengguna |
| `password` | string | Ya | Password akun dalam teks biasa |

#### Response `200 OK`:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsInJvbGVzIjpbImFkbWluIiwic3RhZmYiLCJ0ZWFjaGVyIiwiZW1wbG95ZWUiXX0...",
  "token_type": "bearer",
  "role": "admin",
  "roles": [
    "admin",
    "staff",
    "teacher",
    "employee"
  ]
}
```

#### Kemungkinan Error:
* `401 Unauthorized`: `"Incorrect username or password"` jika username tidak ditemukan atau password salah.
* `400 Bad Request`: `"Inactive user"` jika akun berstatus dinonaktifkan (`is_active: false`).

---

## 5. MODUL PENGGUNA / USER MANAGEMENT (`/api/users`)
*Otorisasi: Seluruh endpoint di bawah ini dikunci khusus **`require_admin`**.*

### 5.1 Tambah Pengguna Baru
* **Endpoint**: `POST /api/users/`
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Deskripsi & Validasi |
|---|---|---|---|
| `username` | string | Ya | Username unik (maks. 50 karakter) |
| `password` | string | Ya | Password teks biasa (akan di-hash dengan bcrypt) |
| `email` | string | Tidak | Alamat email unik pengguna |
| `role` | string | Tidak | Default: `"student"`. Pilihan: `"admin"`, `"teacher"`, `"employee"`, `"staff"`, `"student"`, `"parent"` |
| `school_id` | UUID | Tidak | ID sekolah yang terhubung |
| `is_active` | boolean | Tidak | Status aktif akun (default: `true`) |

```json
{
  "username": "guru_matematika",
  "password": "PasswordKuat123!",
  "email": "guru.math@sekolah.sch.id",
  "role": "teacher",
  "school_id": "7fa12345-1111-2222-3333-444455556666",
  "is_active": true
}
```

#### Response `201 Created`:
```json
{
  "id": "e6ce8ff7-be4b-47ef-9850-8bf848d58a7e",
  "username": "guru_matematika",
  "email": "guru.math@sekolah.sch.id",
  "role": "teacher",
  "school_id": "7fa12345-1111-2222-3333-444455556666",
  "is_active": true,
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z"
}
```

### 5.2 Ambil Seluruh Pengguna
* **Endpoint**: `GET /api/users/`
* **Response `200 OK`**: Array of User Object (seperti pada respons 5.1).

### 5.3 Ambil Detail Pengguna
* **Endpoint**: `GET /api/users/{user_id}`
* **Path Parameter**: `user_id` (UUID)
* **Response `200 OK`**: User Object tunggal.
* **Error**: `404 Not Found` jika ID pengguna tidak ditemukan.

### 5.4 Update Pengguna
* **Endpoint**: `PUT /api/users/{user_id}`
* **Path Parameter**: `user_id` (UUID)

#### Request Body (JSON - Semua Field Opsional):
```json
{
  "username": "guru_matematika_baru",
  "email": "guru.math.baru@sekolah.sch.id",
  "role": "teacher",
  "password": "PasswordBaru456!",
  "is_active": true,
  "school_id": "7fa12345-1111-2222-3333-444455556666"
}
```

#### Response `200 OK`: User Object yang telah diperbarui.

### 5.5 Hapus Pengguna
* **Endpoint**: `DELETE /api/users/{user_id}`
* **Path Parameter**: `user_id` (UUID)
* **Response `204 No Content`**

---

## 6. MODUL PROFIL PENGGUNA & KEAMANAN AKUN (`/api/profile`)
*Otorisasi: **`require_all`** (Pengguna login siapa saja).*

### 6.1 Ambil Profil Pengguna Login
* **Endpoint**: `GET /api/profile/me`
* **Deskripsi**: Mengembalikan rincian data akun yang sedang login beserta relasi profil pegawai (lengkap dengan jabatan aktif) atau profil siswa.

#### Response `200 OK` (Contoh Akun Pegawai / Guru):
```json
{
  "id": "e6ce8ff7-be4b-47ef-9850-8bf848d58a7e",
  "username": "hendra_guru",
  "email": "hendra@sekolah.sch.id",
  "base_role": "teacher",
  "role": "teacher",
  "roles": ["teacher", "employee", "staff", "curriculum", "wali_kelas"],
  "is_active": true,
  "school_id": "7fa12345-1111-2222-3333-444455556666",
  "created_at": "2026-09-02T08:00:00Z",
  "employee_profile": {
    "id": "a2054fda-a7fb-4825-8bfc-a7909aec3d6a",
    "nip": "197504122000031001",
    "full_name": "Drs. Hendra Gunawan, M.Pd.",
    "employment_status": "PNS",
    "ptk_type": "Guru Mapel",
    "is_active": true,
    "active_positions": [
      {
        "id": "4b6c8d1e-2f3a-4e5b-6c7d-8e9f0a1b2c3d",
        "name": "Wakil Kepala Kurikulum",
        "code": "CURRICULUM",
        "is_structural": true
      }
    ]
  },
  "student_profile": null
}
```

### 6.2 Perbarui Profil Akun Sendiri
* **Endpoint**: `PUT /api/profile/me`
* **Request Body (JSON)**:
```json
{
  "email": "hendra.baru@sekolah.sch.id",
  "full_name": "Dr. Hendra Gunawan, M.Pd."
}
```
* **Response `200 OK`**:
```json
{
  "message": "Profil berhasil diperbarui",
  "username": "hendra_guru",
  "email": "hendra.baru@sekolah.sch.id"
}
```

### 6.3 Ganti Password Akun Sendiri
* **Endpoint**: `PUT /api/profile/change-password`
* **Request Body (JSON)**:
```json
{
  "old_password": "PasswordLama123!",
  "new_password": "PasswordBaruKuat456!"
}
```
* **Validasi**: `old_password` dan `new_password` minimal 6 karakter.
* **Response `200 OK`**:
```json
{
  "message": "Password berhasil diubah"
}
```
* **Error**: `400 Bad Request` jika password lama tidak cocok.

---

## 7. MODUL STATISTIK DASHBOARD (`/api/dashboard`)

### 7.1 Statistik Agregat Dashboard
* **Endpoint**: `GET /api/dashboard/stats`
* **Akses**: `require_all` (Seluruh pengguna login)
* **Response `200 OK`**:
```json
{
  "total_students": 1250,
  "total_teachers": 84,
  "total_classrooms": 36,
  "total_subjects": 48,
  "total_assignments": 320,
  "total_materials": 540,
  "total_announcements": 15
}
```

---

## 8. MODUL IDENTITAS SEKOLAH (`/api/schools`)

### 8.1 Simpan / Perbarui Identitas Sekolah (Single Identity)
* **Endpoint**: `POST /api/schools/`
* **Akses**: `require_admin`
* **Status**: `201 Created` / `200 OK`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `name` | string | Ya | Nama resmi sekolah (maks. 100 char) |
| `npsn` | string | Ya | Nomor Pokok Sekolah Nasional (maks. 10 char) |
| `address` | string | Ya | Alamat lengkap sekolah |

```json
{
  "name": "SMK Negeri 1 Jakarta",
  "npsn": "20101234",
  "address": "Jl. Budi Utomo No. 7, Sawah Besar, Jakarta Pusat"
}
```

#### Response `201 Created`:
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

### 8.2 Ambil Profil Sekolah
* **Endpoint**: `GET /api/schools/`
* **Akses**: `require_staff`
* **Response `200 OK`**: School Object tunggal.

---

## 9. MODUL DATA MASTER (`/api/master`)
*Otorisasi Global: Seluruh endpoint write (`POST`, `PUT`, `DELETE`) dan read (`GET`) pada modul ini dikunci oleh **`require_admin`**.*

### 9.1 Tahun Ajaran (Academic Years)
* **URL Base**: `/api/master/academic-years/`

| Method | Endpoint | Deskripsi | Request Body / Params | Response Status |
|---|---|---|---|---|
| `POST` | `/api/master/academic-years/` | Tambah Tahun Ajaran | `start_year` (int), `end_year` (int), `is_active` (bool) | `201 Created` |
| `GET` | `/api/master/academic-years/` | Daftar Seluruh Tahun Ajaran | - | `200 OK` (Array) |
| `PUT` | `/api/master/academic-years/{id}` | Update Tahun Ajaran | `start_year`, `end_year`, `is_active` | `200 OK` |
| `DELETE`| `/api/master/academic-years/{id}` | Hapus Tahun Ajaran | - | `204 No Content` |

#### Contoh Payload Request POST:
```json
{
  "start_year": 2025,
  "end_year": 2026,
  "is_active": true
}
```

#### Contoh Response `201 Created`:
```json
{
  "id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
  "start_year": 2025,
  "end_year": 2026,
  "is_active": true,
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z"
}
```

---

### 9.2 Semester
* **URL Base**: `/api/master/semesters/`

| Method | Endpoint | Deskripsi | Request Body / Params | Response Status |
|---|---|---|---|---|
| `POST` | `/api/master/semesters/` | Tambah Semester | `academic_year_id` (UUID), `name` (str: `"Odd"`/`"Even"`/`"Ganjil"`/`"Genap"`), `is_active` (bool) | `201 Created` |
| `GET` | `/api/master/semesters/` | Daftar Seluruh Semester | - | `200 OK` (Array) |
| `PUT` | `/api/master/semesters/{id}` | Update Semester | Sama dengan schema POST | `200 OK` |
| `DELETE`| `/api/master/semesters/{id}` | Hapus Semester | - | `204 No Content` |

#### Contoh Payload Request POST:
```json
{
  "academic_year_id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
  "name": "Ganjil",
  "is_active": true
}
```

---

### 9.3 Gedung (Buildings)
* **URL Base**: `/api/master/buildings/`

| Method | Endpoint | Deskripsi | Request Body / Params | Response Status |
|---|---|---|---|---|
| `POST` | `/api/master/buildings/` | Tambah Data Gedung | `name` (str), `established_year` (int?), `area` (float?), `width` (float?), `height` (float?), `is_active` (bool) | `201 Created` |
| `GET` | `/api/master/buildings/` | Daftar Seluruh Gedung | - | `200 OK` (Array) |
| `PUT` | `/api/master/buildings/{id}` | Update Data Gedung | Sama dengan schema POST | `200 OK` |
| `DELETE`| `/api/master/buildings/{id}` | Hapus Gedung | - | `204 No Content` |

#### Contoh Payload Request POST:
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

---

### 9.4 Ruang Kelas (Classrooms)
* **URL Base**: `/api/master/classrooms/`

| Method | Endpoint | Deskripsi | Request Body / Params | Response Status |
|---|---|---|---|---|
| `POST` | `/api/master/classrooms/` | Tambah Ruang Kelas | `building_id` (UUID), `name` (str), `area` (float?), `width` (float?), `height` (float?), `is_active` (bool) | `201 Created` |
| `GET` | `/api/master/classrooms/` | Daftar Seluruh Kelas | - | `200 OK` (Array) |
| `PUT` | `/api/master/classrooms/{id}` | Update Data Kelas | Sama dengan schema POST | `200 OK` |
| `DELETE`| `/api/master/classrooms/{id}` | Hapus Ruang Kelas | - | `204 No Content` |

#### Contoh Payload Request POST:
```json
{
  "building_id": "71006039-8458-488d-9868-b2a27fa8fa55",
  "name": "Kelas 10 RPL 1",
  "area": 64.0,
  "width": 8.0,
  "height": 8.0,
  "is_active": true
}
```

---

### 9.5 Mata Pelajaran (Subjects)
* **URL Base**: `/api/master/subjects/`

| Method | Endpoint | Deskripsi | Request Body / Params | Response Status |
|---|---|---|---|---|
| `POST` | `/api/master/subjects/` | Tambah Mata Pelajaran | `name` (str), `lesson_hours` (int), `is_active` (bool) | `201 Created` |
| `GET` | `/api/master/subjects/` | Daftar Seluruh Mapel | - | `200 OK` (Array) |
| `PUT` | `/api/master/subjects/{id}` | Update Mata Pelajaran | Sama dengan schema POST | `200 OK` |
| `DELETE`| `/api/master/subjects/{id}` | Hapus Mata Pelajaran | - | `204 No Content` |

#### Contoh Payload Request POST:
```json
{
  "name": "Pemrograman Web & Perangkat Bergerak",
  "lesson_hours": 6,
  "is_active": true
}
```

---

## 10. MODUL JABATAN PEGAWAI (`/api/positions`)

### 10.1 Master Jabatan

#### 10.1.1 Tambah Jabatan Baru
* **Endpoint**: `POST /api/positions/`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Request Body (JSON)**:
  * `name` (string, wajib): Nama jabatan (contoh: `"Wakil Kepala Bidang Kurikulum"`).
  * `code` (string, opsional, maks. 50): Kode referensi RBAC (contoh: `"CURRICULUM"`, `"HEAD_OF_MAJOR"`, `"STAFF_TU"`).
  * `is_structural` (boolean, opsional, default: `false`): Jabatan struktural.
  * `is_active` (boolean, opsional, default: `true`): Status keaktifan jabatan.

```json
{
  "name": "Kepala Program Keahlian RPL",
  "code": "HEAD_OF_MAJOR",
  "is_structural": true,
  "is_active": true
}
```

#### 10.1.2 Ambil Seluruh Jabatan
* **Endpoint**: `GET /api/positions/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of Position Objects.

#### 10.1.3 Ambil Detail Jabatan
* **Endpoint**: `GET /api/positions/{position_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Position Object.

#### 10.1.4 Update Jabatan
* **Endpoint**: `PUT /api/positions/{position_id}`
* **Akses**: `require_admin`
* **Request Body**: Semua field opsional (`name`, `code`, `is_structural`, `is_active`).
* **Response `200 OK`**: Position Object diperbarui.

#### 10.1.5 Hapus Jabatan
* **Endpoint**: `DELETE /api/positions/{position_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 10.2 Penugasan Jabatan Pegawai (Employee Positions)

#### 10.2.1 Tetapkan Jabatan ke Pegawai
* **Endpoint**: `POST /api/positions/employee/`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Request Body (JSON)**:
  * `employee_id` (UUID, wajib): ID Pegawai.
  * `position_id` (UUID, wajib): ID Jabatan.
  * `academic_year_id` (UUID, wajib): ID Tahun Ajaran penugasan.
  * `is_active` (boolean, opsional, default: `true`): Status keaktifan tugas.

```json
{
  "employee_id": "a2054fda-a7fb-4825-8bfc-a7909aec3d6a",
  "position_id": "4b6c8d1e-2f3a-4e5b-6c7d-8e9f0a1b2c3d",
  "academic_year_id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
  "is_active": true
}
```

#### 10.2.2 Ambil Riwayat Jabatan Milik Pegawai
* **Endpoint**: `GET /api/positions/employee/{employee_id}`
* **Akses**: `require_staff`
* **Path Parameter**: `employee_id` (UUID)
* **Response `200 OK`**: Array of EmployeePosition Objects.

#### 10.2.3 Update Status / Data Penugasan Jabatan
* **Endpoint**: `PUT /api/positions/employee/{assign_id}`
* **Akses**: `require_admin`
* **Request Body (JSON)**: `is_active` (bool?), `position_id` (UUID?), `academic_year_id` (UUID?).
* **Response `200 OK`**: EmployeePosition Object.

#### 10.2.4 Hapus Riwayat Penugasan Jabatan
* **Endpoint**: `DELETE /api/positions/employee/{assign_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

## 11. MODUL PENJADWALAN & WALI KELAS (`/api/schedules`)

### 11.1 Jadwal Mengajar (Teaching Schedules)

#### 11.1.1 Buat Jadwal Mengajar
* **Endpoint**: `POST /api/schedules/teaching/`
* **Akses**: `require_admin`
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `employee_id` | UUID | Ya | ID Guru pengajar |
| `subject_id` | UUID | Ya | ID Mata Pelajaran |
| `classroom_id` | UUID | Ya | ID Ruang Kelas |
| `academic_year_id` | UUID | Ya | ID Tahun Ajaran |
| `semester_id` | UUID | Ya | ID Semester |
| `day_of_week` | string | Ya | Nama hari (contoh: `"Senin"`, `"Selasa"`) |
| `start_time` | string (time) | Ya | Jam mulai format `HH:MM:SS` (contoh: `"07:30:00"`) |
| `end_time` | string (time) | Ya | Jam selesai format `HH:MM:SS` (contoh: `"09:45:00"`) |

```json
{
  "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
  "subject_id": "63df9d9a-8e34-4812-b95b-fa5f15fc4b90",
  "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
  "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d",
  "semester_id": "ee40b194-5b69-4258-ae43-d882c2470817",
  "day_of_week": "Senin",
  "start_time": "07:30:00",
  "end_time": "09:45:00"
}
```

#### 11.1.2 Ambil Seluruh Jadwal Mengajar
* **Endpoint**: `GET /api/schedules/teaching/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of TeachingSchedule Objects.

#### 11.1.3 Ambil Jadwal Mengajar Berdasarkan Guru
* **Endpoint**: `GET /api/schedules/teaching/employee/{employee_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of TeachingSchedule Objects milik guru terkait.

#### 11.1.4 Hapus Jadwal Mengajar
* **Endpoint**: `DELETE /api/schedules/teaching/{schedule_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 11.2 Penugasan Wali Kelas (Homeroom Assignments)

#### 11.2.1 Tugaskan Wali Kelas
* **Endpoint**: `POST /api/schedules/homeroom/`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Request Body (JSON)**:
```json
{
  "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
  "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
  "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d"
}
```

#### 11.2.2 Ambil Seluruh Penugasan Wali Kelas
* **Endpoint**: `GET /api/schedules/homeroom/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of HomeroomAssignment Objects.

#### 11.2.3 Ambil Riwayat Wali Kelas Berdasarkan Ruang Kelas
* **Endpoint**: `GET /api/schedules/homeroom/classroom/{classroom_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of HomeroomAssignment Objects pada kelas tsb.

#### 11.2.4 Hapus Penugasan Wali Kelas
* **Endpoint**: `DELETE /api/schedules/homeroom/{assignment_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

## 12. MODUL DATA SISWA

Struktur data siswa didesain modular guna mendukung formulir pendaftaran bertahap (multi-step wizard).

### 12.1 Biodata Pokok Siswa (`/api/students`)

#### 12.1.1 Tambah Siswa Baru
* **Endpoint**: `POST /api/students/`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Fitur Otomatis**: Jika `user_id` tidak disertakan, sistem otomatis membuatkan akun `users` baru menggunakan `username` (atau `nisn`) dengan password default `"siswa123"`.

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `nik` | string | Ya | 16 digit NIK unik |
| `nisn` | string | Ya | 5-20 digit NISN unik |
| `full_name` | string | Ya | Nama lengkap siswa |
| `first_name` | string | Tidak | Nama depan (otomatis dipisah dari full_name jika kosong) |
| `last_name` | string | Tidak | Nama belakang (otomatis dipisah jika kosong) |
| `school_id` | UUID | Tidak | ID Sekolah terkait |
| `user_id` | UUID | Tidak | ID akun user yang sudah dibuat sebelumnya |
| `username` | string | Tidak | Username akun jika ingin dibuat otomatis |
| `password` | string | Tidak | Password awal akun siswa (default: `"siswa123"`) |
| `email` | string | Tidak | Email akun siswa |

```json
{
  "nik": "3201012345670001",
  "nisn": "0051234567",
  "full_name": "Ahmad Fauzi Rahman",
  "school_id": "7fa12345-1111-2222-3333-444455556666",
  "username": "ahmad_fauzi",
  "email": "ahmad.fauzi@student.sch.id"
}
```

#### Response `201 Created`:
```json
{
  "id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
  "user_id": "b1545031-4ecb-4b63-b576-bf01a4430aac",
  "school_id": "7fa12345-1111-2222-3333-444455556666",
  "nik": "3201012345670001",
  "nisn": "0051234567",
  "full_name": "Ahmad Fauzi Rahman",
  "first_name": "Ahmad",
  "last_name": "Fauzi Rahman",
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z"
}
```

#### 12.1.2 Ambil Daftar Semua Siswa
* **Endpoint**: `GET /api/students/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of StudentResponse (diurutkan berdasarkan nama siswa).

#### 12.1.3 Ambil Detail Lengkap Siswa (Agregasi Seluruh Relasi)
* **Endpoint**: `GET /api/students/{student_id}`
* **Akses**: `require_staff`
* **Deskripsi**: Menampilkan biodata pokok siswa berserta objek relasi `identity`, `address`, `contact`, dan daftar seluruh orang tua / wali di `student_parents`.

#### Response `200 OK`:
```json
{
  "id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
  "user_id": "b1545031-4ecb-4b63-b576-bf01a4430aac",
  "school_id": "7fa12345-1111-2222-3333-444455556666",
  "nik": "3201012345670001",
  "nisn": "0051234567",
  "full_name": "Ahmad Fauzi Rahman",
  "first_name": "Ahmad",
  "last_name": "Fauzi Rahman",
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z",
  "identity": {
    "id": "f1234567-89ab-cdef-0123-456789abcdef",
    "family_card_number": "3201010000000001",
    "gender": "Laki-laki",
    "religion": "Islam",
    "place_of_birth": "Jakarta",
    "date_of_birth": "2008-05-14"
  },
  "address": {
    "id": "a9876543-210f-edcb-a987-6543210fedcb",
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
    "id": "c1112223-3334-4445-5556-666777888999",
    "phone_number": "021-77889900",
    "mobile_number": "081234567890",
    "whatsapp_number": "081234567890",
    "email": "ahmad.fauzi@student.sch.id"
  },
  "student_parents": [
    {
      "relationship_type": 1,
      "parent": {
        "id": "p8889990-1112-2233-4455-66778899aabb",
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
```

#### 12.1.4 Update Biodata Pokok Siswa
* **Endpoint**: `PUT /api/students/{student_id}`
* **Akses**: `require_admin`
* **Request Body (JSON)**: `nik`, `nisn`, `full_name`, `first_name`, `last_name`, `school_id`, `user_id` (semua opsional).
* **Response `200 OK`**: Student Object diperbarui.

#### 12.1.5 Hapus Data Siswa
* **Endpoint**: `DELETE /api/students/{student_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 12.2 Identitas Tambahan Siswa (`/api/identities`)

#### 12.2.1 Simpan / Perbarui Identitas Siswa
* **Endpoint**: `POST /api/identities/{student_id}`
* **Akses**: `get_current_user` (Pengguna login)
* **Status**: `201 Created` / `200 OK` (Upsert otomatis)

#### Request Body (JSON):
```json
{
  "family_card_number": "3201010000000001",
  "gender": "Laki-laki",
  "religion": "Islam",
  "place_of_birth": "Jakarta",
  "date_of_birth": "2008-05-14"
}
```

#### 12.2.2 Ambil Identitas Tambahan Siswa
* **Endpoint**: `GET /api/identities/{student_id}`
* **Akses**: `get_current_user`
* **Response `200 OK`**: StudentIdentity Object.

---

### 12.3 Alamat Siswa (`/api/addresses`)

#### 12.3.1 Simpan / Perbarui Alamat Siswa
* **Endpoint**: `POST /api/addresses/{student_id}`
* **Akses**: `get_current_user`
* **Status**: `201 Created` / `200 OK` (Upsert otomatis)

#### Request Body (JSON):
```json
{
  "street_address": "Jl. Merdeka No. 45",
  "rt": "002",
  "rw": "005",
  "village": "Sukamaju",
  "district": "Cilodong",
  "postal_code": "16415",
  "residence_type": "Bersama Orang Tua",
  "transportation_mode": "Sepeda Motor"
}
```

#### 12.3.2 Ambil Alamat Siswa
* **Endpoint**: `GET /api/addresses/{student_id}`
* **Akses**: `get_current_user`
* **Response `200 OK`**: StudentAddress Object.

---

### 12.4 Kontak Siswa (`/api/contacts`)

#### 12.4.1 Simpan / Perbarui Kontak Siswa
* **Endpoint**: `POST /api/contacts/{student_id}`
* **Akses**: `get_current_user`
* **Status**: `201 Created` / `200 OK` (Upsert otomatis)

#### Request Body (JSON):
```json
{
  "phone_number": "021-77889900",
  "mobile_number": "081234567890",
  "whatsapp_number": "081234567890",
  "email": "ahmad.fauzi@student.sch.id"
}
```

#### 12.4.2 Ambil Kontak Siswa
* **Endpoint**: `GET /api/contacts/{student_id}`
* **Akses**: `get_current_user`
* **Response `200 OK`**: StudentContact Object.

---

### 12.5 Orang Tua / Wali Siswa (`/api/parents`)

#### 12.5.1 Tambah Orang Tua / Wali untuk Siswa
* **Endpoint**: `POST /api/parents/{student_id}`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Keunggulan**: Jika NIK orang tua sudah ada (misal saudara kandung terdaftar di sekolah yang sama), sistem secara otomatis mengaitkan ID orang tua yang sama tanpa membuat duplikasi entri master parent.

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `relationship_type` | integer | Ya | `1`: Ayah Kandung, `2`: Ibu Kandung, `3`: Wali |
| `full_name` | string | Ya | Nama lengkap orang tua (maks. 100 char) |
| `nik` | string | Tidak | NIK orang tua (16 digit) |
| `place_of_birth` | string | Tidak | Tempat lahir |
| `birth_year` | string | Tidak | Tahun lahir (4 digit, contoh: `"1978"`) |
| `education_code` | string | Tidak | Kode pendidikan Dapodik (contoh: `"05"`) |
| `occupation_code` | string | Tidak | Kode pekerjaan Dapodik (contoh: `"02"`) |
| `income_code` | string | Tidak | Kode penghasilan Dapodik (contoh: `"03"`) |
| `special_need_code`| string | Tidak | Kode kebutuhan khusus (contoh: `"00"`) |
| `address` | string | Tidak | Alamat tempat tinggal |
| `phone_number` | string | Tidak | Nomor telepon rumah/kantor |
| `whatsapp_number` | string | Tidak | Nomor kontak WhatsApp |

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
  "address": "Jl. Merdeka No. 45",
  "phone_number": "081311223344",
  "whatsapp_number": "081311223344"
}
```

#### 12.5.2 Ambil Seluruh Orang Tua Siswa
* **Endpoint**: `GET /api/parents/{student_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of StudentParentRelationResponse (relasi + objek parent).

#### 12.5.3 Hapus Tautan Relasi Orang Tua Siswa
* **Endpoint**: `DELETE /api/parents/relation/{relation_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 12.6 Riwayat Kelas & Enrollment (`/api/enrollments`)

#### 12.6.1 Daftarkan Siswa ke Kelas (Enrollment)
* **Endpoint**: `POST /api/enrollments/`
* **Akses**: `require_admin`
* **Status**: `201 Created`

#### Request Body (JSON):
```json
{
  "student_id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
  "classroom_id": "cd65245e-120b-49f5-bde5-41fc13a5f3b5",
  "academic_year_id": "e56b931d-abf0-48c1-bda8-710fb41ff975",
  "semester_id": "8ae202db-fe9d-4661-b4f3-193e8ce3928c",
  "status": "Active"
}
```

#### 12.6.2 Ambil Seluruh Data Pendaftaran Kelas
* **Endpoint**: `GET /api/enrollments/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of StudentEnrollmentResponse.

#### 12.6.3 Ambil Riwayat Kelas per Siswa
* **Endpoint**: `GET /api/enrollments/student/{student_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of StudentEnrollmentResponse milik siswa tsb.

#### 12.6.4 Hapus Riwayat Pendaftaran Siswa
* **Endpoint**: `DELETE /api/enrollments/{enrollment_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

## 13. MODUL DATA PEGAWAI / GURU

### 13.1 Biodata Pokok Pegawai (`/api/employees`)

#### 13.1.1 Tambah Pegawai Baru
* **Endpoint**: `POST /api/employees/`
* **Akses**: `require_admin`
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `full_name` | string | Ya | Nama lengkap dan gelar (maks. 100 char) |
| `nik` | string | Ya | 16 digit NIK unik |
| `gender` | string | Ya | Jenis kelamin (`"Laki-laki"` / `"Perempuan"`) |
| `place_of_birth` | string | Ya | Tempat lahir |
| `date_of_birth` | date | Ya | Tanggal lahir (`YYYY-MM-DD`) |
| `mother_maiden_name`| string | Ya | Nama ibu kandung |
| `employment_status` | string | Ya | Status kerja (contoh: `"PNS"`, `"GTY"`, `"Honorer"`) |
| `ptk_type` | string | Ya | Jenis PTK (contoh: `"Guru Mapel"`, `"Tenaga Kependidikan"`) |
| `user_id` | UUID | Tidak | ID akun `users` jika sudah ada |
| `school_id` | UUID | Tidak | ID sekolah penempatan |
| `nip` | string | Tidak | NIP Pegawai Negeri Sipil (unik) |
| `niy` | string | Tidak | Nomor Induk Yayasan (unik) |
| `nuptk` | string | Tidak | NUPTK resmi Kemendikbudristek (unik) |
| `appointment_decree`| string| Tidak | Nomor SK Pengangkatan |
| `appointment_start_date`| date| Tidak| TMT Pengangkatan (`YYYY-MM-DD`) |
| `appointing_institution`| str | Tidak | Lembaga pengangkat |
| `cpns_decree` | string | Tidak | Nomor SK CPNS |
| `pns_start_date` | date | Tidak | TMT PNS (`YYYY-MM-DD`) |
| `rank_class` | string | Tidak | Golongan/Pangkat (contoh: `"IV/a"`, `"III/c"`) |
| `salary_source` | string | Tidak | Sumber gaji (contoh: `"APBD"`, `"Yayasan"`, `"BOS"`) |
| `employee_card_number`| str | Tidak | Nomor Kartu Pegawai (Karpeg) |
| `is_active` | boolean| Tidak | Status aktif pegawai (default: `true`) |

```json
{
  "full_name": "Drs. Hendra Gunawan, M.Pd.",
  "nik": "3276011204750002",
  "gender": "Laki-laki",
  "place_of_birth": "Bandung",
  "date_of_birth": "1975-04-12",
  "mother_maiden_name": "Siti Maryam",
  "employment_status": "PNS",
  "ptk_type": "Guru Mapel",
  "nip": "197504122000031001",
  "nuptk": "1234567890123456",
  "rank_class": "IV/a",
  "salary_source": "APBD",
  "is_active": true
}
```

#### 13.1.2 Ambil Seluruh Pegawai
* **Endpoint**: `GET /api/employees/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of EmployeeResponse.

#### 13.1.3 Ambil Detail Pegawai
* **Endpoint**: `GET /api/employees/{employee_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: EmployeeResponse Object.

#### 13.1.4 Update Pegawai
* **Endpoint**: `PUT /api/employees/{employee_id}`
* **Akses**: `require_admin`
* **Request Body**: Semua field Employee bersifat opsional.
* **Response `200 OK`**: EmployeeResponse Object.

#### 13.1.5 Hapus Pegawai
* **Endpoint**: `DELETE /api/employees/{employee_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 13.2 Identitas Tambahan Pegawai (`/api/employee-identities`)

#### 13.2.1 Tambah Identitas Pegawai (One-to-One)
* **Endpoint**: `POST /api/employee-identities/`
* **Akses**: `require_admin`
* **Status**: `201 Created`

#### Request Body (JSON):
```json
{
  "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
  "street_address": "Komp. Guru No. 12",
  "rt": "001",
  "rw": "003",
  "hamlet": "Dusun Melati",
  "village": "Pasir Putih",
  "district": "Sawangan",
  "postal_code": "16519",
  "latitude": -6.41234567,
  "longitude": 106.78901234,
  "family_card_number": "3276010000000001",
  "religion": "Islam",
  "citizenship": "WNI",
  "marital_status": "Kawin",
  "spouse_name": "Dewi Sartika",
  "tax_number": "09.123.456.7-412.000",
  "tax_holder_name": "Hendra Gunawan",
  "bank_name": "Bank BJB",
  "bank_account_number": "0012345678901"
}
```

#### 13.2.2 Ambil Seluruh Identitas Pegawai
* **Endpoint**: `GET /api/employee-identities/`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of EmployeeIdentityResponse.

#### 13.2.3 Ambil Identitas Berdasarkan ID
* **Endpoint**: `GET /api/employee-identities/{identity_id}`
* **Akses**: `require_staff`

#### 13.2.4 Ambil Identitas Berdasarkan Employee ID
* **Endpoint**: `GET /api/employee-identities/employee/{employee_id}`
* **Akses**: `require_staff`
* **Deskripsi**: Sangat cocok digunakan untuk fetching detail profil pegawai di halaman frontend.

#### 13.2.5 Update Identitas Pegawai
* **Endpoint**: `PUT /api/employee-identities/{identity_id}`
* **Akses**: `require_admin`
* **Response `200 OK`**: EmployeeIdentityResponse.

#### 13.2.6 Hapus Identitas Pegawai
* **Endpoint**: `DELETE /api/employee-identities/{identity_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 13.3 Kontak Darurat Pegawai (`/api/employee-contacts`)

#### 13.3.1 Tambah Kontak Pegawai
* **Endpoint**: `POST /api/employee-contacts/`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Request Body (JSON)**:
```json
{
  "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
  "contact_name": "Dewi Sartika",
  "relation": "Istri",
  "phone_number": "081299887766",
  "email": "dewi.sartika@gmail.com",
  "address": "Komp. Guru No. 12",
  "is_emergency_contact": true
}
```

#### 13.3.2 Ambil Seluruh Kontak Pegawai
* **Endpoint**: `GET /api/employee-contacts/`
* **Akses**: `require_staff`

#### 13.3.3 Ambil Kontak Berdasarkan ID
* **Endpoint**: `GET /api/employee-contacts/{contact_id}`
* **Akses**: `require_staff`

#### 13.3.4 Ambil Seluruh Kontak Milik Pegawai Tertentu (One-to-Many)
* **Endpoint**: `GET /api/employee-contacts/employee/{employee_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of EmployeeContactResponse.

#### 13.3.5 Update Kontak Pegawai
* **Endpoint**: `PUT /api/employee-contacts/{contact_id}`
* **Akses**: `require_admin`

#### 13.3.6 Hapus Kontak Pegawai
* **Endpoint**: `DELETE /api/employee-contacts/{contact_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 13.4 Data Anak Pegawai (`/api/employee-children`)

#### 13.4.1 Tambah Data Anak Pegawai
* **Endpoint**: `POST /api/employee-children/`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Request Body (JSON)**:
```json
{
  "employee_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
  "child_name": "Rizky Gunawan",
  "child_status": "Anak Kandung",
  "gender": "Laki-laki",
  "place_of_birth": "Depok",
  "date_of_birth": "2012-08-10",
  "education_level": "SMP",
  "nisn": "0098765432",
  "enrollment_year": "2024"
}
```

#### 13.4.2 Ambil Seluruh Data Anak Pegawai
* **Endpoint**: `GET /api/employee-children/`
* **Akses**: `require_staff`

#### 13.4.3 Ambil Data Anak Berdasarkan ID
* **Endpoint**: `GET /api/employee-children/{child_id}`
* **Akses**: `require_staff`

#### 13.4.4 Ambil Seluruh Anak Milik Pegawai Tertentu
* **Endpoint**: `GET /api/employee-children/employee/{employee_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of EmployeeChildResponse.

#### 13.4.5 Update Data Anak Pegawai
* **Endpoint**: `PUT /api/employee-children/{child_id}`
* **Akses**: `require_admin`

#### 13.4.6 Hapus Data Anak Pegawai
* **Endpoint**: `DELETE /api/employee-children/{child_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 13.5 Pengampu Mata Pelajaran Pegawai (`/api/employees/{id}/subjects`)

Tabel relasi many-to-many antara guru dan mata pelajaran yang diampunya.

#### 13.5.1 Tugaskan Mata Pelajaran ke Guru
* **Endpoint**: `POST /api/employees/{employee_id}/subjects/{subject_id}`
* **Akses**: `require_admin`
* **Status**: `201 Created`
* **Response `201 Created`**:
```json
{
  "detail": "Subject assigned"
}
```

#### 13.5.2 Ambil Daftar Mata Pelajaran yang Diampu Guru
* **Endpoint**: `GET /api/employees/{employee_id}/subjects`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of SubjectResponse.

#### 13.5.3 Hapus Penugasan Mata Pelajaran dari Guru
* **Endpoint**: `DELETE /api/employees/{employee_id}/subjects/{subject_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

## 14. MODUL LMS (LEARNING MANAGEMENT SYSTEM) (`/api/lms`)

### 14.1 Materi Belajar (Materials)

#### 14.1.1 Tambah Materi Baru
* **Endpoint**: `POST /api/lms/materials/`
* **Akses**: `require_staff` (Guru & Admin)
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `subject_id` | UUID | Ya | ID Mata Pelajaran |
| `title` | string | Ya | Judul materi pembelajaran |
| `content` | string | Tidak | Rangkuman / isi materi (Markdown/HTML) |
| `file_path` | string | Tidak | Path file berkas modul (dari endpoint upload) |
| `video_url` | string | Tidak | URL video pembelajaran (contoh: YouTube link) |
| `classroom_id` | UUID | Tidak | Khusus untuk kelas tertentu (jika kosong: seluruh kelas) |
| `academic_year_id`| UUID | Tidak | ID Tahun Ajaran |
| `semester_id` | UUID | Tidak | ID Semester |
| `is_active` | boolean| Tidak | Status rilis materi (default: `true`) |

```json
{
  "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
  "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
  "title": "Pengenalan Aljabar Linier & Matriks",
  "content": "Pada modul ini kita akan membahas dasar eliminasi Gauss...",
  "file_path": "/uploads/materials/aljabar_bab1.pdf",
  "video_url": "https://www.youtube.com/watch?v=example",
  "is_active": true
}
```

#### 14.1.2 Ambil Materi Berdasarkan Mata Pelajaran
* **Endpoint**: `GET /api/lms/materials/subject/{subject_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Array of MaterialResponse yang aktif.

#### 14.1.3 Ambil Detail Materi
* **Endpoint**: `GET /api/lms/materials/{material_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: MaterialResponse Object.

#### 14.1.4 Update Materi
* **Endpoint**: `PUT /api/lms/materials/{material_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: MaterialResponse diperbarui.

#### 14.1.5 Hapus Materi
* **Endpoint**: `DELETE /api/lms/materials/{material_id}`
* **Akses**: `require_staff`
* **Response `204 No Content`**

#### 14.1.6 Tandai Selesai Mempelajari Materi (Siswa)
* **Endpoint**: `POST /api/lms/materials/{material_id}/toggle-complete`
* **Akses**: Siswa (`User` yang memiliki profil `Student`)
* **Deskripsi**: Toggle status baca materi (jika sudah ada maka dihapus, jika belum maka ditambahkan).
* **Response `200 OK`**:
```json
{
  "completed": true,
  "message": "Materi selesai dipelajari"
}
```

---

### 14.2 Tugas (Assignments)

#### 14.2.1 Buat Tugas Baru
* **Endpoint**: `POST /api/lms/assignments/`
* **Akses**: `require_staff`
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `subject_id` | UUID | Ya | ID Mata Pelajaran |
| `classroom_id` | UUID | Ya | ID Kelas target |
| `title` | string | Ya | Judul tugas |
| `description` | string | Ya | Petunjuk & rincian instruksi pengerjaan |
| `type` | string | Tidak | Tipe tugas: `"file"`, `"essay"`, `"quiz"`, `"coding"`, `"project"` (default: `"file"`) |
| `file_path` | string | Tidak | File lampiran soal (PDF/Docx) |
| `deadline` | datetime | Ya | Batas akhir pengumpulan (ISO 8601 UTC) |
| `max_score` | decimal | Tidak | Nilai maksimum (default: `100.00`) |
| `is_active` | boolean | Tidak | Status aktif (default: `true`) |

```json
{
  "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
  "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
  "title": "Tugas 1: Menyelesaikan Sistem Persamaan Linier",
  "description": "Kerjakan latihan pada slide 10-15 dan kumpulkan berkas jawaban PDF.",
  "type": "file",
  "deadline": "2026-09-15T23:59:59Z",
  "max_score": 100.00,
  "is_active": true
}
```

#### 14.2.2 Ambil Tugas Berdasarkan Mata Pelajaran
* **Endpoint**: `GET /api/lms/assignments/subject/{subject_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Array of AssignmentResponse.

#### 14.2.3 Ambil Tugas yang Mendekati Deadline (Upcoming)
* **Endpoint**: `GET /api/lms/assignments/upcoming`
* **Akses**: `require_all`
* **Deskripsi**: Mengambil 10 tugas aktif terdekat yang deadline-nya belum terlewati.
* **Response `200 OK`**: Array of AssignmentResponse (urut berdasarkan deadline terdekat).

#### 14.2.4 Ambil Detail Tugas
* **Endpoint**: `GET /api/lms/assignments/{assignment_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: AssignmentResponse Object.

#### 14.2.5 Update Tugas
* **Endpoint**: `PUT /api/lms/assignments/{assignment_id}`
* **Akses**: `require_staff`
* **Response `200 OK`**: AssignmentResponse diperbarui.

#### 14.2.6 Hapus Tugas
* **Endpoint**: `DELETE /api/lms/assignments/{assignment_id}`
* **Akses**: `require_staff`
* **Response `204 No Content`**

---

### 14.3 Pengumpulan & Penilaian Tugas (Submissions & Grades)

#### 14.3.1 Kumpulkan Tugas (Siswa)
* **Endpoint**: `POST /api/lms/submissions/`
* **Akses**: Khusus Siswa (`Student`)
* **Status**: `201 Created` / `200 OK`
* **Audit Trail**: Jika siswa pernah mengumpulkan sebelumnya (revisi), sistem secara otomatis mencatat berkas dan isi lama ke tabel `submission_histories`.

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `assignment_id` | UUID | Ya | ID Tugas yang dikerjakan |
| `content` | string | Tidak | Teks jawaban, penjelasan, atau tautan Github/Drive |
| `file_path` | string | Tidak | Path file jawaban yang diunggah ke `/api/uploads/document` |
| `status` | string | Tidak | Default: `"submitted"`. Pilihan: `"draft"`, `"submitted"`, `"need_revision"` |

```json
{
  "assignment_id": "b8159043-98fe-4a94-b209-661ff97a514d",
  "content": "Berikut adalah link pengerjaan tugas dan penjelasan langkah eliminasi.",
  "file_path": "/uploads/submissions/jawaban_ahmad_fauzi.pdf",
  "status": "submitted"
}
```

#### 14.3.2 Ambil Daftar Submisi Siswa pada Suatu Tugas (Guru)
* **Endpoint**: `GET /api/lms/assignments/{assignment_id}/submissions`
* **Akses**: `require_staff`
* **Response `200 OK`**: Array of SubmissionResponse (termasuk nilai `grade` jika sudah dinilai).

#### 14.3.3 Beri Nilai & Masukan pada Submisi Siswa
* **Endpoint**: `POST /api/lms/submissions/{submission_id}/grade`
* **Akses**: `require_staff`
* **Deskripsi**: Menyimpan nilai guru dan mengubah status submisi menjadi `"graded"`. Jika sebelumnya sudah dinilai, maka nilai dan feedback akan diperbarui.

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `score` | decimal (float) | Ya | Nilai tugas (contoh: `92.50`) |
| `feedback` | string | Tidak | Umpan balik / catatan perbaikan dari guru |

```json
{
  "score": 92.50,
  "feedback": "Penjelasan di nomor 3 sangat sistematis dan tepat. Bagus!"
}
```

#### Response `200 OK`:
```json
{
  "id": "g1234567-89ab-cdef-0123-456789abcdef",
  "submission_id": "s9876543-210f-edcb-a987-6543210fedcb",
  "graded_by": "a782245e-896e-415c-b9c2-4471a9e75b27",
  "score": 92.50,
  "feedback": "Penjelasan di nomor 3 sangat sistematis dan tepat. Bagus!",
  "created_at": "2026-09-02T08:00:00Z",
  "updated_at": "2026-09-02T08:00:00Z"
}
```

---

### 14.4 Portofolio Siswa (Portfolios)

#### 14.4.1 Buat Karya Portofolio Siswa
* **Endpoint**: `POST /api/lms/portfolios/`
* **Akses**: Siswa (`require_all` + akun terikat profil `Student`)
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `title` | string | Ya | Judul karya portofolio |
| `description` | string | Ya | Deskripsi lengkap proyek / karya |
| `file_path` | string | Tidak | Gambar mockup / tangkapan layar berkas karya |
| `submission_id` | UUID | Tidak | Kaitkan dengan tugas yang pernah disubmit jika ada |
| `status` | string | Tidak | `"draft"` atau `"published"` (default: `"draft"`) |

```json
{
  "title": "Aplikasi Web E-Commerce Produk UMKM",
  "description": "Karya akhir semester menggunakan FastAPI dan React Tailwind.",
  "file_path": "/uploads/portfolios/preview_ecommerce.png",
  "status": "published"
}
```

#### 14.4.2 Ambil Daftar Portofolio Siswa
* **Endpoint**: `GET /api/lms/portfolios/student/{student_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Array of PortfolioResponse.

#### 14.4.3 Hapus Portofolio
* **Endpoint**: `DELETE /api/lms/portfolios/{portfolio_id}`
* **Akses**: `require_all`
* **Response `204 No Content`**

---

## 15. MODUL AKADEMIK & NILAI RAPOR (`/api/academics`)

### 15.1 Header Rapor Siswa (Report Cards)

#### 15.1.1 Buat Header Rapor Semester
* **Endpoint**: `POST /api/academics/report-cards/`
* **Akses**: `require_staff`
* **Status**: `201 Created`
* **Validasi**: Siswa hanya boleh memiliki 1 rapor per kombinasi `academic_year_id` dan `semester_id`.

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `student_id` | UUID | Ya | ID Siswa penerima rapor |
| `classroom_id` | UUID | Ya | ID Ruang Kelas |
| `academic_year_id` | UUID | Ya | ID Tahun Ajaran |
| `semester_id` | UUID | Ya | ID Semester |
| `homeroom_teacher_id`| UUID | Tidak | ID Wali Kelas (otomatis diambil dari akun login jika guru) |
| `sick_count` | integer | Tidak | Jumlah hari sakit (default: `0`) |
| `permitted_count` | integer | Tidak | Jumlah hari izin (default: `0`) |
| `unexcused_count` | integer | Tidak | Jumlah hari tanpa keterangan / alpa (default: `0`) |
| `homeroom_notes` | string | Tidak | Catatan evaluasi wali kelas |
| `status` | string | Tidak | `"draft"`, `"locked"`, atau `"published"` (default: `"draft"`) |

```json
{
  "student_id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
  "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
  "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d",
  "semester_id": "4b684da3-0bca-4bc4-9d54-8e1da4d5a371",
  "sick_count": 1,
  "permitted_count": 2,
  "unexcused_count": 0,
  "homeroom_notes": "Siswa sangat berprestasi, aktif dalam diskusi, dan memiliki kepemimpinan yang baik."
}
```

#### 15.1.2 Ambil Seluruh Rapor Milik Siswa
* **Endpoint**: `GET /api/academics/report-cards/student/{student_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Array of ReportCardResponse.

#### 15.1.3 Ambil Detail Rapor (Beserta Rincian Seluruh Nilai Mapel)
* **Endpoint**: `GET /api/academics/report-cards/{report_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Objek ReportCardResponse lengkap dengan array `items` (nilai seluruh mata pelajaran).

#### 15.1.4 Update Header Rapor
* **Endpoint**: `PUT /api/academics/report-cards/{report_id}`
* **Akses**: `require_staff`
* **Request Body**: `sick_count`, `permitted_count`, `unexcused_count`, `homeroom_notes`, `status`, `homeroom_teacher_id`.

#### 15.1.5 Terbitkan Rapor (Publish)
* **Endpoint**: `PUT /api/academics/report-cards/{report_id}/publish`
* **Akses**: `require_staff`
* **Deskripsi**: Mengubah status rapor menjadi `"published"` sehingga dapat dilihat oleh siswa dan orang tua.

#### 15.1.6 Hapus Rapor
* **Endpoint**: `DELETE /api/academics/report-cards/{report_id}`
* **Akses**: `require_admin`
* **Response `204 No Content`**

---

### 15.2 Rincian Nilai Mata Pelajaran Rapor (Report Card Items)

#### 15.2.1 Batch Simpan / Update Nilai Rapor
* **Endpoint**: `POST /api/academics/report-cards/{report_id}/items`
* **Akses**: `require_staff`
* **Deskripsi**: Menerima batch nilai mata pelajaran. Jika nilai untuk mata pelajaran tsb sudah ada di rapor, nilainya akan di-update (upsert).

#### Request Body (JSON):
```json
{
  "items": [
    {
      "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
      "teacher_id": "a782245e-896e-415c-b9c2-4471a9e75b27",
      "knowledge_score": 88.00,
      "skill_score": 90.00,
      "final_score": 89.00,
      "letter_grade": "A",
      "competency_description": "Sangat terampil dalam memecahkan soal aljabar dan matriks linier."
    },
    {
      "subject_id": "63df9d9a-8e34-4812-b95b-fa5f15fc4b90",
      "knowledge_score": 85.00,
      "skill_score": 85.00,
      "final_score": 85.00,
      "letter_grade": "A",
      "competency_description": "Memiliki pemahaman yang sangat baik dalam algoritma pemrograman."
    }
  ]
}
```

#### Response `200 OK`:
Array of ReportCardItemResponse yang berhasil disimpan.

---

## 16. MODUL PRESENSI & ABSENSI (`/api/attendance`)

### 16.1 Sesi Presensi (Attendance Sessions)

#### 16.1.1 Buka Sesi Presensi Baru
* **Endpoint**: `POST /api/attendance/sessions/`
* **Akses**: `require_staff`
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `classroom_id` | UUID | Ya | ID Ruang Kelas |
| `academic_year_id` | UUID | Ya | ID Tahun Ajaran |
| `semester_id` | UUID | Ya | ID Semester |
| `session_date` | date | Ya | Tanggal pertemuan (`YYYY-MM-DD`) |
| `subject_id` | UUID | Tidak | ID Mapel (kosongkan jika absensi harian kelas) |
| `teaching_schedule_id`| UUID | Tidak | ID Jadwal Pelajaran terkait |
| `start_time` | time | Tidak | Waktu mulai sesi (`HH:MM:SS`) |
| `end_time` | time | Tidak | Waktu selesai sesi (`HH:MM:SS`) |
| `topic` | string | Tidak | Materi / topik bahasan pertemuan |

```json
{
  "classroom_id": "cc3f08f0-5cb3-4d3f-9be7-c6def98d60d5",
  "subject_id": "97e68fa7-8898-4447-97fe-902c38ce7139",
  "academic_year_id": "885b60a7-74bc-4686-9adb-8cf51861bf9d",
  "semester_id": "4b684da3-0bca-4bc4-9d54-8e1da4d5a371",
  "session_date": "2026-09-02",
  "start_time": "07:30:00",
  "end_time": "09:00:00",
  "topic": "Pengenalan Vektor 2D dan Sistem Koordinat"
}
```

#### 16.1.2 Ambil Riwayat Sesi Presensi per Ruang Kelas
* **Endpoint**: `GET /api/attendance/sessions/classroom/{classroom_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Array of AttendanceSessionResponse (diurutkan berdasarkan tanggal terbaru).

#### 16.1.3 Ambil Detail Sesi Presensi (Beserta Seluruh Catatan Kehadiran Siswa)
* **Endpoint**: `GET /api/attendance/sessions/{session_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: Objek AttendanceSessionResponse beserta daftar entri pada array `records`.

#### 16.1.4 Hapus Sesi Presensi
* **Endpoint**: `DELETE /api/attendance/sessions/{session_id}`
* **Akses**: `require_staff`
* **Response `204 No Content`**

---

### 16.2 Catatan & Rekap Kehadiran Siswa

#### 16.2.1 Simpan Kehadiran Siswa (Batch Upsert)
* **Endpoint**: `POST /api/attendance/sessions/{session_id}/records`
* **Akses**: `require_staff`
* **Deskripsi**: Menyimpan status kehadiran banyak siswa sekaligus dalam satu kali panggil API. Jika siswa sudah memiliki catatan di sesi ini, statusnya otomatis diperbarui.

#### Request Body (JSON):
```json
{
  "records": [
    {
      "student_id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
      "status": "present",
      "remarks": "Hadir tepat waktu"
    },
    {
      "student_id": "78a911d2-11bb-49cc-a924-a1e8b15d6c99",
      "status": "sick",
      "remarks": "Surat dokter terlampir"
    },
    {
      "student_id": "89b022e3-22cc-40dd-ba35-b2e9c26e7daa",
      "status": "permit",
      "remarks": "Izin mengikuti lomba olimpiade sains"
    },
    {
      "student_id": "90c133f4-33dd-41ee-cb46-c3f0d37f8ebb",
      "status": "absent",
      "remarks": "Tanpa keterangan"
    }
  ]
}
```

*Status Kehadiran yang Diakui*:
* `"present"`: Hadir
* `"sick"`: Sakit
* `"permit"`: Izin
* `"absent"`: Alpa / Tanpa Keterangan

#### 16.2.2 Rekap Kehadiran Siswa (Summary & Persentase)
* **Endpoint**: `GET /api/attendance/summary/student/{student_id}`
* **Akses**: `require_all`
* **Deskripsi**: Menghitung total kehadiran, sakit, izin, alpa, serta persentase kehadiran kumulatif siswa.

#### Response `200 OK`:
```json
{
  "student_id": "698ce711-abd2-432c-a004-9d88f7b13ab2",
  "total_sessions": 40,
  "present_count": 38,
  "sick_count": 1,
  "permit_count": 1,
  "absent_count": 0,
  "attendance_rate_percentage": 95.0
}
```

---

## 17. MODUL PENGUMUMAN (`/api/announcements`)

### 17.1 Buat Pengumuman Baru
* **Endpoint**: `POST /api/announcements/`
* **Akses**: `require_staff`
* **Status**: `201 Created`

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `title` | string | Ya | Judul pengumuman (maks. 255 char) |
| `content` | string | Ya | Isi lengkap pengumuman (mendukung teks panjang/Markdown) |
| `priority` | string | Tidak | Tingkat urgensi: `"low"`, `"normal"`, `"high"`, `"urgent"` (default: `"normal"`) |
| `target_role` | string | Tidak | Target sasaran: `"all"`, `"teacher"`, `"student"`, `"parent"` (default: `"all"`) |
| `classroom_id` | UUID | Tidak | ID Kelas target (kosongkan jika pengumuman untuk seluruh sekolah) |
| `school_id` | UUID | Tidak | ID Sekolah (otomatis terisi dari sekolah pengguna login jika kosong) |

```json
{
  "title": "Jadwal Pelaksanaan Penilaian Akhir Semester (PAS) Ganjil",
  "content": "Diberitahukan kepada seluruh siswa bahwa PAS akan diselenggarakan pada tanggal 1-10 Desember 2026...",
  "priority": "high",
  "target_role": "all"
}
```

### 17.2 Ambil Daftar Pengumuman
* **Endpoint**: `GET /api/announcements/`
* **Akses**: `require_all`

#### Query Parameters:
| Parameter | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `classroom_id` | UUID | Tidak | Filter pengumuman untuk kelas tertentu (otomatis menyertakan pengumuman umum sekolah) |
| `target_role` | string | Tidak | Filter berdasarkan target peran (contoh: `"student"`, `"teacher"`) |

*Contoh Pemanggilan*: `GET /api/announcements/?target_role=student`
* **Response `200 OK`**: Array of AnnouncementResponse (diurutkan berdasarkan waktu pembuatan terbaru).

### 17.3 Ambil Detail Pengumuman
* **Endpoint**: `GET /api/announcements/{announcement_id}`
* **Akses**: `require_all`
* **Response `200 OK`**: AnnouncementResponse Object.

### 17.4 Update Pengumuman
* **Endpoint**: `PUT /api/announcements/{announcement_id}`
* **Akses**: `require_staff`
* **Request Body**: Semua field Announcement opsional.

### 17.5 Hapus Pengumuman
* **Endpoint**: `DELETE /api/announcements/{announcement_id}`
* **Akses**: `require_staff`
* **Response `204 No Content`**

---

## 18. MODUL UNGGAH MEDIA & BERKAS (`/api/uploads`)

File statis yang diunggah dapat diakses langsung melalui browser pada rute `/uploads/{folder}/{filename}` (contoh: `http://127.0.0.1:8000/uploads/avatars/xxxx.jpg`).

### 18.1 Upload Avatar / Foto Profil
* **Endpoint**: `POST /api/uploads/avatar`
* **Content-Type**: `multipart/form-data`
* **Akses**: `require_all` (Semua pengguna login)
* **Validasi**: Berkas harus berformat gambar (`image/jpeg`, `image/png`, `image/webp`).

#### Request Form Data:
* `file`: File gambar (Binary)

#### Response `200 OK`:
```json
{
  "id": "m1234567-89ab-cdef-0123-456789abcdef",
  "uploaded_by": "e6ce8ff7-be4b-47ef-9850-8bf848d58a7e",
  "original_name": "foto_profil_resmi.png",
  "stored_path": "/uploads/avatars/3fa85f64-5717-4562-b3fc-2c963f66afa6.png",
  "mime_type": "image/png",
  "file_size": 245820,
  "category": "avatar",
  "created_at": "2026-09-02T08:00:00Z"
}
```

### 18.2 Upload Dokumen / Modul / Tugas / Submisi
* **Endpoint**: `POST /api/uploads/document`
* **Content-Type**: `multipart/form-data`
* **Akses**: `require_all`

#### Request Parameters:
* `file` (Multipart Form Data): File berkas yang diunggah (PDF, DOCX, ZIP, gambar, dll).
* `category` (Form / Query parameter, opsional): Kategori folder penyimpanan.
  * `"material"` -> disimpan di folder `/uploads/materials/`
  * `"assignment"` -> disimpan di folder `/uploads/assignments/`
  * `"submission"` -> disimpan di folder `/uploads/submissions/`
  * `"document"` (default) -> disimpan di folder `/uploads/documents/`

#### Response `200 OK`:
```json
{
  "id": "m9876543-210f-edcb-a987-6543210fedcb",
  "uploaded_by": "e6ce8ff7-be4b-47ef-9850-8bf848d58a7e",
  "original_name": "modul_aljabar_bab1.pdf",
  "stored_path": "/uploads/materials/4cb91201-9988-4122-a012-334455667788.pdf",
  "mime_type": "application/pdf",
  "file_size": 1548290,
  "category": "material",
  "created_at": "2026-09-02T08:00:00Z"
}
```

---

## 19. MODUL DATABASE BACKUP & MAINTENANCE (`/api/backup`)
*Otorisasi: Seluruh endpoint di bawah ini dikunci khusus **`require_admin`**.*

### 19.1 Statistik Jumlah Record Tabel Database
* **Endpoint**: `GET /api/backup/stats`
* **Akses**: `require_admin`
* **Deskripsi**: Menghitung jumlah total tabel dan baris data pada setiap tabel di database secara real-time.

#### Response `200 OK`:
```json
{
  "total_tables": 24,
  "total_records": 4850,
  "generated_at": "2026-09-02T10:30:00.123456",
  "tables": [
    { "table_name": "academic_years", "row_count": 3 },
    { "table_name": "assignments", "row_count": 45 },
    { "table_name": "employees", "row_count": 84 },
    { "table_name": "students", "row_count": 1250 },
    { "table_name": "users", "row_count": 1340 }
  ]
}
```

### 19.2 Export Seluruh Database ke Format JSON
* **Endpoint**: `GET /api/backup/export-json`
* **Akses**: `require_admin`
* **Response**: File unduhan `backup_school_YYYYMMDD_HHMMSS.json` (`application/json` attachment).
* **Struktur Isi JSON**:
```json
{
  "timestamp": "2026-09-02T10:30:00.123456",
  "total_tables": 24,
  "tables": {
    "users": [ ... ],
    "students": [ ... ],
    "employees": [ ... ]
  }
}
```

### 19.3 Export Seluruh Database ke Format SQL Dump
* **Endpoint**: `GET /api/backup/export-sql`
* **Akses**: `require_admin`
* **Response**: File unduhan `backup_school_YYYYMMDD_HHMMSS.sql` (`application/sql` attachment) yang diawali dengan `BEGIN TRANSACTION;` dan diakhiri `COMMIT;`, siap di-restore ke PostgreSQL / SQLite.

---

## 20. MODUL PPDB (PENERIMAAN PESERTA DIDIK BARU) (`/api/ppdb`)

Modul PPDB dirancang menggunakan arsitektur **Staging Area** yang memisahkan seluruh data pendaftar baru dari data akademik utama sekolah.

### 20.1 Konsep Staging Area & Alur Bisnis
1. **Pemisahan Database**: Pendaftar ditampung di tabel khusus (`ppdb_accounts` dan `ppdb_registrations`) dan **tidak langsung** masuk ke tabel master SIAKAD (`students`, `users`, dll).
2. **Sistem Penguncian Pembayaran & Formulir**:
   * Calon siswa dapat mengisi formulir pendaftaran kapan saja dalam format JSON bersarang (*nested*).
   * Verifikasi pembayaran (`payment_status: 'paid'`) wajib dipenuhi sebelum admin dapat menerima pendaftar.
   * Setelah diterima (`registration_status: 'accepted'`), data formulir pendaftaran otomatis dikunci permanen (*locked*) dan tidak dapat diubah lagi oleh calon siswa.
3. **Migrasi Otomatis (Accept & Migrate)**:
   * Saat admin memanggil `POST /api/ppdb/accept/{id}`, sistem secara atomik mengekstrak seluruh data formulir dan mendistribusikannya ke tabel master `students`, `student_identities`, `student_addresses`, `student_contacts`, dan `parents` & `student_parent_relations`.
   * Akun login portal SIAKAD utama (`users`) otomatis dibuat dengan `role="student"` dan langsung mewarisi password yang didaftarkan calon siswa saat PPDB.

---

### 20.2 Registrasi Akun Calon Siswa
* **Endpoint**: `POST /api/ppdb/register-account`
* **Akses**: Publik
* **Status**: `201 Created`
* **Deskripsi**: Membuat akun di `ppdb_accounts` dan menginisialisasi entri di `ppdb_registrations` dengan status bayar `unpaid`.

#### Request Body (JSON):
| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `nik` | string | Ya | NIK 16 digit unik |
| `full_name` | string | Ya | Nama lengkap calon siswa |
| `email` | string | Ya | Email unik calon siswa |
| `password` | string | Ya | Password akun (min. 6 karakter) |

```json
{
  "nik": "3201012345670001",
  "full_name": "Ahmad Fauzi Rahman",
  "email": "ahmad.fauzi@gmail.com",
  "password": "PasswordPendaftar123!"
}
```

#### Response `201 Created`:
```json
{
  "id": "e45bef0f-5f00-4d7e-82cf-dfc0e924e2fe",
  "nik": "3201012345670001",
  "full_name": "Ahmad Fauzi Rahman",
  "email": "ahmad.fauzi@gmail.com",
  "is_active": true,
  "created_at": "2026-09-08T10:00:00Z",
  "updated_at": "2026-09-08T10:00:00Z"
}
```

---

### 20.3 Login Calon Siswa
* **Endpoint**: `POST /api/ppdb/login`
* **Akses**: Publik
* **Deskripsi**: Autentikasi akun pendaftar dan mengembalikan JWT Bearer Token khusus dengan claim `role: "ppdb_applicant"`.

#### Request Body (JSON):
```json
{
  "nik": "3201012345670001",
  "password": "PasswordPendaftar123!"
}
```
*(Catatan: Login juga dapat menggunakan field `email` sebagai alternatif NIK).*

#### Response `200 OK`:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "account_id": "e45bef0f-5f00-4d7e-82cf-dfc0e924e2fe",
  "nik": "3201012345670001",
  "full_name": "Ahmad Fauzi Rahman",
  "email": "ahmad.fauzi@gmail.com"
}
```

---

### 20.4 Status Pendaftaran Calon Siswa
* **Endpoint**: `GET /api/ppdb/my-registration`
* **Akses**: Calon Siswa Login (`Bearer <token_ppdb>`)
* **Response `200 OK`**:
```json
{
  "id": "7309fd3f-3b26-4b86-98fb-c75791abab8d",
  "account_id": "e45bef0f-5f00-4d7e-82cf-dfc0e924e2fe",
  "payment_status": "unpaid",
  "payment_amount": 0.0,
  "payment_proof_path": null,
  "payment_verified_at": null,
  "payment_verified_by": null,
  "registration_status": "pending",
  "form_data": null,
  "student_id": null,
  "created_at": "2026-09-08T10:00:00Z",
  "updated_at": "2026-09-08T10:00:00Z"
}
```

---

### 20.5 Unggah Bukti Pembayaran
* **Endpoint**: `POST /api/ppdb/upload-payment`
* **Content-Type**: `multipart/form-data`
* **Akses**: Calon Siswa Login (`Bearer <token_ppdb>`)
* **Deskripsi**: Mengunggah berkas transfer bank (JPG/PNG/WebP/PDF). Berkas disimpan di `/uploads/ppdb_payments/` dan `payment_status` otomatis berubah menjadi `"pending_verification"`.

#### Request Form Data:
* `file`: Berkas foto/PDF bukti bayar (Binary)

#### Response `200 OK`:
```json
{
  "id": "7309fd3f-3b26-4b86-98fb-c75791abab8d",
  "account_id": "e45bef0f-5f00-4d7e-82cf-dfc0e924e2fe",
  "payment_status": "pending_verification",
  "payment_amount": 0.0,
  "payment_proof_path": "/uploads/ppdb_payments/d8a1c234-5678-4abc-9def-0123456789ab.jpg",
  "registration_status": "pending",
  "created_at": "2026-09-08T10:00:00Z",
  "updated_at": "2026-09-08T10:05:00Z"
}
```

---

### 20.6 Pengisian Formulir Pendaftaran Bersarang
* **Endpoint**: `PUT /api/ppdb/registration-form`
* **Akses**: Calon Siswa Login (`Bearer <token_ppdb>`)
* **Format Body**: JSON bersarang (*nested*) yang strukturnya **identik 100%** dengan respons `GET /api/students/{id}` pada modul SIAKAD master.

#### Request Body (JSON):
```json
{
  "nik": "3201012345670001",
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
```

#### Response `200 OK`:
Data registrasi diperbarui dengan `form_data` berisi payload bersarang di atas.

#### Error Response:
* `400 Bad Request`: `"Formulir telah dikunci karena Anda telah resmi diterima sebagai siswa"` jika status seleksi sudah `accepted`.

---

### 20.7 Monitoring Seluruh Pendaftar PPDB (Admin)
* **Endpoint**: `GET /api/ppdb/registrations`
* **Akses**: `require_admin`

#### Query Parameters:
| Parameter | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `payment_status` | string | Tidak | Filter: `unpaid`, `pending_verification`, `paid`, `rejected` |
| `registration_status` | string | Tidak | Filter: `pending`, `accepted`, `rejected` |
| `search` | string | Tidak | Pencarian nama pendaftar atau NIK |

*Contoh Pemanggilan*: `GET /api/ppdb/registrations?payment_status=pending_verification`
* **Response `200 OK`**: Array of PPDBRegistrationResponse.

---

### 20.8 Detail Pendaftar PPDB (Admin)
* **Endpoint**: `GET /api/ppdb/registrations/{id}`
* **Akses**: `require_admin`
* **Response `200 OK`**: PPDBRegistrationResponse lengkap dengan `form_data` dan akun pendaftar.

---

### 20.9 Verifikasi Pembayaran (Admin)
* **Endpoint**: `PUT /api/ppdb/verify-payment/{id}`
* **Akses**: `require_admin`
* **Deskripsi**: Admin memvalidasi bukti transfer pendaftar dan mengubah status menjadi `paid` atau `rejected`.

#### Request Body (JSON):
```json
{
  "payment_status": "paid",
  "payment_amount": 250000.00
}
```

#### Response `200 OK`:
```json
{
  "id": "7309fd3f-3b26-4b86-98fb-c75791abab8d",
  "payment_status": "paid",
  "payment_amount": 250000.00,
  "payment_verified_at": "2026-09-08T10:15:00Z",
  "payment_verified_by": "e6ce8ff7-be4b-47ef-9850-8bf848d58a7e",
  "registration_status": "pending"
}
```

---

### 20.10 Penerimaan Siswa & Migrasi Otomatis ke Master SIAKAD (Admin)
* **Endpoint**: `POST /api/ppdb/accept/{id}`
* **Akses**: `require_admin`
* **Deskripsi**: **Mesin Migrasi Data Atomik**. Sistem memindahkan data dari staging area `ppdb_registrations` langsung ke tabel-tabel master akademik SIAKAD:
  1. Membuat akun `users` dengan `role: "student"` dan password yang sama dengan akun pendaftaran PPDB.
  2. Membuat entri di tabel `students`.
  3. Membuat entri identitas tambahan di `student_identities`.
  4. Membuat entri alamat di `student_addresses`.
  5. Membuat entri kontak di `student_contacts`.
  6. Membuat/menautkan data orang tua di `parents` dan pivot relasi di `student_parent_relations`.
  7. Mengubah `registration_status` menjadi `"accepted"` dan menautkan `student_id`.

#### Syarat Validasi:
* Pendaftar harus berstatus pembayaran `"paid"`.
* Formulir pendaftaran `form_data` tidak boleh kosong.
* Pendaftar belum pernah diterima sebelumnya.

#### Response `200 OK`:
```json
{
  "message": "Calon siswa berhasil diterima dan seluruh data berhasil dimigrasikan ke database master SIAKAD!",
  "registration_id": "7309fd3f-3b26-4b86-98fb-c75791abab8d",
  "student_id": "9b638b0e-425a-4a87-abf3-f98cea4bedde",
  "user_id": "948a6175-1c51-49e3-9baa-f895488a2887",
  "username": "0051234567",
  "full_name": "Ahmad Fauzi Rahman",
  "role": "student",
  "migrated_at": "2026-09-08T10:20:00Z"
}
```

---

## 21. STANDAR FORMAT ERROR RESPONSE & HTTP STATUS CODE

### 21.1 Format Standar Error Aplikasi (FastAPI HTTPException)
Format error response standar:
```json
{
  "detail": "Pesan deskripsi kesalahan yang spesifik dan jelas"
}
```

### 20.2 Format Validasi Schema Gagal (`422 Unprocessable Entity`)
Jika payload request body tidak sesuai tipe data Pydantic:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "nik"],
      "msg": "String should have at least 16 characters",
      "input": "12345"
    }
  ]
}
```

### 20.3 Rangkuman HTTP Status Code:
| Status Code | Arti | Skenario Terjadinya |
|---|---|---|
| `200 OK` | Sukses | Request GET / PUT / POST berhasil mengembalikan data |
| `201 Created` | Berhasil Dibuat | Entitas baru berhasil dibuat (POST) |
| `204 No Content`| Tanpa Konten | Entitas berhasil dihapus (DELETE) |
| `400 Bad Request`| Permintaan Tidak Sah | Validasi bisnis gagal (misal: NIK/NISN kembar, email sudah terpakai, password lama salah) |
| `401 Unauthorized`| Belum Terautentikasi | Token JWT tidak disertakan, kedaluwarsa, atau kredensial login salah |
| `403 Forbidden` | Akses Ditolak | Pengguna login tetapi role tidak memiliki hak akses ke endpoint terkait |
| `404 Not Found` | Data Tidak Ditemukan | ID entitas yang dicari tidak ditemukan di database |
| `422 Unprocessable Entity`| Tipe Data Salah | Format payload JSON tidak lolos validasi schema Pydantic |
| `500 Internal Server Error`| Kesalahan Server | Terjadi exception internal atau kegagalan koneksi database |

---

*Dokumentasi ini sinkron dengan arsitektur backend SIAKAD & LMS versi 2.0.0 (FastAPI + SQLAlchemy + PostgreSQL).*
