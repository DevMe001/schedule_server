from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, String, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_building = Column(String(255), nullable=False)
    room_number = Column(String(50), nullable=True)
    is_lab = Column(Boolean, default=False)
    # Mandatory Tables
    created_at = Column(DateTime, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    schedules = relationship("Manage_Schedule", back_populates="room")
