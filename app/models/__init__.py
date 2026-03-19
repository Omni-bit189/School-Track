# Import all models here so Alembic can detect them all
from app.models.school import School
from app.models.user import User, UserRole
from app.models.academic import Class, Subject, ClassTeacher, Student, GenderEnum
from app.models.operations import (
    AttendanceRecord, AttendanceStatus,
    ExamResult, ExamType,
    NotificationLog, NotificationType, NotificationChannel, NotificationStatus,
    Worksheet, WorksheetStatus
)
