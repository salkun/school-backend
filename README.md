# 🏫 EduSphere SIAKAD & LMS API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B%20%7C%2015%2B%20%7C%2016%2B-336791.svg?style=flat&logo=PostgreSQL&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?style=flat&logo=SQLAlchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=flat&logo=Pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Deployment](https://img.shields.io/badge/Deployment-cPanel%20%7C%20Docker%20%7C%20Uvicorn-blue.svg?style=flat)](#-panduan-deployment)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

Backend REST API untuk **Sistem Informasi Akademik (SIAKAD)** dan **Learning Management System (LMS)** sekolah modern yang tangguh, modular, dan terukur. Dibangun menggunakan **FastAPI** dan **PostgreSQL**, sistem ini mencakup pengelolaan master data sekolah standar nasional (Dapodik), manajemen siswa dan PTK, jadwal pelajaran, e-learning, penilaian rapor kurikulum, presensi, pengumuman, modul backup data, serta sistem **PPDB Online (Penerimaan Peserta Didik Baru)** terintegrasi dengan migrasi data otomatis.

---

## 📑 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Modul & Fitur Utama](#-modul--fitur-utama)
- [Tech Stack & Library](#-tech-stack--library)
- [Struktur Direktori](#-struktur-direktori)
- [Persyaratan Sistem](#-persyaratan-sistem)
- [Instalasi & Menjalankan di Lokal](#-instalasi--menjalankan-di-lokal)
- [Konfigurasi Environment Variables](#-konfigurasi-environment-variables)
- [Panduan Deployment](#-panduan-deployment)
  - [1. Phusion Passenger (cPanel / CloudLinux)](#1-phusion-passenger-cpanel--cloudlinux)
  - [2. Docker / Server Linux & GitHub Actions](#2-docker--server-linux--github-actions)
- [Dokumentasi API & Testing](#-dokumentasi-api--testing)
- [Pengujian Otomatis (Testing)](#-pengujian-otomatis-testing)
- [Referensi Dokumen Terkait](#-referensi-dokumen-terkait)

---

## 💡 Tentang Proyek

EduSphere Backend API dirancang untuk memenuhi kebutuhan tata kelola operasional sekolah modern dalam satu platform terpadu:
1. **Multi-Role & Multi-Tenant Ready**: Mendukung isolasi data sekolah dengan pembagian hak akses terperinci (*Role-Based Access Control*).
2. **Standar Data Dapodik**: Struktur entitas siswa, orang tua, dan PTK dirancang selaras dengan format data pokok pendidikan nasional.
3. **Terintegrasi Penuh (End-to-End)**: Dari pendaftaran calon siswa baru (PPDB), pembayaran, verifikasi, hingga konversi otomatis menjadi siswa aktif dan pengguna aplikasi SIAKAD.
4. **Performa Tinggi**: Arsitektur asinkron FastAPI dengan validasi data ketat berbasis Pydantic V2 dan query efisien via SQLAlchemy 2.0.

---

## 🚀 Modul & Fitur Utama

### 1. 🔐 Autentikasi & Hak Akses (RBAC) (`/api/auth`, `/api/users`)
- Autentikasi berbasis **JWT Bearer Token** (`access_token`, `token_type: Bearer`).
- Enkripsi password aman menggunakan **bcrypt** dan salt otomatis.
- Skema peran berjenjang:
  - `admin`: Hak akses penuh ke seluruh modul sistem dan konfigurasi.
  - `staff` / `employee`: Akses modul operasional, data master, dan presensi.
  - `teacher`: Mengelola jadwal mengajar, materi LMS, tugas, nilai rapor, dan absensi kelas.
  - `student`: Mengakses jadwal pelajaran, materi belajar, pengumpulan tugas, portofolio, dan nilai rapor.
  - `ppdb_applicant`: Akses portal calon siswa baru untuk melengkapi formulir dan pembayaran.

### 2. 👤 Profil Pengguna & Dashboard (`/api/profile`, `/api/dashboard`)
- Pengambilan dan pembaharuan profil pengguna yang sedang login.
- Fitur ganti password mandiri pengguna.
- Unggah foto profil / avatar pengguna.
- Ringkasan metrik statistik dinamis untuk admin, guru, dan staf (total siswa, guru, rombel, dan aktivitas terkini).

### 3. 🏢 Profil Sekolah & Master Data (`/api/schools`, `/api/master`)
- **Profil Sekolah**: NPSN, Nama Lembaga, Jenjang, Akreditasi, Alamat, Logo, dan Kontak.
- **Tahun Ajaran & Semester**: Status aktif/nonaktif periode akademik berjalan.
- **Sarana & Prasarana**: Manajemen Gedung (*Buildings*) dan Ruang Kelas (*Classrooms*) beserta kapasitas fisik.
- **Mata Pelajaran & Kurikulum**: Daftar mapel, kode, kelompok kurikulum, dan alokasi beban jam mengajar.

### 4. 👨‍🏫 Manajemen Pendidik & Tenaga Kependidikan (PTK) (`/api/employees`)
- Master data PTK lengkap selaras Dapodik:
  - `Identitas Tambahan`: NIK, NUPTK, NPWP, BPJS Kesehatan/Ketenagakerjaan, No. Rekening Bank.
  - `Kontak Darurat`: Kontak keluarga/kerabat darurat pegawai.
  - `Keluarga & Anak`: Riwayat anak kandung/tanggungan pegawai.
  - `Pemetaan Mapel`: Pengampu mata pelajaran oleh masing-masing guru.
- **Jabatan Struktural (`/api/positions`)**: Definisi jabatan (Kepala Sekolah, Waka Kurikulum, dll.) dan riwayat SK penugasan pegawai.

### 5. 👨‍🎓 Manajemen Siswa Terpadu (`/api/students`)
- Master data siswa lengkap:
  - `Identitas Pokok & Tambahan`: NISN, NIS, NIK, No. Akta, Program KIP/PIP/KPS.
  - `Alamat Domisili`: Wilayah administratif lengkap (RT/RW, Dusun, Kelurahan, Kecamatan, Kode Pos).
  - `Kontak Pribadi`: Nomor ponsel, telepon rumah, dan email siswa.
  - `Data Orang Tua & Wali`: Rincian data Ayah, Ibu, dan Wali (NIK, Pekerjaan, Pendidikan, Penghasilan Bulanan).
  - `Enrollment & Rombel`: Riwayat penempatan kelas siswa per tahun ajaran dan semester.

### 6. 📅 Penjadwalan & Wali Kelas (`/api/schedules`)
- Pengaturan jadwal pelajaran mingguan per hari, jam ke, ruang kelas, rombel, mapel, dan guru pengampu.
- Deteksi konflik jadwal mengajar guru dan ruang kelas.
- Penugasan resmi wali kelas untuk setiap rombongan belajar (*homeroom assignment*).

### 7. 💻 Learning Management System (LMS) (`/api/lms`)
- **Materi Belajar**: Unggah modul ajar, silabus dokumen (PDF/DOCX), materi teks, tautan video YouTube/eksternal.
- **Tugas Siswa (Assignments)**: Penugasan terstruktur dengan instruksi lengkap, tenggat waktu (*deadline*), dan bobot nilai.
- **Pengumpulan Tugas (Submissions)**: Siswa mengunggah berkas jawaban tugas, catatan, dan riwayat revisi berkas.
- **Penilaian & Feedback (Grades)**: Guru memberi skor nilai numerik, catatan masukan guru, dan tanggal penilaian.
- **Portofolio Siswa**: Wadah dokumentasi karya dan prestasi siswa berdasarkan kategori (Akademik, Seni, Teknologi, Literasi).

### 8. 📊 Akademik & Nilai Rapor (`/api/academics`)
- Pengelolaan Buku Rapor Semester Siswa (*Report Cards*).
- Komponen penilaian komprehensif:
  - Nilai formatif harian, tugas, PTS (Penilaian Tengah Semester), PAS (Penilaian Akhir Semester).
  - Nilai akhir terhitung, predikat huruf (A/B/C/D), dan deskripsi capaian kompetensi pembelajaran.
  - Catatan evaluasi perkembangan dan rekomendasi wali kelas.

### 9. 📝 Presensi & Absensi Terpadu (`/api/attendance`)
- Pembuatan sesi presensi per tanggal, rombel, mata pelajaran, dan guru.
- Pencatatan status kehadiran tiap siswa: `Hadir (H)`, `Sakit (S)`, `Izin (I)`, `Alpa (A)` disertai catatan/surat keterangan.
- Rekapitulasi kehadiran berkala untuk laporan evaluasi kesiswaan.

### 10. 📢 Pengumuman & Broadcast Sekolah (`/api/announcements`)
- Publikasi pengumuman sekolah dengan target audiens fleksibel: Semua Pengguna, Khusus Guru, Khusus Siswa, atau Khusus Orang Tua.
- Fitur *Pin Announcement* untuk menyematkan pengumuman prioritas di bagian atas.
- Pengaturan status publikasi (*draft* atau *published*).

### 11. 🎓 PPDB Online (Penerimaan Peserta Didik Baru) (`/api/ppdb`)
- **Staging Area Terisolasi**: Calon siswa baru disimpan di tabel staging terpisah, menjaga integritas database master SIAKAD.
- **Pendaftaran & Login Mandiri**: Akun calon siswa dibuat menggunakan NIK dan Email yang tervalidasi unik.
- **Unggah Bukti Pembayaran**: Calon siswa mengunggah bukti transfer biaya pendaftaran untuk diverifikasi admin/panitia.
- **Formulir Pendaftaran Bersarang**: Pengisian bertahap data calon siswa, orang tua/wali, kontak, asal sekolah, dan dokumen persyaratan.
- **Panel Monitoring & Verifikasi Admin**: Filter pendaftar berdasarkan status pendaftaran, jalur masuk, dan status verifikasi bayar.
- **Penerimaan & Migrasi Otomatis**: Sekali klik *Accept*, sistem secara otomatis:
  1. Mentransfer seluruh data formulir PPDB ke entitas master `Student`, `StudentAddress`, `StudentParent`, dan `StudentContact`.
  2. Membuatkan akun pengguna `User` resmi SIAKAD dengan peran `student` dan kredensial akses default siap pakai.

### 12. 📁 Manajemen Media & Unggah Berkas (`/api/uploads`)
- Endpoint khusus unggah berkas dengan validasi ekstensi dan tipe file.
- Penataan folder penyimpanan otomatis di direktori static `/uploads/`.
- Berkas dapat diakses langsung secara publik/aman melalui URL statis.

### 13. 💾 Pemeliharaan & Backup Database (`/api/backup`)
- Fasilitas pencadangan snapshot basis data PostgreSQL.
- Riwayat eksekusi backup dan log status untuk keperluan *disaster recovery*.

---

## 🛠 Tech Stack & Library

| Kategori | Teknologi | Deskripsi |
| :--- | :--- | :--- |
| **Bahasa Pemrograman** | Python 3.9 - 3.11+ | Lingkungan eksekusi utama |
| **Web Framework** | FastAPI (v0.111+) | Framework REST API modern, berbasis ASGI, bertipe data tinggi |
| **Server Engine** | Uvicorn [standard] | ASGI web server dengan performa tinggi |
| **Database** | PostgreSQL | Sistem basis data relasional utama |
| **ORM** | SQLAlchemy 2.0+ | Object Relational Mapping berbasis tipe modern |
| **Validasi Data** | Pydantic V2 & Settings | Validasi skema request/response dan manajemen `.env` |
| **Database Driver** | psycopg2-binary | Driver PostgreSQL untuk koneksi Python yang stabil |
| **Autentikasi & Kriptografi** | PyJWT, Passlib, Bcrypt | Manajemen JWT Token dan enkripsi hash password |
| **WSGI Bridge** | a2wsgi | Adapter ASGI-ke-WSGI untuk deployment Phusion Passenger cPanel |
| **Migrasi Database** | Alembic | Manajemen versi dan migrasi skema tabel |
| **Dokumentasi Otomatis** | Swagger UI & ReDoc | OpenAPI interactive documentation bawaan FastAPI |

---

## 📂 Struktur Direktori

```text
school-backend/
├── app/
│   ├── config.py                 # Konfigurasi aplikasi & parsing .env via Pydantic Settings
│   ├── database.py               # Engine SQLAlchemy, SessionLocal, dan Base metadata
│   ├── dependencies.py           # Dependency injection (Auth checker, RBAC role guard, DB session)
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py           # Fungsi hash bcrypt, verify password, dan create JWT token
│   ├── models/                   # Definisi model tabel ORM SQLAlchemy
│   │   ├── academic_report.py    # Model Rapor & Nilai Mata Pelajaran
│   │   ├── attendance.py         # Model Sesi & Catatan Presensi
│   │   ├── communication.py      # Model Pengumuman & Media Unggahan
│   │   ├── employee.py           # Model Master PTK, Identitas, Anak, Kontak, Pengampu
│   │   ├── lms.py                # Model Materi, Tugas, Submission, Nilai, Portofolio
│   │   ├── master.py             # Model Tahun Ajaran, Semester, Gedung, Ruang, Mapel, Rombel
│   │   ├── parent.py             # Model Orang Tua / Wali Siswa
│   │   ├── ppdb.py               # Model Calon Siswa, Formulir Pendaftaran, Pembayaran PPDB
│   │   ├── school.py             # Model Profil Sekolah Multi-Tenant
│   │   ├── student.py            # Model Siswa, Alamat, Kontak, Identitas, Enrollment
│   │   └── user.py               # Model Akun Pengguna & Enum Peran (UserRole)
│   ├── schemas/                  # Pydantic Schemas (Validasi input payload & serialisasi output)
│   │   ├── academic.py
│   │   ├── announcement.py
│   │   ├── attendance.py
│   │   ├── auth.py
│   │   ├── common.py
│   │   ├── employee.py
│   │   ├── lms.py
│   │   ├── master.py
│   │   ├── ppdb.py
│   │   ├── school.py
│   │   ├── student.py
│   │   └── user.py
│   └── routers/                  # Controller / API Endpoint per modul
│       ├── academics.py          # /api/academics/*
│       ├── addresses.py          # /api/addresses/*
│       ├── announcements.py      # /api/announcements/*
│       ├── attendance.py         # /api/attendance/*
│       ├── auth.py               # /api/auth/*
│       ├── backup.py             # /api/backup/*
│       ├── contacts.py           # /api/contacts/*
│       ├── dashboard.py          # /api/dashboard/*
│       ├── employee_children.py  # /api/employee-children/*
│       ├── employee_contacts.py  # /api/employee-contacts/*
│       ├── employee_identities.py# /api/employee-identities/*
│       ├── employee_subjects.py  # /api/employees/{id}/subjects/*
│       ├── employees.py          # /api/employees/*
│       ├── enrollments.py        # /api/enrollments/*
│       ├── identities.py         # /api/identities/*
│       ├── lms.py                # /api/lms/*
│       ├── master.py             # /api/master/*
│       ├── parents.py            # /api/parents/*
│       ├── positions.py          # /api/positions/*
│       ├── ppdb.py               # /api/ppdb/*
│       ├── profile.py            # /api/profile/*
│       ├── schedules.py          # /api/schedules/*
│       ├── schools.py            # /api/schools/*
│       ├── students.py           # /api/students/*
│       ├── uploads.py            # /api/uploads/*
│       └── users.py              # /api/users/*
├── uploads/                      # Direktori statis penyimpanan berkas media unggahan
├── .github/
│   └── workflows/
│       └── deploy.yaml           # Pipeline CI/CD GitHub Actions via Remote SSH
├── main.py                       # Inisialisasi FastAPI, CORS, mount uploads, dan registrasi router
├── passenger_wsgi.py             # Entrypoint Phusion Passenger WSGI (cPanel deployment)
├── test_ppdb_flow.py             # Script pengujian otomatis alur PPDB end-to-end
├── requirements.txt              # Daftar dependensi paket Python
├── API_DOCUMENTATION.md          # Dokumentasi teknis terperinci 2000+ baris seluruh endpoint
├── DATABASE_SCHEMA_ADDITIONS.md  # Spesifikasi skema database tambahan & ERD Mermaid
└── README.md                     # Panduan komprehensif proyek (Dokumen ini)
```

---

## 💻 Persyaratan Sistem

Sebelum memulai instalasi, pastikan sistem Anda memenuhi persyaratan berikut:
- **Python**: Versi `3.9` atau yang lebih baru (disarankan `Python 3.10` atau `3.11`).
- **PostgreSQL**: Versi `13` atau yang lebih baru (dapat menggunakan PostgreSQL lokal, Docker, Laragon PostgreSQL, atau Cloud Database seperti Supabase/Neon).
- **Git**: Untuk proses cloning dan manajemen versi kode.

---

## ⚙️ Instalasi & Menjalankan di Lokal

### 1. Clone Repositori
```bash
git clone https://github.com/salkun/school-backend.git
cd school-backend
```

### 2. Buat dan Aktifkan Virtual Environment
- **Windows (PowerShell / Command Prompt)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependensi
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Konfigurasi Environment File (`.env`)
Salin atau buat file baru bernama `.env` di folder *root* proyek dan sesuaikan kredensial database Anda:
```env
DATABASE_URL=postgresql://postgres:password_db_anda@localhost:5432/siakad
SECRET_KEY=kunci_rahasia_jwt_yang_sangat_aman_dan_panjang_minimal_32_karakter
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> [!NOTE]
> Pastikan basis data bernama `siakad` sudah dibuat terlebih dahulu di PostgreSQL Anda sebelum menjalankan server.

### 5. Jalankan Server Development
Jalankan aplikasi menggunakan server Uvicorn dengan mode *auto-reload*:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Saat aplikasi dijalankan untuk pertama kali, baris `Base.metadata.create_all(bind=engine)` di `main.py` akan secara otomatis menyinkronkan dan membuat semua tabel model ke dalam PostgreSQL.

Aplikasi siap diakses di:
- **Root Endpoint**: `http://127.0.0.1:8000/`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 🔑 Konfigurasi Environment Variables

Aplikasi membaca konfigurasi dari berkas `.env` menggunakan Pydantic Settings ([app/config.py](file:///c:/laragon/www/school-backend/app/config.py)):

| Variabel | Tipe Data | Default | Deskripsi |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `string` | *(Wajib diisi)* | URI koneksi basis data PostgreSQL standar, contoh: `postgresql://user:pass@host:5432/dbname` |
| `SECRET_KEY` | `string` | *(Wajib diisi)* | Kunci rahasia untuk menandatangani signature JSON Web Token (JWT) |
| `ALGORITHM` | `string` | `HS256` | Algoritma enkripsi kriptografi untuk JWT (default: HMAC-SHA256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| `integer` | `60` | Masa berlaku akses token JWT dalam satuan menit |

---

## 🌐 Panduan Deployment

### 1. Phusion Passenger (cPanel / CloudLinux)
Aplikasi ini sudah dilengkapi berkas adapter [passenger_wsgi.py](file:///c:/laragon/www/school-backend/passenger_wsgi.py) berbasis library `a2wsgi` untuk menjalankan aplikasi ASGI FastAPI di atas web server WSGI cPanel (*Setup Python App*):

1. Masuk ke cPanel menu **Setup Python App**.
2. Buat aplikasi baru:
   - **Python Version**: Pilih `3.9`, `3.10`, atau `3.11`.
   - **Application Root**: Arahkan ke folder proyek di server (misal: `school-backend`).
   - **Application URL**: Subdomain atau domain utama API Anda.
   - **Application Startup File**: Isi `passenger_wsgi.py`.
   - **Application Entry Point**: Isi `application`.
3. Buka terminal cPanel atau SSH, aktifkan virtualenv yang dibentuk cPanel, lalu pasang dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Buat file `.env` di folder root aplikasi dengan konfigurasi database server produksi.
5. Klik tombol **Restart** pada antarmuka *Setup Python App* cPanel.

### 2. Docker / Server Linux & GitHub Actions
Aplikasi menyertakan pipeline deployment otomatis pada [.github/workflows/deploy.yaml](file:///c:/laragon/www/school-backend/.github/workflows/deploy.yaml):
- Setiap perubahan yang di-*push* ke cabang `main` akan memicu eksekusi SSH Action ke server target.
- Server secara otomatis menarik kode terbaru (`git pull origin main`) dan mengeksekusi containerisasi via Docker Compose:
  ```bash
  docker-compose up -d --build
  ```

---

## 📖 Dokumentasi API & Testing

Sistem menyediakan dua antarmuka dokumentasi API interaktif yang otomatis dibuat oleh FastAPI:
- **Swagger UI** (`/docs`): Uji langsung setiap endpoint REST API (GET, POST, PUT, DELETE), kirim parameter, dan periksa respons payload secara interaktif.
- **ReDoc** (`/redoc`): Tampilan dokumentasi OpenAPI yang bersih, elegan, dan terstruktur untuk pengembang frontend & mobile.

### Format Standar Respons & Autentikasi:
- **Header Autentikasi**:
  ```http
  Authorization: Bearer <access_token_anda>
  ```
- **Struktur Standar HTTP Status**:
  - `200 OK` / `201 Created`: Permintaan berhasil diproses.
  - `400 Bad Request`: Validasi data gagal atau pelanggaran aturan logika bisnis.
  - `401 Unauthorized`: Token tidak disertakan, format tidak valid, atau telah kedaluwarsa.
  - `403 Forbidden`: Hak akses peran pengguna tidak mencukupi untuk endpoint terkait.
  - `404 Not Found`: Data entitas (ID/UUID) yang dicari tidak ditemukan.
  - `500 Internal Server Error`: Kesalahan server internal.

---

## 🧪 Pengujian Otomatis (Testing)

Tersedia skrip pengujian integrasi otomatis untuk memverifikasi alur bisnis pendaftaran calon siswa hingga migrasi ke master SIAKAD:

```bash
# Pastikan server database aktif dan .env sudah terkonfigurasi
python test_ppdb_flow.py
```

Skrip ini akan memvalidasi skenario secara end-to-end:
1. Pendaftaran calon siswa (`/api/ppdb/register-account`).
2. Login akun calon siswa (`/api/ppdb/login`).
3. Pengunggahan berkas bukti pembayaran formulir (`/api/ppdb/upload-payment`).
4. Pengisian formulir pendaftaran bertingkat (`/api/ppdb/registration-form`).
5. Verifikasi pembayaran oleh admin (`/api/ppdb/verify-payment/{id}`).
6. Persetujuan & migrasi otomatis calon siswa ke tabel master siswa dan tabel user (`/api/ppdb/accept/{id}`).

---

## 📚 Referensi Dokumen Terkait

Untuk informasi lebih mendalam mengenai integrasi teknis dan basis data, silakan pelajari dokumen resmi pendukung berikut:
- **[API_DOCUMENTATION.md](file:///c:/laragon/www/school-backend/API_DOCUMENTATION.md)**: Spesifikasi lengkap 2000+ baris mencakup skema payload, request body, query parameter, dan contoh respons JSON untuk 20 modul endpoint.
- **[DATABASE_SCHEMA_ADDITIONS.md](file:///c:/laragon/www/school-backend/DATABASE_SCHEMA_ADDITIONS.md)**: Diagram relasi entitas lengkap (ERD Mermaid), detail tipe data kolom, constraint relasional, dan skema tabel tambahan (LMS, Rapor, Presensi, Pengumuman).

---

## 📄 Lisensi

Proyek ini dirilis di bawah lisensi **MIT License**. Anda bebas menggunakan, memodifikasi, dan mengembangkan perangkat lunak ini untuk keperluan institusi pendidikan maupun komersial.
