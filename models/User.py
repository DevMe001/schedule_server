from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Credentials
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    # User Details
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    usertype = Column(String(25), nullable=False)
    # Mandatory tables
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)
