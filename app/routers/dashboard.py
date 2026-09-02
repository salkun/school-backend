from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.student import Student
from app.models.employee import Employee
from app.models.master import Classroom, Subject
from app.models.lms import Assignment, Material
from app.models.communication import Announcement
from app.schemas.communication import DashboardStatsResponse
from app.dependencies import require_all

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard Analytics"]
)

@router.get("/stats", response_model=DashboardStatsResponse, dependencies=[Depends(require_all)])
def get_dashboard_statistics(db: Session = Depends(get_db)):
    total_students = db.query(func.count(Student.id)).scalar() or 0
    total_teachers = db.query(func.count(Employee.id)).scalar() or 0
    total_classrooms = db.query(func.count(Classroom.id)).scalar() or 0
    total_subjects = db.query(func.count(Subject.id)).scalar() or 0
    total_assignments = db.query(func.count(Assignment.id)).scalar() or 0
    total_materials = db.query(func.count(Material.id)).scalar() or 0
    total_announcements = db.query(func.count(Announcement.id)).scalar() or 0

    return DashboardStatsResponse(
        total_students=total_students,
        total_teachers=total_teachers,
        total_classrooms=total_classrooms,
        total_subjects=total_subjects,
        total_assignments=total_assignments,
        total_materials=total_materials,
        total_announcements=total_announcements
    )
