from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

import uuid


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # Mandatory Tables
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)
    # relationship
    curriculums = relationship("Curriculum", back_populates="course")
    classes = relationship("Class", back_populates="course")
    schedules = relationship("Manage_Schedule", back_populates="course")