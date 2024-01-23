from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, String, DateTime, Integer, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid


class FacultyLoading(Base):
    __tablename__ = "facultyloadings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    acadyear_id = Column(UUID(as_uuid=True), ForeignKey("academicyears.id"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False)
    facultyname = Column(String(50), nullable=False)
    facultystatus = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    course_code = Column(String, nullable=False)
    course_description = Column(String, nullable=False)
    units = Column(String, nullable=False)
    lec = Column(String, nullable=False)
    lab = Column(String, nullable=False)
    classname = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    roomname = Column(String, nullable=False)
    # Relationships
    acadyear = relationship("AcademicYear", back_populates="facultyloadings")
    semester = relationship("Semester", back_populates="facultyloadings")
    # Mandatory Tables
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)