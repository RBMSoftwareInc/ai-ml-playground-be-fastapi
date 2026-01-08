"""
Workflow and Versioning Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ContentVersionCreate(BaseModel):
    entity_type: str
    entity_id: str
    version_label: Optional[str] = None
    content_snapshot: Dict[str, Any]
    change_summary: Optional[str] = None


class ContentVersionUpdate(BaseModel):
    version_label: Optional[str] = None
    change_summary: Optional[str] = None
    status: Optional[str] = None  # draft, pending_review, approved, published, rejected, archived


class ContentVersionResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: str
    version_number: int
    version_label: Optional[str]
    content_snapshot: Dict[str, Any]
    status: str
    is_published: bool
    published_at: Optional[datetime]
    published_by: Optional[int]
    change_summary: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class ContentApprovalCreate(BaseModel):
    version_id: int
    approver_role: Optional[str] = None
    comments: Optional[str] = None
    approval_order: int = 1


class ContentApprovalUpdate(BaseModel):
    status: str  # pending, approved, rejected
    comments: Optional[str] = None


class ContentApprovalResponse(BaseModel):
    id: int
    version_id: int
    approver_id: int
    approver_role: Optional[str]
    status: str
    comments: Optional[str]
    approved_at: Optional[datetime]
    approval_order: int
    requested_at: datetime
    responded_at: Optional[datetime]

    class Config:
        from_attributes = True


class WorkflowDefinitionCreate(BaseModel):
    workflow_name: str
    display_name: str
    description: Optional[str] = None
    entity_type: Optional[str] = None
    approval_steps: List[Dict[str, Any]]
    requires_all_approvers: bool = True
    auto_publish_on_approval: bool = False


class WorkflowDefinitionUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    approval_steps: Optional[List[Dict[str, Any]]] = None
    requires_all_approvers: Optional[bool] = None
    auto_publish_on_approval: Optional[bool] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class WorkflowDefinitionResponse(BaseModel):
    id: int
    workflow_name: str
    display_name: str
    description: Optional[str]
    entity_type: Optional[str]
    approval_steps: List[Dict[str, Any]]
    requires_all_approvers: bool
    auto_publish_on_approval: bool
    is_active: bool
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ContentScheduleCreate(BaseModel):
    entity_type: str
    entity_id: str
    version_id: Optional[int] = None
    scheduled_publish_at: datetime
    scheduled_unpublish_at: Optional[datetime] = None


class ContentScheduleUpdate(BaseModel):
    scheduled_publish_at: Optional[datetime] = None
    scheduled_unpublish_at: Optional[datetime] = None
    status: Optional[str] = None


class ContentScheduleResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: str
    version_id: Optional[int]
    scheduled_publish_at: datetime
    scheduled_unpublish_at: Optional[datetime]
    status: str
    published_at: Optional[datetime]
    executed_by: Optional[int]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class CMSSettingCreate(BaseModel):
    setting_key: str
    setting_value: Dict[str, Any]
    setting_type: str = "json"
    category: str = "general"
    description: Optional[str] = None
    is_public: bool = False


class CMSSettingUpdate(BaseModel):
    setting_value: Optional[Dict[str, Any]] = None
    setting_type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class CMSSettingResponse(BaseModel):
    id: int
    setting_key: str
    setting_value: Dict[str, Any]
    setting_type: Optional[str]
    category: Optional[str]
    description: Optional[str]
    is_public: bool
    updated_by: Optional[int]
    updated_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

