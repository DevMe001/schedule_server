# models/Curriculum.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
from models.YearLevel import YearLevel
from models.Course import Course

import uuid

class Curriculum(Base):
    __tablename__ = "curriculums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    curriculum_year_name = Column(UUID(as_uuid=True), ForeignKey("mcurriculums.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    year_level_id = Column(UUID(as_uuid=True), ForeignKey("year_levels.id"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False)
    subject_code = Column(String, nullable=False)
    subject_name = Column(String, nullable=False)
    pre_req = Column(String, nullable=True)
    co_req = Column(String, nullable=True)
    lecture_hours = Column(Integer, nullable=True)
    lab_hours = Column(Integer, nullable=True)
    units = Column(Integer, nullable=False)
    tuition_hours = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="curriculums")
    year_level = relationship("YearLevel", back_populates="curriculums")
    semester = relationship("Semester", back_populates="curriculums")
    m_curriculum = relationship("Manage_Curriculum", back_populates="curriculums")

    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)