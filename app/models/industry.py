"""
Industry Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Industry(Base):
    """Industry model"""
    __tablename__ = "industries"
    
    id = Column(Integer, primary_key=True, index=True)
    industry_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    icon = Column(String(50))  # Increased from 10 to 50 to accommodate Material-UI icon names
    description = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

