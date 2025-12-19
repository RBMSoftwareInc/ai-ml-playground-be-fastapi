"""
Analytics Models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class AnalyticsEvent(Base):
    """Analytics event model"""
    __tablename__ = "analytics_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    session_id = Column(String(255), index=True)
    
    # Event data
    event_data = Column(JSON)
    properties = Column(JSON)
    
    # Context
    page_url = Column(String(500))
    referrer = Column(String(500))
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class ABTest(Base):
    """A/B test model"""
    __tablename__ = "ab_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Test configuration
    primary_kpi = Column(String(100))  # conversion, revenue, engagement, etc.
    traffic_split = Column(String(50))  # "50/50", "70/30", etc.
    required_sample_size = Column(Integer)
    confidence_level = Column(Float)  # 0.95 for 95%
    
    # Variants
    variants = Column(JSON)  # [{name: "A", config: {}}, {name: "B", config: {}}]
    
    # Status
    status = Column(String(50), default="draft")  # draft, running, paused, completed
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ABTestResult(Base):
    """A/B test result model"""
    __tablename__ = "ab_test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(String(100), ForeignKey("ab_tests.test_id"), nullable=False)
    variant_name = Column(String(100), nullable=False)
    
    # Metrics
    visitors = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    average_order_value = Column(Float, default=0.0)
    
    # Statistical significance
    is_significant = Column(Boolean, default=False)
    p_value = Column(Float)
    confidence_interval = Column(JSON)  # [lower, upper]
    
    # Winner
    is_winner = Column(Boolean, default=False)
    lift_percentage = Column(Float)
    
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

