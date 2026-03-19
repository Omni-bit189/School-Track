from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class Class(Base):
    """e.g. Class 8 - Section A"""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(50), nullable=False)       # e.g. "8"
    section = Column(String(10), nullable=False)    # e.g. "A"
    academic_year = Column(String(10), nullable=False)  # e.g. "2024-25"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    school = relationship("School", back_populates="classes")
    students = relationship("Student", back_populates="class_")
    teachers = relationship("ClassTeacher", back_populates="class_")
    attendance_records = relationship("AttendanceRecord", back_populates="class_")


class Subject(Base):
    """e.g. Mathematics, Science, English"""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20))       # e.g. "MATH01"
    is_active = Column(Boolean, default=True)

    # Relationships
    school = relationship("School", back_populates="subjects")
    exam_results = relationship("ExamResult", back_populates="subject")
    worksheets = relationship("Worksheet", back_populates="subject")


class ClassTeacher(Base):
    """Links teachers to classes they teach (and optionally which subject)"""
    __tablename__ = "class_teachers"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    is_class_teacher = Column(Boolean, default=False)  # The primary class teacher

    class_ = relationship("Class", back_populates="teachers")
    teacher = relationship("User", back_populates="taught_classes")


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Parent user account

    # Personal info
    full_name = Column(String(255), nullable=False)
    roll_number = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(Enum(GenderEnum))
    admission_number = Column(String(50), unique=True)

    # Parent contact (stored here too for quick access without joining)
    parent_name = Column(String(255))
    parent_phone = Column(String(15))
    parent_whatsapp = Column(String(15))
    parent_email = Column(String(255))

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("School", back_populates="students")
    class_ = relationship("Class", back_populates="students")
    parent = relationship("User", back_populates="students")
    attendance_records = relationship("AttendanceRecord", back_populates="student")
    exam_results = relationship("ExamResult", back_populates="student")
    worksheets = relationship("Worksheet", back_populates="student")
    notifications = relationship("NotificationLog", back_populates="student")
