# models/Curriculum.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
from models.YearLevel import YearLevel
from models.Course import Course

import uuid


class Manage_Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    acadyear_id = Column(UUID(as_uuid=True), ForeignKey("academicyears.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    subject_code = Column(String, nullable=False)
    subject_name = Column(String, nullable=False)
    lecture_hours = Column(Integer, nullable=True)
    lab_hours = Column(Integer, nullable=True)
    units = Column(Integer, nullable=False)
    tuition_hours = Column(Integer, nullable=False)
    day = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)  # Add this line
    end_time = Column(Time, nullable=False)  # Add this line
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    acadyear = relationship("AcademicYear", back_populates="schedules")
    course = relationship("Course", back_populates="schedules")
    semester = relationship("Semester", back_populates="schedules")
    room = relationship("Room", back_populates="schedules")
    classes = relationship("Class", back_populates="schedules")

    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)
    __table_args__ = (
        UniqueConstraint('acadyear_id', 'semester_id', 'day', 'start_time', 'end_time', 'room_id',
                         name='unique_scheduling_constraint'),
    )