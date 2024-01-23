from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
import uuid


class Person(Base):
    __tablename__ = "persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    # Foreign Key relationship to Address
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"))
    address = relationship("Address", back_populates="persons")

    # Foreign Key relationship to PhoneNumber
    phone_number_id = Column(UUID(as_uuid=True), ForeignKey("phone_numbers.id"))
    phone_number = relationship("PhoneNumber", back_populates="persons")
