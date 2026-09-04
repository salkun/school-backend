from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.models.employee import Employee
from app.schemas.communication import ProfileUpdate, PasswordChangeRequest
from app.dependencies import get_current_user, require_all
from app.core.security import verify_password, get_password_hash

router = APIRouter(
    prefix="/api/profile",
    tags=["Profile & Account"]
)

@router.get("/me", dependencies=[Depends(require_all)])
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.dependencies import resolve_user_roles
    user_roles = resolve_user_roles(current_user, db)

    profile_info = {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "base_role": current_user.role,
        "role": current_user.role,
        "roles": user_roles,
        "is_active": current_user.is_active,
        "school_id": str(current_user.school_id) if current_user.school_id else None,
        "created_at": current_user.created_at,
        "employee_profile": None,
        "student_profile": None
    }

    if current_user.employee:
        emp = current_user.employee
        
        # Ambil daftar jabatan aktif
        from app.models.employee import EmployeePosition
        from app.models.master import Position
        active_positions = (
            db.query(Position)
            .join(EmployeePosition, EmployeePosition.position_id == Position.id)
            .filter(
                EmployeePosition.employee_id == emp.id,
                EmployeePosition.is_active == True
            )
            .all()
        )
        
        profile_info["employee_profile"] = {
            "id": str(emp.id),
            "nip": emp.nip,
            "full_name": emp.full_name,
            "employment_status": emp.employment_status,
            "ptk_type": emp.ptk_type,
            "is_active": emp.is_active,
            "active_positions": [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "code": p.code,
                    "is_structural": p.is_structural
                }
                for p in active_positions
            ]
        }
    elif current_user.students:
        std = current_user.students[0] if isinstance(current_user.students, list) and len(current_user.students) > 0 else current_user.students
        if hasattr(std, 'id'):
            profile_info["student_profile"] = {
                "id": str(std.id),
                "nik": std.nik,
                "nisn": std.nisn,
                "full_name": std.full_name
            }

    return profile_info

@router.put("/me", dependencies=[Depends(require_all)])
def update_my_profile(data: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.email:
        # Periksa apakah email sudah dipakai user lain
        existing = db.query(User).filter(User.email == data.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email sudah digunakan")
        current_user.email = data.email

    if data.full_name:
        if current_user.employee:
            current_user.employee.full_name = data.full_name
        elif current_user.students:
            std = current_user.students[0] if isinstance(current_user.students, list) and len(current_user.students) > 0 else current_user.students
            if hasattr(std, 'full_name'):
                std.full_name = data.full_name

    db.commit()
    db.refresh(current_user)
    return {"message": "Profil berhasil diperbarui", "username": current_user.username, "email": current_user.email}

@router.put("/change-password", dependencies=[Depends(require_all)])
def change_my_password(data: PasswordChangeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Password lama tidak sesuai")
    
    current_user.password = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password berhasil diubah"}
