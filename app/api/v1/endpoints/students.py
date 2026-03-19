from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

from app.db.session import get_db
from app.models.academic import Student, GenderEnum
from app.core.security import get_current_user

router = APIRouter()


# ─── Schemas ──────────────────────────────────────────────────

class StudentCreate(BaseModel):
    full_name: str
    class_id: int
    roll_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
    admission_number: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_whatsapp: Optional[str] = None
    parent_email: Optional[EmailStr] = None


class StudentOut(BaseModel):
    id: int
    full_name: str
    roll_number: Optional[str]
    class_id: int
    parent_name: Optional[str]
    parent_phone: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


# ─── Endpoints ────────────────────────────────────────────────

@router.post("/", response_model=StudentOut, status_code=201)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = Student(
        school_id=current_user.school_id,
        **payload.model_dump()
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=List[StudentOut])
def list_students(
    class_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Student).filter(
        Student.school_id == current_user.school_id,
        Student.is_active == True
    )
    if class_id:
        query = query.filter(Student.class_id == class_id)
    return query.all()


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.school_id == current_user.school_id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=204)
def deactivate_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.school_id == current_user.school_id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.is_active = False
    db.commit()
