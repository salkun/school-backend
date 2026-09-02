# SIAKAD API (School Management System)

A robust and scalable Backend API for a School Management System (Sistem Informasi Akademik) built with **FastAPI** and **PostgreSQL**. This API serves as the core master data management system, handling everything from user authentication to complex employee and student relational data.

---

## Key Features

### 1. Authentication & User Management
* Role-based access control (Admin, Staff, Teacher, Student).
* Secure password hashing using `bcrypt`.
* User-to-School relational binding (Multi-tenant ready).

### 2. Master Data Management
* **Academic Year & Semester:** Manage active school years and terms.
* **Facilities:** Manage Buildings and Classrooms with physical dimensions.
* **Curriculum:** Manage Subjects (Mata Pelajaran) and lesson hours.

### 3. Employee (PTK) Management
* Comprehensive master data for Teachers and Staff aligned with national standards (Dapodik).
* **Sub-modules (One-to-One / One-to-Many):**
  * `Employee Identities` (KTP, Address, Tax, Bank details).
  * `Employee Contacts` (Emergency contacts).
  * `Employee Children` (Family and dependents data).
  * `Employee Educations` (Academic history & degrees).

### 4. Student Management
* Complete master data for Students.
* **Sub-modules:**
  * `Student Identities` and `Addresses`.
  * `Student Parents` (Father, Mother, Guardian).
  * `Student Contacts`.

---

## Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.9+)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0
* **Data Validation:** Pydantic V2
* **Server:** Uvicorn

---

## 📂 Project Structure

```text
├── app/
│   ├── core/              # Security and config (JWT, Hashing, Settings)
│   ├── models/            # SQLAlchemy Models (Database Tables)
│   │   ├── employee.py
│   │   ├── master.py
│   │   ├── school.py
│   │   ├── student.py
│   │   └── user.py
│   ├── schemas/           # Pydantic Schemas (Input/Output Validation)
│   ├── routers/           # API Endpoints (Controllers)
│   ├── database.py        # Database connection & session maker
│   └── dependencies.py    # FastAPI Dependencies (e.g., Auth Checkers)
├── main.py                # FastAPI application instance & router registration
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (DB URL, Secret Keys)
```

## Installation & Setup
### 1. Prerequisites
* Python 3.9 or higher
* PostgreSQL server running locally (e.g., via Laragon or pgAdmin)

### 2.Clone the Repository
    git clone https://github.com/salkun/school-backend.git
    cd siakad-api

### 3. Setup Virtual Environment
    python -m venv venv
      # On Windows:
    venv\Scripts\activate
      # On macOS/Linux:
    source venv/bin/activate

### 4. Install Dependencies
    pip install -r requirements.txt

### 5. Configure Environment Variables
* Create a `.env` file in the root directory and configure your PostgreSQL database connection:
    ```
    DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/SIAKAD"
    SECRET_KEY="your_super_secret_key"
    ```
### 6. Run the Server
* The database tables will be automatically generated upon starting the application.
    `uvicorn main:app --reload`

# API Documentation
* Once the server is running, FastAPI automatically generates interactive API documentation. You can access it via your web browser:
* - Swagger UI (Recommended): http://127.0.0.1:8000/docs
* - ReDoc: http://127.0.0.1:8000/redoc
You can use the Swagger UI to test all `GET`, `POST`, `PUT`, and `DELETE` requests directly from your browser.

