import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ==========================================
# 1. REPORT CARDS (Rapor Semester Siswa)
# ==========================================
class ReportCard(Base):
    __tablename__ = "report_cards"
    __table_args__ = (
        UniqueConstraint("student_id", "academic_year_id", "semester_id", name="uq_student_report_semester"),
        {'extend_existing': True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id", ondelete="RESTRICT"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id", ondelete="RESTRICT"), nullable=False)
    homeroom_teacher_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)

    sick_count = Column(Integer, default=0, nullable=False)
    permitted_count = Column(Integer, default=0, nullable=False)
    unexcused_count = Column(Integer, default=0, nullable=False)
    homeroom_notes = Column(Text, nullable=True)
    status = Column(String(20), default="draft", nullable=False) # draft, locked, published

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student")
    classroom = relationship("Classroom")
    academic_year = relationship("AcademicYear")
    semester = relationship("Semester")
    homeroom_teacher = relationship("Employee")
    items = relationship("ReportCardItem", back_populates="report_card", cascade="all, delete-orphan")


# ==========================================
# 2. REPORT CARD ITEMS (Rincian Nilai Mapel)
# ==========================================
class ReportCardItem(Base):
    __tablename__ = "report_card_items"
    __table_args__ = (
        UniqueConstraint("report_card_id", "subject_id", name="uq_report_card_subject"),
        {'extend_existing': True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_card_id = Column(UUID(as_uuid=True), ForeignKey("report_cards.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)

    knowledge_score = Column(Numeric(5, 2), nullable=True)
    skill_score = Column(Numeric(5, 2), nullable=True)
    final_score = Column(Numeric(5, 2), nullable=False)
    letter_grade = Column(String(5), nullable=False) # A, B, C, D
    competency_description = Column(Text, nullable=True)

    # Relationships
    report_card = relationship("ReportCard", back_populates="items")
    subject = relationship("Subject")
    teacher = relationship("Employee")
