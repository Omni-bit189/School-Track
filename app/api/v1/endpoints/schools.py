from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.db.session import get_db
from app.models.school import School
from app.models.academic import Class, Subject
from app.core.security import get_current_user, require_role

router = APIRouter()


# ─── School Schemas ───────────────────────────────────────────

class SchoolCreate(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    board: Optional[str] = None  # CBSE, ICSE, State Board


class SchoolOut(BaseModel):
    id: int
    name: str
    city: Optional[str]
    board: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


# ─── Class Schemas ────────────────────────────────────────────

class ClassCreate(BaseModel):
    name: str           # "8"
    section: str        # "A"
    academic_year: str  # "2024-25"


class ClassOut(BaseModel):
    id: int
    name: str
    section: str
    academic_year: str
    school_id: int

    class Config:
        from_attributes = True


# ─── Subject Schemas ──────────────────────────────────────────

class SubjectCreate(BaseModel):
    name: str
    code: Optional[str] = None


class SubjectOut(BaseModel):
    id: int
    name: str
    code: Optional[str]

    class Config:
        from_attributes = True


# ─── School Endpoints ─────────────────────────────────────────

@router.post("/", response_model=SchoolOut, status_code=201)
def create_school(
    payload: SchoolCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("super_admin"))
):
    school = School(**payload.model_dump())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


@router.get("/mine", response_model=SchoolOut)
def get_my_school(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    school = db.query(School).filter(School.id == current_user.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


# ─── Class Endpoints ──────────────────────────────────────────

@router.post("/{school_id}/classes", response_model=ClassOut, status_code=201)
def create_class(
    school_id: int,
    payload: ClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    class_ = Class(school_id=school_id, **payload.model_dump())
    db.add(class_)
    db.commit()
    db.refresh(class_)
    return class_


@router.get("/{school_id}/classes", response_model=List[ClassOut])
def list_classes(
    school_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Class).filter(Class.school_id == school_id, Class.is_active == True).all()


# ─── Subject Endpoints ────────────────────────────────────────

@router.post("/{school_id}/subjects", response_model=SubjectOut, status_code=201)
def create_subject(
    school_id: int,
    payload: SubjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    subject = Subject(school_id=school_id, **payload.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("/{school_id}/subjects", response_model=List[SubjectOut])
def list_subjects(
    school_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Subject).filter(Subject.school_id == school_id, Subject.is_active == True).all()
