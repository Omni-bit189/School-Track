from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Enum, Float, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base


# ─── Attendance ───────────────────────────────────────────────

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Teacher who marked
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    note = Column(String(255))   # Optional note e.g. "Doctor's appointment"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="attendance_records")
    class_ = relationship("Class", back_populates="attendance_records")


# ─── Exam Results ─────────────────────────────────────────────

class ExamType(str, enum.Enum):
    UNIT_TEST = "unit_test"
    MID_TERM = "mid_term"
    FINAL = "final"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"


class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    exam_type = Column(Enum(ExamType), nullable=False)
    exam_name = Column(String(255))         # e.g. "Unit Test 1 - Chapter 3"
    exam_date = Column(Date)
    marks_obtained = Column(Float, nullable=False)
    total_marks = Column(Float, nullable=False)
    percentage = Column(Float)              # Computed on insert
    grade = Column(String(5))              # A+, A, B etc.

    # AI-extracted topic analysis (from uploaded exam paper)
    topic_scores = Column(JSON)            # e.g. {"Algebra": 60, "Geometry": 85}
    weak_topics = Column(JSON)             # e.g. ["Algebra", "Fractions"]

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="exam_results")
    subject = relationship("Subject", back_populates="exam_results")


# ─── Notifications ────────────────────────────────────────────

class NotificationType(str, enum.Enum):
    ABSENCE_ALERT = "absence_alert"
    RESULT_SHARE = "result_share"
    WORKSHEET_SHARE = "worksheet_share"
    GENERAL = "general"


class NotificationChannel(str, enum.Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"
    VOICE_CALL = "voice_call"
    EMAIL = "email"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    channel = Column(Enum(NotificationChannel), nullable=False)
    recipient_phone = Column(String(15))
    recipient_email = Column(String(255))
    message_body = Column(Text)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    external_id = Column(String(255))     # Twilio SID or MSG91 ID for tracking
    error_message = Column(Text)
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="notifications")


# ─── AI Worksheets ────────────────────────────────────────────

class WorksheetStatus(str, enum.Enum):
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"
    SENT = "sent"


class Worksheet(Base):
    __tablename__ = "worksheets"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    generated_for_result_id = Column(Integer, ForeignKey("exam_results.id"), nullable=True)

    title = Column(String(255))
    weak_topics = Column(JSON)             # Topics this worksheet targets
    content = Column(JSON)                 # Full worksheet content (questions, sections)
    difficulty_level = Column(String(20))  # easy, medium, hard
    status = Column(Enum(WorksheetStatus), default=WorksheetStatus.GENERATING)
    file_path = Column(String(500))        # Local path to generated PDF (later)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))

    student = relationship("Student", back_populates="worksheets")
    subject = relationship("Subject", back_populates="worksheets")
