from app.database import Base
from app.models.user import User, UserRole
from app.models.school import SchoolIdentity
from app.models.student import Student, StudentIdentity, StudentAddress, StudentContact, StudentParent, StudentEnrollment
from app.models.parent import Parent, StudentParentRelation
from app.models.employee import (
    Employee, EmployeeIdentity, EmployeeContact, 
    EmployeeChild, EmployeePosition
)
from app.models.master import (
    AcademicYear, Semester, Building, Classroom, 
    Subject, Position, HomeroomAssignment, TeachingSchedule,
    employee_subjects
)
from app.models.lms import (
    Material, StudentMaterialProgress, Assignment, 
    Submission, SubmissionHistory, Grade, Portfolio
)
from app.models.academic_report import (
    ReportCard, ReportCardItem
)
from app.models.attendance import (
    AttendanceSession, AttendanceRecord
)
from app.models.communication import (
    Announcement, MediaFile, ActivityLog, SystemSetting
)