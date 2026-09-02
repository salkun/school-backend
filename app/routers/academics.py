from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.models.academic_report import ReportCard, ReportCardItem
from app.schemas.academic_report import (
    ReportCardCreate, ReportCardUpdate, ReportCardResponse,
    ReportCardItemCreate, ReportCardItemResponse, BatchReportCardItemsCreate
)
from app.dependencies import get_current_user, require_admin, require_staff, require_all

router = APIRouter(
    prefix="/api/academics",
    tags=["Academic & Report Cards"]
)

# ==========================================
# 1. REPORT CARDS ENDPOINTS
# ==========================================
@router.post("/report-cards/", response_model=ReportCardResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_staff)])
def create_report_card(data: ReportCardCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Cek duplikasi rapor untuk siswa pada tahun ajaran & semester yang sama
    existing = db.query(ReportCard).filter(
        ReportCard.student_id == data.student_id,
        ReportCard.academic_year_id == data.academic_year_id,
        ReportCard.semester_id == data.semester_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Rapor untuk siswa pada semester dan tahun ajaran ini sudah dibuat")

    homeroom_id = data.homeroom_teacher_id
    if not homeroom_id and current_user.employee:
        homeroom_id = current_user.employee.id

    new_report = ReportCard(
        **data.model_dump(exclude={"homeroom_teacher_id"}),
        homeroom_teacher_id=homeroom_id
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/report-cards/student/{student_id}", response_model=List[ReportCardResponse], dependencies=[Depends(require_all)])
def get_student_report_cards(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(ReportCard).filter(ReportCard.student_id == student_id).all()

@router.get("/report-cards/{report_id}", response_model=ReportCardResponse, dependencies=[Depends(require_all)])
def get_report_card_detail(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(ReportCard).filter(ReportCard.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report card not found")
    return report

@router.put("/report-cards/{report_id}", response_model=ReportCardResponse, dependencies=[Depends(require_staff)])
def update_report_card(report_id: UUID, data: ReportCardUpdate, db: Session = Depends(get_db)):
    report = db.query(ReportCard).filter(ReportCard.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report card not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(report, field, value)
    db.commit()
    db.refresh(report)
    return report

@router.put("/report-cards/{report_id}/publish", response_model=ReportCardResponse, dependencies=[Depends(require_staff)])
def publish_report_card(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(ReportCard).filter(ReportCard.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report card not found")
    report.status = "published"
    db.commit()
    db.refresh(report)
    return report

@router.delete("/report-cards/{report_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_report_card(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(ReportCard).filter(ReportCard.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report card not found")
    db.delete(report)
    db.commit()
    return None


# ==========================================
# 2. REPORT CARD ITEMS (NILAI MAPEL)
# ==========================================
@router.post("/report-cards/{report_id}/items", response_model=List[ReportCardItemResponse], dependencies=[Depends(require_staff)])
def batch_save_report_card_items(report_id: UUID, payload: BatchReportCardItemsCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(ReportCard).filter(ReportCard.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report card not found")

    teacher_id = current_user.employee.id if current_user.employee else None
    saved_items = []

    for item_data in payload.items:
        # Cari jika sudah ada nilai mapel tsb di rapor ini
        item = db.query(ReportCardItem).filter(
            ReportCardItem.report_card_id == report_id,
            ReportCardItem.subject_id == item_data.subject_id
        ).first()

        if item:
            item.knowledge_score = item_data.knowledge_score
            item.skill_score = item_data.skill_score
            item.final_score = item_data.final_score
            item.letter_grade = item_data.letter_grade
            item.competency_description = item_data.competency_description
            item.teacher_id = item_data.teacher_id or teacher_id
        else:
            item = ReportCardItem(
                report_card_id=report_id,
                subject_id=item_data.subject_id,
                teacher_id=item_data.teacher_id or teacher_id,
                knowledge_score=item_data.knowledge_score,
                skill_score=item_data.skill_score,
                final_score=item_data.final_score,
                letter_grade=item_data.letter_grade,
                competency_description=item_data.competency_description
            )
            db.add(item)
        saved_items.append(item)

    db.commit()
    for item in saved_items:
        db.refresh(item)
    return saved_items
