from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

import uuid


class YearLevel(Base):
    __tablename__ = "year_levels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    order = Column(String, nullable=False)
    # Mandatory Tables
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)
    # relationship
    classes = relationship("Class", back_populates="year_level_classec")
    curriculums = relationship("Curriculum", back_populates="year_level")
