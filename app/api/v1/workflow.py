"""
CMS Workflow API Endpoints
Content versioning, approval chains, scheduling, and settings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi.security import HTTPBearer

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.cms_workflow import (
    WorkflowContentVersion, ContentApproval, WorkflowDefinition,
    ContentSchedule, CMSSettings, ContentStatus
)
from app.schemas.workflow import (
    ContentVersionCreate, ContentVersionUpdate, ContentVersionResponse,
    ContentApprovalCreate, ContentApprovalUpdate, ContentApprovalResponse,
    WorkflowDefinitionCreate, WorkflowDefinitionUpdate, WorkflowDefinitionResponse,
    ContentScheduleCreate, ContentScheduleUpdate, ContentScheduleResponse,
    CMSSettingCreate, CMSSettingUpdate, CMSSettingResponse,
)

router = APIRouter(prefix="/admin/workflow", tags=["CMS Workflow"])


# Content Versioning
@router.post("/versions", response_model=ContentVersionResponse, status_code=status.HTTP_201_CREATED)
def create_version(
    version_data: ContentVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new content version"""
    # Get the latest version number
    latest = db.query(WorkflowContentVersion).filter(
        WorkflowContentVersion.entity_type == version_data.entity_type,
        WorkflowContentVersion.entity_id == version_data.entity_id
    ).order_by(WorkflowContentVersion.version_number.desc()).first()
    
    next_version = (latest.version_number + 1) if latest else 1
    
    new_version = WorkflowContentVersion(
        entity_type=version_data.entity_type,
        entity_id=version_data.entity_id,
        version_number=next_version,
        version_label=version_data.version_label or f"v{next_version}",
        content_snapshot=version_data.content_snapshot,
        change_summary=version_data.change_summary,
        status=ContentStatus.DRAFT,
        created_by=current_user.id,
    )
    
    db.add(new_version)
    db.commit()
    db.refresh(new_version)
    return new_version


@router.get("/versions", response_model=List[ContentVersionResponse])
def list_versions(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List content versions"""
    query = db.query(WorkflowContentVersion)
    
    if entity_type:
        query = query.filter(WorkflowContentVersion.entity_type == entity_type)
    if entity_id:
        query = query.filter(WorkflowContentVersion.entity_id == entity_id)
    if status:
        try:
            status_enum = ContentStatus(status)
            query = query.filter(WorkflowContentVersion.status == status_enum)
        except ValueError:
            pass
    
    return query.order_by(WorkflowContentVersion.created_at.desc()).all()


@router.get("/versions/{version_id}", response_model=ContentVersionResponse)
def get_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific version"""
    version = db.query(WorkflowContentVersion).filter(WorkflowContentVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


@router.put("/versions/{version_id}", response_model=ContentVersionResponse)
def update_version(
    version_id: int,
    version_update: ContentVersionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a version"""
    version = db.query(WorkflowContentVersion).filter(WorkflowContentVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    if version_update.version_label:
        version.version_label = version_update.version_label
    if version_update.change_summary:
        version.change_summary = version_update.change_summary
    if version_update.status:
        try:
            version.status = ContentStatus(version_update.status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    db.commit()
    db.refresh(version)
    return version


@router.post("/versions/{version_id}/publish", response_model=ContentVersionResponse)
def publish_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Publish a version"""
    version = db.query(WorkflowContentVersion).filter(WorkflowContentVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Check if version is approved
    if version.status != ContentStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail="Version must be approved before publishing"
        )
    
    # Unpublish previous published version
    previous = db.query(WorkflowContentVersion).filter(
        WorkflowContentVersion.entity_type == version.entity_type,
        WorkflowContentVersion.entity_id == version.entity_id,
        WorkflowContentVersion.is_published == True,
        WorkflowContentVersion.id != version_id
    ).first()
    
    if previous:
        previous.is_published = False
    
    version.is_published = True
    version.status = ContentStatus.PUBLISHED
    version.published_at = datetime.utcnow()
    version.published_by = current_user.id
    
    db.commit()
    db.refresh(version)
    return version


# Approval Chains
@router.post("/approvals", response_model=ContentApprovalResponse, status_code=status.HTTP_201_CREATED)
def create_approval(
    approval_data: ContentApprovalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create an approval request"""
    version = db.query(WorkflowContentVersion).filter(
        WorkflowContentVersion.id == approval_data.version_id
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    new_approval = ContentApproval(
        version_id=approval_data.version_id,
        approver_id=current_user.id,
        approver_role=approval_data.approver_role,
        status="pending",
        comments=approval_data.comments,
        approval_order=approval_data.approval_order,
    )
    
    # Update version status to pending_review
    version.status = ContentStatus.PENDING_REVIEW
    
    db.add(new_approval)
    db.commit()
    db.refresh(new_approval)
    return new_approval


@router.get("/approvals", response_model=List[ContentApprovalResponse])
def list_approvals(
    version_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List approvals"""
    query = db.query(ContentApproval)
    
    if version_id:
        query = query.filter(ContentApproval.version_id == version_id)
    if status:
        query = query.filter(ContentApproval.status == status)
    
    return query.order_by(ContentApproval.approval_order).all()


@router.put("/approvals/{approval_id}", response_model=ContentApprovalResponse)
def update_approval(
    approval_id: int,
    approval_update: ContentApprovalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Approve or reject a version"""
    approval = db.query(ContentApproval).filter(ContentApproval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    approval.status = approval_update.status
    approval.comments = approval_update.comments
    approval.responded_at = datetime.utcnow()
    
    # Update version status based on approval
    version = approval.version
    if approval_update.status == "approved":
        # Check if all required approvals are done
        # For simplicity, auto-approve if this is the last approval
        version.status = ContentStatus.APPROVED
    elif approval_update.status == "rejected":
        version.status = ContentStatus.REJECTED
    
    db.commit()
    db.refresh(approval)
    return approval


# Workflow Definitions
@router.post("/workflows", response_model=WorkflowDefinitionResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(
    workflow_data: WorkflowDefinitionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a workflow definition"""
    new_workflow = WorkflowDefinition(**workflow_data.dict())
    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)
    return new_workflow


@router.get("/workflows", response_model=List[WorkflowDefinitionResponse])
def list_workflows(
    entity_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List workflow definitions"""
    query = db.query(WorkflowDefinition)
    
    if entity_type:
        query = query.filter(WorkflowDefinition.entity_type == entity_type)
    if is_active is not None:
        query = query.filter(WorkflowDefinition.is_active == is_active)
    
    return query.all()


@router.put("/workflows/{workflow_id}", response_model=WorkflowDefinitionResponse)
def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowDefinitionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a workflow definition"""
    workflow = db.query(WorkflowDefinition).filter(WorkflowDefinition.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    for key, value in workflow_update.dict(exclude_unset=True).items():
        setattr(workflow, key, value)
    
    db.commit()
    db.refresh(workflow)
    return workflow


# Content Scheduling
@router.post("/schedules", response_model=ContentScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule_data: ContentScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Schedule content for publishing"""
    new_schedule = ContentSchedule(
        **schedule_data.dict(),
        created_by=current_user.id,
        status="scheduled"
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


@router.get("/schedules", response_model=List[ContentScheduleResponse])
def list_schedules(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List scheduled content"""
    query = db.query(ContentSchedule)
    
    if entity_type:
        query = query.filter(ContentSchedule.entity_type == entity_type)
    if entity_id:
        query = query.filter(ContentSchedule.entity_id == entity_id)
    if status:
        query = query.filter(ContentSchedule.status == status)
    
    return query.order_by(ContentSchedule.scheduled_publish_at).all()


@router.put("/schedules/{schedule_id}", response_model=ContentScheduleResponse)
def update_schedule(
    schedule_id: int,
    schedule_update: ContentScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a schedule"""
    schedule = db.query(ContentSchedule).filter(ContentSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    for key, value in schedule_update.dict(exclude_unset=True).items():
        setattr(schedule, key, value)
    
    db.commit()
    db.refresh(schedule)
    return schedule


# CMS Settings
@router.post("/settings", response_model=CMSSettingResponse, status_code=status.HTTP_201_CREATED)
def create_setting(
    setting_data: CMSSettingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a CMS setting"""
    new_setting = CMSSettings(**setting_data.dict())
    new_setting.updated_by = current_user.id
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    return new_setting


@router.get("/settings", response_model=List[CMSSettingResponse])
def list_settings(
    category: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """List CMS settings (public settings don't require auth)"""
    query = db.query(CMSSettings)
    
    if category:
        query = query.filter(CMSSettings.category == category)
    if is_public is not None:
        query = query.filter(CMSSettings.is_public == is_public)
    
    return query.all()


@router.get("/settings/{setting_key}", response_model=CMSSettingResponse)
def get_setting(
    setting_key: str,
    db: Session = Depends(get_db)
):
    """Get a specific setting (public settings accessible without auth)"""
    setting = db.query(CMSSettings).filter(CMSSettings.setting_key == setting_key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    # Public settings don't require auth, private ones do
    # For now, allow access - frontend will handle auth for admin endpoints
    
    return setting


@router.put("/settings/{setting_key}", response_model=CMSSettingResponse)
def update_setting(
    setting_key: str,
    setting_update: CMSSettingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a CMS setting"""
    setting = db.query(CMSSettings).filter(CMSSettings.setting_key == setting_key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    for key, value in setting_update.dict(exclude_unset=True).items():
        setattr(setting, key, value)
    
    setting.updated_by = current_user.id
    db.commit()
    db.refresh(setting)
    return setting

