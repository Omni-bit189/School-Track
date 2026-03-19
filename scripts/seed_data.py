#!/usr/bin/env python3
"""
Seeds the database with a sample school, admin, teachers, classes, and students.
Run once after setting up: python scripts/seed_data.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, Base, engine
from app.models import *
from app.core.security import hash_password
from datetime import date

db = SessionLocal()

print("🌱 Seeding database...")

# ─── School ───────────────────────────────────────────────────
school = School(
    name="Delhi Public School",
    address="123 Main Road",
    city="New Delhi",
    state="Delhi",
    pincode="110001",
    phone="01123456789",
    email="admin@dps.edu.in",
    board="CBSE"
)
db.add(school)
db.flush()
print(f"   ✅ School: {school.name} (id={school.id})")

# ─── Users ────────────────────────────────────────────────────
admin = User(
    school_id=school.id, full_name="Rajesh Kumar",
    email="admin@dps.edu.in", phone="9876543210",
    hashed_password=hash_password("admin123"),
    role=UserRole.SCHOOL_ADMIN
)
teacher1 = User(
    school_id=school.id, full_name="Priya Sharma",
    email="priya@dps.edu.in", phone="9876543211",
    hashed_password=hash_password("teacher123"),
    role=UserRole.TEACHER
)
teacher2 = User(
    school_id=school.id, full_name="Amit Verma",
    email="amit@dps.edu.in", phone="9876543212",
    hashed_password=hash_password("teacher123"),
    role=UserRole.TEACHER
)
parent1 = User(
    school_id=school.id, full_name="Sunita Gupta",
    email="sunita@gmail.com", phone="9876543213",
    hashed_password=hash_password("parent123"),
    role=UserRole.PARENT
)
db.add_all([admin, teacher1, teacher2, parent1])
db.flush()
print(f"   ✅ Users created (admin, 2 teachers, 1 parent)")

# ─── Classes ──────────────────────────────────────────────────
class_8a = Class(school_id=school.id, name="8", section="A", academic_year="2024-25")
class_8b = Class(school_id=school.id, name="8", section="B", academic_year="2024-25")
class_9a = Class(school_id=school.id, name="9", section="A", academic_year="2024-25")
db.add_all([class_8a, class_8b, class_9a])
db.flush()
print(f"   ✅ Classes: 8A, 8B, 9A")

# ─── Subjects ─────────────────────────────────────────────────
math = Subject(school_id=school.id, name="Mathematics", code="MATH")
science = Subject(school_id=school.id, name="Science", code="SCI")
english = Subject(school_id=school.id, name="English", code="ENG")
db.add_all([math, science, english])
db.flush()
print(f"   ✅ Subjects: Math, Science, English")

# ─── Students ─────────────────────────────────────────────────
students_data = [
    ("Arjun Gupta",    "8A-001", class_8a.id, "Sunita Gupta",   "9876543213", "9876543213"),
    ("Kavya Singh",    "8A-002", class_8a.id, "Rakesh Singh",    "9876543214", "9876543214"),
    ("Rohan Mehta",    "8A-003", class_8a.id, "Anita Mehta",     "9876543215", "9876543215"),
    ("Sneha Patel",    "8A-004", class_8a.id, "Vikram Patel",    "9876543216", "9876543216"),
    ("Ananya Rao",     "8B-001", class_8b.id, "Srinivas Rao",   "9876543217", "9876543217"),
    ("Vikram Nair",    "8B-002", class_8b.id, "Meera Nair",      "9876543218", "9876543218"),
]

for name, roll, class_id, parent_name, parent_phone, parent_wa in students_data:
    s = Student(
        school_id=school.id, class_id=class_id,
        full_name=name, roll_number=roll,
        date_of_birth=date(2011, 6, 15),
        gender=GenderEnum.MALE,
        parent_name=parent_name, parent_phone=parent_phone,
        parent_whatsapp=parent_wa,
    )
    db.add(s)

db.flush()
print(f"   ✅ Students: 6 students across 8A and 8B")

# ─── Class Teachers ───────────────────────────────────────────
db.add(ClassTeacher(class_id=class_8a.id, teacher_id=teacher1.id, subject_id=math.id, is_class_teacher=True))
db.add(ClassTeacher(class_id=class_8b.id, teacher_id=teacher2.id, subject_id=science.id, is_class_teacher=True))
db.flush()
print(f"   ✅ Class teachers assigned")

db.commit()
print("\n🎉 Seed complete! Login credentials:")
print("   Admin:   admin@dps.edu.in / admin123")
print("   Teacher: priya@dps.edu.in / teacher123")
print("   Parent:  sunita@gmail.com / parent123")
