from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from app.db.session import get_db
from app.models.operations import AttendanceRecord, AttendanceStatus
from app.models.academic import Student
from app.core.security import get_current_user

router = APIRouter()


# ─── Schemas ──────────────────────────────────────────────────

class AttendanceEntry(BaseModel):
    student_id: int
    status: AttendanceStatus
    note: Optional[str] = None


class BulkAttendanceRequest(BaseModel):
    class_id: int
    date: date
    records: List[AttendanceEntry]


class AttendanceOut(BaseModel):
    id: int
    student_id: int
    class_id: int
    date: date
    status: AttendanceStatus
    note: Optional[str]

    class Config:
        from_attributes = True


class AttendanceSummary(BaseModel):
    student_id: int
    student_name: str
    total_days: int
    present: int
    absent: int
    late: int
    attendance_percentage: float


# ─── Endpoints ────────────────────────────────────────────────

@router.post("/bulk", status_code=201)
def mark_bulk_attendance(
    payload: BulkAttendanceRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Mark attendance for an entire class at once — primary teacher flow."""
    # Check if attendance already marked for this class+date
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.class_id == payload.class_id,
        AttendanceRecord.date == payload.date
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Attendance already marked for this class on {payload.date}"
        )

    records = []
    for entry in payload.records:
        record = AttendanceRecord(
            student_id=entry.student_id,
            class_id=payload.class_id,
            marked_by=current_user.id,
            date=payload.date,
            status=entry.status,
            note=entry.note,
        )
        records.append(record)

    db.bulk_save_objects(records)
    db.commit()

    # Identify absentees for notification (returned so caller can trigger alerts)
    absentees = [e.student_id for e in payload.records if e.status == AttendanceStatus.ABSENT]
    return {
        "message": f"Attendance marked for {len(records)} students",
        "absentee_ids": absentees,
        "date": payload.date,
    }


@router.get("/class/{class_id}", response_model=List[AttendanceOut])
def get_class_attendance(
    class_id: int,
    date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(AttendanceRecord).filter(AttendanceRecord.class_id == class_id)
    if date:
        query = query.filter(AttendanceRecord.date == date)
    return query.order_by(AttendanceRecord.date.desc()).all()


@router.get("/student/{student_id}/summary", response_model=AttendanceSummary)
def get_student_attendance_summary(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    records = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student_id).all()
    total = len(records)
    present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
    absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
    late = sum(1 for r in records if r.status == AttendanceStatus.LATE)

    return AttendanceSummary(
        student_id=student_id,
        student_name=student.full_name,
        total_days=total,
        present=present,
        absent=absent,
        late=late,
        attendance_percentage=round((present / total * 100) if total > 0 else 0, 2)
    )
