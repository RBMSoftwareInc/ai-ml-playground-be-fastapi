"""
Content Management Models
For managing content versions and syncing between frontend and backend
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class ContentVersion(Base):
    """Content version tracking for frontend-backend sync"""
    __tablename__ = "content_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(50), nullable=False, index=True)  # 'use_case', 'industry', 'discovery_tool', 'solution'
    content_id = Column(String(100), nullable=False, index=True)  # ID of the content item
    version = Column(String(50), nullable=False)
    content_data = Column(JSON, nullable=False)  # Full content data
    source = Column(String(50))  # 'frontend', 'backend', 'migration'
    source_file = Column(String(500))  # Original file path
    checksum = Column(String(64))  # Content hash for change detection
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)


class ContentSync(Base):
    """Content synchronization log"""
    __tablename__ = "content_syncs"
    
    id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(String(50), nullable=False)  # 'extraction', 'migration', 'update'
    content_type = Column(String(50), nullable=False)
    source = Column(String(100))  # Source location
    destination = Column(String(100))  # Destination location
    records_processed = Column(Integer, default=0)
    records_success = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    status = Column(String(50), default='pending')  # 'pending', 'running', 'completed', 'failed'
    error_log = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

