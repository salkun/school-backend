from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.models.employee import Employee
from app.models.lms import (
    Material, StudentMaterialProgress, Assignment, 
    Submission, SubmissionHistory, Grade, Portfolio
)
from app.schemas.lms import (
    MaterialCreate, MaterialUpdate, MaterialResponse, MaterialProgressResponse,
    AssignmentCreate, AssignmentUpdate, AssignmentResponse,
    SubmissionCreate, SubmissionResponse,
    GradeCreate, GradeResponse,
    PortfolioCreate, PortfolioUpdate, PortfolioResponse
)
from app.dependencies import get_current_user, require_admin, require_staff, require_all

router = APIRouter(
    prefix="/api/lms",
    tags=["LMS (Learning Management System)"]
)

# ==========================================
# 1. MATERIALS ENDPOINTS
# ==========================================
@router.post("/materials/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_staff)])
def create_material(data: MaterialCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    employee_id = current_user.employee.id if current_user.employee else None
    new_material = Material(
        **data.model_dump(),
        employee_id=employee_id
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

@router.get("/materials/subject/{subject_id}", response_model=List[MaterialResponse], dependencies=[Depends(require_all)])
def get_materials_by_subject(subject_id: UUID, db: Session = Depends(get_db)):
    return db.query(Material).filter(Material.subject_id == subject_id, Material.is_active == True).all()

@router.get("/materials/{material_id}", response_model=MaterialResponse, dependencies=[Depends(require_all)])
def get_material_detail(material_id: UUID, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.put("/materials/{material_id}", response_model=MaterialResponse, dependencies=[Depends(require_staff)])
def update_material(material_id: UUID, data: MaterialUpdate, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(material, field, value)
    db.commit()
    db.refresh(material)
    return material

@router.delete("/materials/{material_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_staff)])
def delete_material(material_id: UUID, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()
    return None

@router.post("/materials/{material_id}/toggle-complete", dependencies=[Depends(require_all)])
def toggle_material_complete(material_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=403, detail="Hanya akun siswa yang dapat menandai progres materi")

    progress = db.query(StudentMaterialProgress).filter(
        StudentMaterialProgress.student_id == student.id,
        StudentMaterialProgress.material_id == material_id
    ).first()

    if progress:
        db.delete(progress)
        db.commit()
        return {"completed": False, "message": "Progres materi dibatalkan"}
    else:
        new_progress = StudentMaterialProgress(student_id=student.id, material_id=material_id)
        db.add(new_progress)
        db.commit()
        return {"completed": True, "message": "Materi selesai dipelajari"}


# ==========================================
# 2. ASSIGNMENTS ENDPOINTS
# ==========================================
@router.post("/assignments/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_staff)])
def create_assignment(data: AssignmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    employee_id = current_user.employee.id if current_user.employee else None
    new_assignment = Assignment(
        **data.model_dump(),
        employee_id=employee_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.get("/assignments/subject/{subject_id}", response_model=List[AssignmentResponse], dependencies=[Depends(require_all)])
def get_assignments_by_subject(subject_id: UUID, db: Session = Depends(get_db)):
    return db.query(Assignment).filter(Assignment.subject_id == subject_id, Assignment.is_active == True).all()

@router.get("/assignments/upcoming", response_model=List[AssignmentResponse], dependencies=[Depends(require_all)])
def get_upcoming_assignments(db: Session = Depends(get_db)):
    now = datetime.now()
    return db.query(Assignment).filter(
        Assignment.deadline >= now,
        Assignment.is_active == True
    ).order_by(Assignment.deadline.asc()).limit(10).all()

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse, dependencies=[Depends(require_all)])
def get_assignment_detail(assignment_id: UUID, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse, dependencies=[Depends(require_staff)])
def update_assignment(assignment_id: UUID, data: AssignmentUpdate, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(assignment, field, value)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_staff)])
def delete_assignment(assignment_id: UUID, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return None


# ==========================================
# 3. SUBMISSIONS & GRADES ENDPOINTS
# ==========================================
@router.post("/submissions/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_all)])
def submit_assignment(data: SubmissionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=403, detail="Hanya akun siswa yang dapat mengumpulkan tugas")

    # Cek apakah sudah pernah submit
    existing_sub = db.query(Submission).filter(
        Submission.assignment_id == data.assignment_id,
        Submission.student_id == student.id
    ).first()

    if existing_sub:
        # Catat riwayat revisi
        history = SubmissionHistory(
            submission_id=existing_sub.id,
            status=existing_sub.status,
            content=existing_sub.content,
            file_path=existing_sub.file_path,
            comment="Revisi / Submit ulang jawaban",
            changed_by=current_user.id
        )
        db.add(history)
        
        # Update submission
        existing_sub.content = data.content
        existing_sub.file_path = data.file_path
        existing_sub.status = data.status
        existing_sub.submitted_at = datetime.now()
        db.commit()
        db.refresh(existing_sub)
        return existing_sub
    else:
        new_sub = Submission(
            assignment_id=data.assignment_id,
            student_id=student.id,
            content=data.content,
            file_path=data.file_path,
            status=data.status
        )
        db.add(new_sub)
        db.commit()
        db.refresh(new_sub)
        return new_sub

@router.get("/assignments/{assignment_id}/submissions", response_model=List[SubmissionResponse], dependencies=[Depends(require_staff)])
def get_submissions_for_assignment(assignment_id: UUID, db: Session = Depends(get_db)):
    return db.query(Submission).filter(Submission.assignment_id == assignment_id).all()

@router.post("/submissions/{submission_id}/grade", response_model=GradeResponse, dependencies=[Depends(require_staff)])
def grade_submission(submission_id: UUID, data: GradeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    employee_id = current_user.employee.id if current_user.employee else None

    grade = db.query(Grade).filter(Grade.submission_id == submission_id).first()
    if grade:
        grade.score = data.score
        grade.feedback = data.feedback
        grade.graded_by = employee_id
    else:
        grade = Grade(
            submission_id=submission_id,
            graded_by=employee_id,
            score=data.score,
            feedback=data.feedback
        )
        db.add(grade)

    submission.status = "graded"
    db.commit()
    db.refresh(grade)
    return grade


# ==========================================
# 4. PORTFOLIOS ENDPOINTS
# ==========================================
@router.post("/portfolios/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_all)])
def create_portfolio(data: PortfolioCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=403, detail="Hanya akun siswa yang dapat membuat portofolio")

    portfolio = Portfolio(
        **data.model_dump(),
        student_id=student.id
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.get("/portfolios/student/{student_id}", response_model=List[PortfolioResponse], dependencies=[Depends(require_all)])
def get_student_portfolios(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(Portfolio).filter(Portfolio.student_id == student_id).all()

@router.delete("/portfolios/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_all)])
def delete_portfolio(portfolio_id: UUID, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    db.delete(portfolio)
    db.commit()
    return None
