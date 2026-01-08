"""
CMS Workflow Models
Content versioning, draft/publish workflow, and approval chains
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ContentStatus(str, enum.Enum):
    """Content status enum"""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class WorkflowContentVersion(Base):
    """Content versioning for workflow (draft/publish/approval)"""
    __tablename__ = "content_versions_new"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)  # 'content_block', 'theme', 'use_case', etc.
    entity_id = Column(String(100), nullable=False, index=True)
    
    # Version info
    version_number = Column(Integer, nullable=False, default=1)
    version_label = Column(String(50))  # 'v1.0', 'Initial', etc.
    
    # Content snapshot
    content_snapshot = Column(JSON, nullable=False)  # Full content state
    
    # Status and workflow
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT, nullable=False, index=True)
    
    # Publishing
    is_published = Column(Boolean, default=False, index=True)
    published_at = Column(DateTime(timezone=True))
    published_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Metadata
    change_summary = Column(Text)  # What changed in this version
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    approvals = relationship("ContentApproval", back_populates="version", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])


class ContentApproval(Base):
    """Approval chain for content"""
    __tablename__ = "content_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("content_versions_new.id"), nullable=False)
    
    # Approver info
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approver_role = Column(String(50))  # Role required for this approval
    
    # Approval details
    status = Column(String(50), nullable=False)  # 'pending', 'approved', 'rejected'
    comments = Column(Text)
    approved_at = Column(DateTime(timezone=True))
    
    # Order in chain
    approval_order = Column(Integer, nullable=False, default=1)
    
    # Timestamps
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True))
    
    # Relationships
    version = relationship("WorkflowContentVersion", back_populates="approvals")
    approver = relationship("User", foreign_keys=[approver_id])


class WorkflowDefinition(Base):
    """Define approval workflows"""
    __tablename__ = "workflow_definitions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Scope
    entity_type = Column(String(50))  # 'content_block', 'theme', etc. or 'all'
    
    # Workflow steps (stored as JSON)
    approval_steps = Column(JSON, nullable=False)  # [{role: 'editor', order: 1}, {role: 'admin', order: 2}]
    
    # Settings
    requires_all_approvers = Column(Boolean, default=True)  # True = all must approve, False = any can approve
    auto_publish_on_approval = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContentSchedule(Base):
    """Schedule content for publishing"""
    __tablename__ = "content_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(100), nullable=False)
    version_id = Column(Integer, ForeignKey("content_versions_new.id"), nullable=True)
    
    # Schedule
    scheduled_publish_at = Column(DateTime(timezone=True), nullable=False, index=True)
    scheduled_unpublish_at = Column(DateTime(timezone=True))  # Optional
    
    # Status
    status = Column(String(50), default='scheduled')  # 'scheduled', 'published', 'cancelled', 'failed'
    
    # Execution
    published_at = Column(DateTime(timezone=True))
    executed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CMSSettings(Base):
    """CMS Configuration and Settings"""
    __tablename__ = "cms_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, nullable=False, index=True)
    setting_value = Column(JSON, nullable=False)
    setting_type = Column(String(50))  # 'string', 'number', 'boolean', 'json', 'array'
    category = Column(String(50))  # 'general', 'workflow', 'publishing', 'security', 'features'
    description = Column(Text)
    is_public = Column(Boolean, default=False)  # Public settings can be read without auth
    
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContentProject(Base):
    """Content editing projects - manages draft/review/publish workflow"""
    __tablename__ = "content_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Workspace context
    workspace_type = Column(String(50), nullable=False, index=True)  # 'industry', 'use_case', 'theme', etc.
    workspace_id = Column(String(100), nullable=False, index=True)  # ID of the workspace being modified
    
    # Project status
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT, nullable=False, index=True)
    
    # Content snapshot - stores all changes in this project
    content_changes = Column(JSON, nullable=False, default=dict)  # {entity_type: {entity_id: {...changes...}}}
    
    # Metadata
    change_summary = Column(Text)  # Summary of changes
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    
    # Review workflow
    submitted_for_review_at = Column(DateTime(timezone=True))
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True))
    review_comments = Column(Text)
    
    # Publishing
    published_at = Column(DateTime(timezone=True))
    published_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    publisher = relationship("User", foreign_keys=[published_by])

