import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

class SchoolIdentity(Base):
    __tablename__ = "school_identities"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    npsn = Column(String(10), unique=True, index=True, nullable=False)
    address = Column(Text, nullable=False)
    users = relationship("User", back_populates="school")
    employees = relationship("Employee", back_populates="school")
    students = relationship("Student", back_populates="school")
    # Automated Timestamp Audit Trails
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)