"""
Customer Models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    first_name = Column(String(100))
    last_name = Column(String(100))
    
    # Demographics
    date_of_birth = Column(DateTime(timezone=True))
    gender = Column(String(20))
    location = Column(JSON)  # {city, state, country, zip}
    
    # Engagement metrics
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    average_order_value = Column(Float, default=0.0)
    last_order_date = Column(DateTime(timezone=True))
    days_since_last_purchase = Column(Integer, default=0)
    
    # Churn prediction
    churn_probability = Column(Float)
    churn_risk_level = Column(String(50))  # low, medium, high
    
    # Segmentation
    segment_id = Column(Integer, ForeignKey("customer_segments.id"), nullable=True)
    
    # Preferences
    preferences = Column(JSON)
    tags = Column(JSON)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    segment = relationship("CustomerSegment", back_populates="customers")


class CustomerSegment(Base):
    """Customer segment model"""
    __tablename__ = "customer_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    criteria = Column(JSON)  # Segmentation criteria
    characteristics = Column(JSON)  # Segment characteristics
    size = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customers = relationship("Customer", back_populates="segment")

