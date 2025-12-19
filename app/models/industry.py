"""
Industry Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Industry(Base):
    """Industry model"""
    __tablename__ = "industries"
    
    id = Column(Integer, primary_key=True, index=True)
    industry_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    icon = Column(String(10))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

