"""
Transaction Models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Transaction(Base):
    """Transaction model for fraud detection and payment processing"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    order_id = Column(String(100), ForeignKey("orders.order_id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Transaction details
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    payment_method = Column(String(50))  # credit_card, debit_card, upi, etc.
    payment_gateway = Column(String(100))
    
    # Fraud detection
    is_fraud = Column(Boolean, default=False)
    fraud_score = Column(Float)
    fraud_reasons = Column(JSON)  # Array of reasons
    
    # Device and location
    device_fingerprint = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    location = Column(JSON)  # {lat, lng, city, country}
    
    # Transaction metadata
    meta_data = Column(JSON)
    status = Column(String(50), default="pending")  # pending, completed, failed, refunded
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
