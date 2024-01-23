# models/Curriculum.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
from models.YearLevel import YearLevel
from models.Course import Course

import uuid


class Class(Base):
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    classname = Column(String(50), nullable=False)
    year_level_id = Column(UUID(as_uuid=True), ForeignKey("year_levels.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)

    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    year_level_classec = relationship("YearLevel", back_populates="classes")
    course = relationship("Course", back_populates="classes")
    section = relationship("Section", back_populates="classes")
    schedules = relationship("Manage_Schedule", back_populates="classes")
