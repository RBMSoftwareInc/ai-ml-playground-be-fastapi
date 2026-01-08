"""
Use Case Models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class UseCaseCategory(Base):
    """Use case category model"""
    __tablename__ = "use_case_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    icon = Column(String(50))  # Increased from 10 to 50 to accommodate Material-UI icon names
    description = Column(Text)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())


class UseCase(Base):
    """Use case model"""
    __tablename__ = "use_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    use_case_id = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    industry_id = Column(String(50), ForeignKey("industries.industry_id"), nullable=False)
    category_id = Column(String(100), ForeignKey("use_case_categories.category_id"), nullable=True)
    category = Column(String(100), nullable=False)  # Legacy field for backward compatibility
    short_description = Column(Text)
    long_description = Column(Text)
    theory_content = Column(Text)  # Educational content
    keywords = Column(JSON)  # Array of keywords
    tips = Column(JSON)  # Array of tips/guidance
    icon = Column(String(50))  # Increased from 10 to 50 to accommodate Material-UI icon names
    interactive_route = Column(String(255))
    industry_route = Column(String(255))
    api_endpoint = Column(String(255))  # API endpoint path
    is_dynamic = Column(Boolean, default=False)  # Dynamic use case vs static
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    meta_data = Column(JSON)  # Additional metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    
    # Relationships
    executions = relationship("UseCaseExecution", back_populates="use_case")
    category_ref = relationship("UseCaseCategory", foreign_keys=[category_id])


class UseCaseExecution(Base):
    """Use case execution log"""
    __tablename__ = "use_case_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    use_case_id = Column(String(100), ForeignKey("use_cases.use_case_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(255), index=True)
    input_data = Column(JSON)
    output_data = Column(JSON)
    confidence = Column(Float)
    latency_ms = Column(Integer)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    model_version = Column(String(50))  # Model version used
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    use_case = relationship("UseCase", back_populates="executions")
