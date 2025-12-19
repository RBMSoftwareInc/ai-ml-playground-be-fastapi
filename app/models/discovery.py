"""
Discovery Tools Models
For Discovery Zone micro-AI tools
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class DiscoveryTool(Base):
    """Discovery tool model"""
    __tablename__ = "discovery_tools"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    icon = Column(String(10))
    description = Column(Text)
    category = Column(String(50), index=True)  # 'design', 'productivity', 'analysis', etc.
    
    # Interaction configuration
    interaction_type = Column(String(50))  # 'input', 'textarea', 'select', 'dragdrop'
    interaction_label = Column(String(255))
    interaction_placeholder = Column(String(255))
    interaction_options = Column(JSON)  # Array of options for select
    
    # Model configuration
    model_message = Column(Text)
    model_prompt_template = Column(Text)
    
    # Visualization
    visualization_type = Column(String(50))  # 'palette', 'chart', 'text', etc.
    visualization_animation = Column(String(50))
    
    # Surprise element
    surprise_type = Column(String(50))  # 'vibe', 'insight', 'prediction', etc.
    surprise_message_template = Column(Text)
    
    # Metadata
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    meta_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    executions = relationship("DiscoveryToolExecution", back_populates="tool")


class DiscoveryToolExecution(Base):
    """Discovery tool execution log"""
    __tablename__ = "discovery_tool_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(String(100), ForeignKey("discovery_tools.tool_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(255), index=True)
    input_data = Column(JSON)
    output_data = Column(JSON)
    visualization_data = Column(JSON)
    surprise_result = Column(JSON)
    execution_time_ms = Column(Integer)
    model_version = Column(String(50))
    success = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    tool = relationship("DiscoveryTool", back_populates="executions")

