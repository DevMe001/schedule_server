from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, String, DateTime, Integer, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

import uuid


class FacultyLoading(Base):
    __tablename__ = "facultyloadings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    acadyear_id = Column(UUID(as_uuid=True), ForeignKey("academicyears.id"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False)
    facultyid = Column(Integer, nullable=False)
    facultystatus = Column(String, nullable=False)
    totalunits = Column(Integer, nullable=True)
    totalhours = Column(Integer, nullable=True)
    ts = Column(Integer, nullable=True)
    rank = Column(String, nullable=False)
    course_code = Column(String, nullable=False)
    course_description = Column(String, nullable=False)
    units = Column(String, nullable=False)
    lec = Column(String, nullable=False)
    lab = Column(String, nullable=False)
    tuition_hours = Column(String, nullable=False)
    day = Column(String, nullable=False)
    fstart_time = Column(Time, nullable=False)  # Add this line
    fend_time = Column(Time, nullable=False)  # Add this line
    classname = Column(String, nullable=False)
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
    __table_args__ = (
        UniqueConstraint('acadyear_id', 'semester_id', 'course_code', 'day', 'fstart_time', 'fend_time', 'roomname',
                         name='unique_schedule_constraint'),
    )
