from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base  # 🔥 use shared Base

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    operation = Column(String(50), nullable=False)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    result = Column(Float, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="calculations")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
