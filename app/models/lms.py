import uuid
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, DateTime, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ==========================================
# 1. MATERIALS (Materi Pembelajaran)
# ==========================================
class Material(Base):
    __tablename__ = "materials"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="SET NULL"), nullable=True)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="SET NULL"), nullable=True)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    subject = relationship("Subject")
    employee = relationship("Employee")
    classroom = relationship("Classroom")
    academic_year = relationship("AcademicYear")
    semester = relationship("Semester")
    progress_records = relationship("StudentMaterialProgress", back_populates="material", cascade="all, delete-orphan")


# ==========================================
# 2. STUDENT MATERIAL PROGRESS (Progres Materi)
# ==========================================
class StudentMaterialProgress(Base):
    __tablename__ = "student_material_progress"
    __table_args__ = (
        UniqueConstraint("student_id", "material_id", name="uq_student_material_progress"),
        {'extend_existing': True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    material_id = Column(UUID(as_uuid=True), ForeignKey("materials.id", ondelete="CASCADE"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    student = relationship("Student")
    material = relationship("Material", back_populates="progress_records")


# ==========================================
# 3. ASSIGNMENTS (Tugas Siswa)
# ==========================================
class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="SET NULL"), nullable=True)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(20), default="file", nullable=False) # essay, file, quiz, coding, project
    file_path = Column(String(500), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=False)
    max_score = Column(Numeric(5, 2), default=100.00, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    subject = relationship("Subject")
    classroom = relationship("Classroom")
    employee = relationship("Employee")
    academic_year = relationship("AcademicYear")
    semester = relationship("Semester")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")


# ==========================================
# 4. SUBMISSIONS (Pengumpulan Tugas)
# ==========================================
class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student_submission"),
        {'extend_existing': True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)

    content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    status = Column(String(30), default="submitted", nullable=False) # draft, submitted, need_revision, graded
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student")
    grade = relationship("Grade", back_populates="submission", uselist=False, cascade="all, delete-orphan")
    histories = relationship("SubmissionHistory", back_populates="submission", cascade="all, delete-orphan")


# ==========================================
# 5. SUBMISSION HISTORIES (Audit Trail Revisi)
# ==========================================
class SubmissionHistory(Base):
    __tablename__ = "submission_histories"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), nullable=False)
    content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    comment = Column(Text, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="histories")
    user = relationship("User")


# ==========================================
# 6. GRADES (Penilaian Tugas)
# ==========================================
class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="CASCADE"), unique=True, nullable=False)
    graded_by = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)

    score = Column(Numeric(5, 2), nullable=False)
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="grade")
    grader = relationship("Employee")


# ==========================================
# 7. PORTFOLIOS (Portofolio Karya Siswa)
# ==========================================
class Portfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=True)
    status = Column(String(20), default="draft", nullable=False) # draft, published

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student")
    submission = relationship("Submission")
