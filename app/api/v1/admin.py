"""
Admin Panel API Endpoints
Content management, themes, assets, actions, AI model configuration
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
from pathlib import Path

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.admin import (
    ContentAsset, Theme, ContentBlock, ActionDefinition,
    OutputTheme, AIModelConfiguration, ContentAuditLog
)
from app.models.industry import Industry
from app.models.use_case import UseCase, UseCaseCategory
from app.models.cms_workflow import ContentProject, ContentStatus
from app.schemas.admin import (
    ContentAsset as ContentAssetSchema,
    ContentAssetCreate,
    ContentAssetUpdate,
    Theme as ThemeSchema,
    ThemeCreate,
    ThemeUpdate,
    ContentBlock as ContentBlockSchema,
    ContentBlockCreate,
    ContentBlockUpdate,
    ActionDefinition as ActionDefinitionSchema,
    ActionDefinitionCreate,
    ActionDefinitionUpdate,
    OutputTheme as OutputThemeSchema,
    OutputThemeCreate,
    OutputThemeUpdate,
    AIModelConfiguration as AIModelConfigurationSchema,
    AIModelConfigurationCreate,
    AIModelConfigurationUpdate,
    IndustryAdminUpdate,
    UseCaseAdminUpdate,
    BulkContentUpdate,
    BulkActionUpdate,
)
from app.core.config import settings

router = APIRouter(tags=["Admin"])


# Content Assets
@router.post("/admin/assets", response_model=ContentAssetSchema)
async def upload_asset(
    file: UploadFile = File(...),
    alt_text: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),  # Comma-separated
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a content asset (image, icon, etc.)"""
    # Create uploads directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR) / "assets"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    asset_id = f"asset_{uuid.uuid4().hex[:12]}"
    filename = f"{asset_id}{file_ext}"
    file_path = upload_dir / filename
    
    # Save file
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Get image dimensions if it's an image
    width, height = None, None
    if file.content_type and file.content_type.startswith("image/"):
        try:
            from PIL import Image
            img = Image.open(file_path)
            width, height = img.size
        except ImportError:
            # PIL not available, skip dimension extraction
            pass
    
    # Parse tags
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    
    # Create database record
    asset = ContentAsset(
        asset_id=asset_id,
        filename=file.filename,
        file_path=str(file_path.relative_to(Path(settings.UPLOAD_DIR))),
        file_type="image" if file.content_type and file.content_type.startswith("image/") else "document",
        mime_type=file.content_type,
        file_size=len(content),
        width=width,
        height=height,
        alt_text=alt_text,
        caption=caption,
        tags=tag_list,
    )
    
    db.add(asset)
    db.commit()
    db.refresh(asset)
    
    return asset


@router.get("/admin/assets", response_model=List[ContentAssetSchema])
def list_assets(
    file_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all content assets"""
    query = db.query(ContentAsset)
    if file_type:
        query = query.filter(ContentAsset.file_type == file_type)
    query = query.filter(ContentAsset.is_active == True)
    return query.offset(skip).limit(limit).all()


@router.get("/admin/assets/{asset_id}", response_model=ContentAssetSchema)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    """Get a specific asset"""
    asset = db.query(ContentAsset).filter(ContentAsset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.patch("/admin/assets/{asset_id}", response_model=ContentAssetSchema)
def update_asset(
    asset_id: str,
    update: ContentAssetUpdate,
    db: Session = Depends(get_db)
):
    """Update an asset"""
    asset = db.query(ContentAsset).filter(ContentAsset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(asset, key, value)
    
    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/admin/assets/{asset_id}")
def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    """Delete an asset (soft delete)"""
    asset = db.query(ContentAsset).filter(ContentAsset.asset_id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    asset.is_active = False
    db.commit()
    return {"message": "Asset deleted"}


# Themes
@router.post("/admin/themes", response_model=ThemeSchema)
def create_theme(theme: ThemeCreate, db: Session = Depends(get_db)):
    """Create a new theme"""
    theme_obj = Theme(
        theme_id=f"theme_{uuid.uuid4().hex[:12]}",
        **theme.dict()
    )
    db.add(theme_obj)
    db.commit()
    db.refresh(theme_obj)
    return theme_obj


@router.get("/admin/themes", response_model=List[ThemeSchema])
def list_themes(
    scope: Optional[str] = None,
    scope_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List themes"""
    query = db.query(Theme).filter(Theme.is_active == True)
    if scope:
        query = query.filter(Theme.scope == scope)
    if scope_id:
        query = query.filter(Theme.scope_id == scope_id)
    return query.all()


@router.get("/admin/themes/{theme_id}", response_model=ThemeSchema)
def get_theme(theme_id: str, db: Session = Depends(get_db)):
    """Get a specific theme"""
    theme = db.query(Theme).filter(Theme.theme_id == theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme


@router.patch("/admin/themes/{theme_id}", response_model=ThemeSchema)
def update_theme(
    theme_id: str,
    update: ThemeUpdate,
    db: Session = Depends(get_db)
):
    """Update a theme"""
    theme = db.query(Theme).filter(Theme.theme_id == theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(theme, key, value)
    
    db.commit()
    db.refresh(theme)
    return theme


# Content Blocks
@router.post("/admin/content-blocks", response_model=ContentBlockSchema)
def create_content_block(
    block: ContentBlockCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a content block"""
    block_obj = ContentBlock(
        block_id=f"block_{uuid.uuid4().hex[:12]}",
        **block.dict()
    )
    db.add(block_obj)
    db.commit()
    db.refresh(block_obj)
    return block_obj


@router.get("/admin/content-blocks", response_model=List[ContentBlockSchema])
def list_content_blocks(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    block_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List content blocks"""
    query = db.query(ContentBlock).filter(ContentBlock.is_visible == True)
    if entity_type:
        query = query.filter(ContentBlock.entity_type == entity_type)
    if entity_id:
        query = query.filter(ContentBlock.entity_id == entity_id)
    if block_type:
        query = query.filter(ContentBlock.block_type == block_type)
    query = query.order_by(ContentBlock.order_index)
    return query.all()


@router.get("/admin/content-blocks/{block_id}", response_model=ContentBlockSchema)
def get_content_block(block_id: str, db: Session = Depends(get_db)):
    """Get a specific content block"""
    block = db.query(ContentBlock).filter(ContentBlock.block_id == block_id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Content block not found")
    return block


@router.patch("/admin/content-blocks/{block_id}", response_model=ContentBlockSchema)
def update_content_block(
    block_id: str,
    update: ContentBlockUpdate,
    db: Session = Depends(get_db)
):
    """Update a content block"""
    block = db.query(ContentBlock).filter(ContentBlock.block_id == block_id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(block, key, value)
    
    db.commit()
    db.refresh(block)
    return block


@router.delete("/admin/content-blocks/{block_id}")
def delete_content_block(block_id: str, db: Session = Depends(get_db)):
    """Delete a content block"""
    block = db.query(ContentBlock).filter(ContentBlock.block_id == block_id).first()
    if not block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    db.delete(block)
    db.commit()
    return {"message": "Content block deleted"}


# Action Definitions
@router.post("/admin/actions", response_model=ActionDefinitionSchema)
def create_action(action: ActionDefinitionCreate, db: Session = Depends(get_db)):
    """Create an action definition"""
    action_obj = ActionDefinition(
        action_id=f"action_{uuid.uuid4().hex[:12]}",
        **action.dict()
    )
    db.add(action_obj)
    db.commit()
    db.refresh(action_obj)
    return action_obj


@router.get("/admin/actions", response_model=List[ActionDefinitionSchema])
def list_actions(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List action definitions"""
    query = db.query(ActionDefinition).filter(ActionDefinition.is_active == True)
    if entity_type:
        query = query.filter(ActionDefinition.entity_type == entity_type)
    if entity_id:
        query = query.filter(ActionDefinition.entity_id == entity_id)
    query = query.order_by(ActionDefinition.order_index)
    return query.all()


@router.patch("/admin/actions/{action_id}", response_model=ActionDefinitionSchema)
def update_action(
    action_id: str,
    update: ActionDefinitionUpdate,
    db: Session = Depends(get_db)
):
    """Update an action definition"""
    action = db.query(ActionDefinition).filter(ActionDefinition.action_id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(action, key, value)
    
    db.commit()
    db.refresh(action)
    return action


# Output Themes
@router.post("/admin/output-themes", response_model=OutputThemeSchema)
def create_output_theme(theme: OutputThemeCreate, db: Session = Depends(get_db)):
    """Create an output theme"""
    theme_obj = OutputTheme(
        theme_id=f"output_theme_{uuid.uuid4().hex[:12]}",
        **theme.dict()
    )
    db.add(theme_obj)
    db.commit()
    db.refresh(theme_obj)
    return theme_obj


@router.get("/admin/output-themes", response_model=List[OutputThemeSchema])
def list_output_themes(
    use_case_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List output themes"""
    query = db.query(OutputTheme).filter(OutputTheme.is_active == True)
    if use_case_id:
        query = query.filter(OutputTheme.use_case_id == use_case_id)
    return query.all()


@router.patch("/admin/output-themes/{theme_id}", response_model=OutputThemeSchema)
def update_output_theme(
    theme_id: str,
    update: OutputThemeUpdate,
    db: Session = Depends(get_db)
):
    """Update an output theme"""
    theme = db.query(OutputTheme).filter(OutputTheme.theme_id == theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Output theme not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(theme, key, value)
    
    db.commit()
    db.refresh(theme)
    return theme


# AI Model Configurations
@router.post("/admin/ai-models", response_model=AIModelConfigurationSchema)
def create_ai_model_config(
    config: AIModelConfigurationCreate,
    db: Session = Depends(get_db)
):
    """Create an AI model configuration"""
    config_obj = AIModelConfiguration(
        config_id=f"model_config_{uuid.uuid4().hex[:12]}",
        **config.dict()
    )
    db.add(config_obj)
    db.commit()
    db.refresh(config_obj)
    return config_obj


@router.get("/admin/ai-models", response_model=List[AIModelConfigurationSchema])
def list_ai_model_configs(
    use_case_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List AI model configurations"""
    query = db.query(AIModelConfiguration)
    if use_case_id:
        query = query.filter(AIModelConfiguration.use_case_id == use_case_id)
    if is_active is not None:
        query = query.filter(AIModelConfiguration.is_active == is_active)
    return query.all()


@router.patch("/admin/ai-models/{config_id}", response_model=AIModelConfigurationSchema)
def update_ai_model_config(
    config_id: str,
    update: AIModelConfigurationUpdate,
    db: Session = Depends(get_db)
):
    """Update an AI model configuration"""
    config = db.query(AIModelConfiguration).filter(
        AIModelConfiguration.config_id == config_id
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="AI model configuration not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(config, key, value)
    
    db.commit()
    db.refresh(config)
    return config


# Industry & Use Case Admin
@router.get("/admin/industries")
def list_all_industries(
    include_inactive: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all industries (admin endpoint - includes inactive)"""
    query = db.query(Industry)
    if not include_inactive:
        query = query.filter(Industry.is_active == True)
    
    industries = query.all()
    return industries


@router.patch("/admin/industries/{industry_id}")
def update_industry(
    industry_id: str,
    update: IndustryAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an industry"""
    industry = db.query(Industry).filter(Industry.industry_id == industry_id).first()
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(industry, key, value)
    
    db.commit()
    db.refresh(industry)
    return industry


@router.get("/admin/use-cases")
def list_all_use_cases(
    industry_id: Optional[str] = None,
    include_inactive: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all use cases (admin endpoint - includes inactive)"""
    query = db.query(UseCase)
    
    if industry_id:
        query = query.filter(UseCase.industry_id == industry_id)
    
    if not include_inactive:
        query = query.filter(UseCase.is_active == True)
    
    use_cases = query.order_by(UseCase.industry_id, UseCase.display_order).all()
    return use_cases


@router.patch("/admin/use-cases/{use_case_id}")
def update_use_case(
    use_case_id: str,
    update: UseCaseAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a use case"""
    use_case = db.query(UseCase).filter(UseCase.use_case_id == use_case_id).first()
    if not use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    
    for key, value in update.dict(exclude_unset=True).items():
        setattr(use_case, key, value)
    
    db.commit()
    db.refresh(use_case)
    return use_case


# Bulk Operations
@router.post("/admin/content-bulk")
def bulk_update_content(
    bulk: BulkContentUpdate,
    db: Session = Depends(get_db)
):
    """Bulk update content blocks"""
    created_blocks = []
    for block_data in bulk.blocks:
        block = ContentBlock(
            block_id=f"block_{uuid.uuid4().hex[:12]}",
            entity_type=bulk.entity_type,
            entity_id=bulk.entity_id,
            **block_data.dict()
        )
        db.add(block)
        created_blocks.append(block)
    
    db.commit()
    return {"message": f"Created {len(created_blocks)} content blocks", "count": len(created_blocks)}


@router.post("/admin/actions-bulk")
def bulk_update_actions(
    bulk: BulkActionUpdate,
    db: Session = Depends(get_db)
):
    """Bulk update actions"""
    created_actions = []
    for action_data in bulk.actions:
        action = ActionDefinition(
            action_id=f"action_{uuid.uuid4().hex[:12]}",
            entity_type=bulk.entity_type,
            entity_id=bulk.entity_id,
            **action_data.dict()
        )
        db.add(action)
        created_actions.append(action)
    
    db.commit()
    return {"message": f"Created {len(created_actions)} actions", "count": len(created_actions)}


# Public API endpoints (for frontend to fetch content)
@router.get("/public/industries")
def list_industries(db: Session = Depends(get_db)):
    """List all active industries with their categories and use cases"""
    industries = db.query(Industry).filter(
        Industry.is_active == True
    ).all()
    
    result = []
    for industry in industries:
        # Get theme
        theme = db.query(Theme).filter(
            Theme.scope == "industry",
            Theme.scope_id == industry.industry_id,
            Theme.is_active == True
        ).first()
        
        # Get categories
        categories_data = []
        categories = db.query(UseCaseCategory).filter(
            UseCaseCategory.category_id.like(f"{industry.industry_id}_%")
        ).order_by(UseCaseCategory.display_order).all()
        
        for category in categories:
            # Get use cases for this category
            use_cases = db.query(UseCase).filter(
                UseCase.category_id == category.category_id,
                UseCase.is_active == True
            ).order_by(UseCase.display_order).all()
            
            use_cases_data = []
            for uc in use_cases:
                # Get content blocks for use case
                blocks = db.query(ContentBlock).filter(
                    ContentBlock.entity_type == "use_case",
                    ContentBlock.entity_id == uc.use_case_id,
                    ContentBlock.is_visible == True
                ).order_by(ContentBlock.order_index).all()
                
                # Build details from blocks and metadata
                details = {
                    "duration": uc.meta_data.get("duration", "") if uc.meta_data else "",
                    "difficulty": uc.meta_data.get("difficulty", "") if uc.meta_data else "",
                    "benefits": uc.tips or [],
                    "how_it_works": uc.long_description or "",
                    "tech_stack": uc.keywords or [],
                }
                
                use_cases_data.append({
                    "key": uc.use_case_id,
                    "label": uc.display_name,
                    "description": uc.short_description,
                    "icon": uc.icon,
                    "route": uc.interactive_route or "#",
                    "details": details,
                })
            
            categories_data.append({
                "title": category.name,
                "icon": category.icon,
                "color": theme.secondary_color if theme else "#6b7280",
                "description": category.description,
                "use_cases": use_cases_data,
            })
        
        # Get content blocks
        blocks = db.query(ContentBlock).filter(
            ContentBlock.entity_type == "industry",
            ContentBlock.entity_id == industry.industry_id,
            ContentBlock.is_visible == True
        ).order_by(ContentBlock.order_index).all()
        
        # Build description and tagline from blocks
        description = industry.description or ""
        tagline = ""
        for block in blocks:
            if block.block_type == "tagline":
                tagline = block.content or ""
            elif block.block_type == "description":
                description = block.content or description
        
        result.append({
            "id": industry.industry_id,
            "name": industry.name,
            "tagline": tagline,
            "description": description,
            "icon": industry.icon,
            "primary_color": theme.primary_color if theme else "#6b7280",
            "secondary_color": theme.secondary_color if theme else "#4b5563",
            "categories": categories_data,
        })
    
    return result


@router.get("/public/industries/{industry_id}/content")
def get_industry_content(industry_id: str, db: Session = Depends(get_db)):
    """Get all content blocks for an industry with full structure"""
    industry = db.query(Industry).filter(Industry.industry_id == industry_id).first()
    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")
    
    theme = db.query(Theme).filter(
        Theme.scope == "industry",
        Theme.scope_id == industry_id,
        Theme.is_active == True
    ).first()
    
    blocks = db.query(ContentBlock).filter(
        ContentBlock.entity_type == "industry",
        ContentBlock.entity_id == industry_id,
        ContentBlock.is_visible == True
    ).order_by(ContentBlock.order_index).all()
    
    # Get categories and use cases
    categories = db.query(UseCaseCategory).filter(
        UseCaseCategory.category_id.like(f"{industry_id}_%")
    ).order_by(UseCaseCategory.display_order).all()
    
    categories_data = []
    for category in categories:
        use_cases = db.query(UseCase).filter(
            UseCase.category_id == category.category_id,
            UseCase.is_active == True
        ).order_by(UseCase.display_order).all()
        
        use_cases_data = []
        for uc in use_cases:
            use_cases_data.append({
                "id": uc.id,
                "key": uc.use_case_id,
                "label": uc.display_name,
                "description": uc.short_description,
                "icon": uc.icon,
                "order": uc.display_order,
            })
        
        categories_data.append({
            "id": category.id,
            "title": category.name,
            "icon": category.icon,
            "description": category.description,
            "order": category.display_order,
            "useCases": use_cases_data,
        })
    
    # Extract tagline and description from blocks
    tagline = ""
    description = industry.description or ""
    for block in blocks:
        if block.block_type == "tagline":
            tagline = block.content or ""
        elif block.block_type == "description":
            description = block.content or description
    
    return {
        "id": industry.industry_id,
        "name": industry.name,
        "tagline": tagline,
        "description": description,
        "icon": industry.icon,
        "primary_color": theme.primary_color if theme else "#6b7280",
        "secondary_color": theme.secondary_color if theme else "#4b5563",
        "categories": categories_data,
        "is_active": industry.is_active,
    }


@router.get("/public/use-cases/{use_case_id}/content")
def get_use_case_content(use_case_id: str, db: Session = Depends(get_db)):
    """Get all content blocks, theme, and config for a use case"""
    blocks = db.query(ContentBlock).filter(
        ContentBlock.entity_type == "use_case",
        ContentBlock.entity_id == use_case_id,
        ContentBlock.is_visible == True
    ).order_by(ContentBlock.order_index).all()
    
    use_case = db.query(UseCase).filter(UseCase.use_case_id == use_case_id).first()
    theme = db.query(Theme).filter(
        Theme.scope == "use_case",
        Theme.scope_id == use_case_id,
        Theme.is_active == True
    ).first()
    
    output_theme = db.query(OutputTheme).filter(
        OutputTheme.use_case_id == use_case_id,
        OutputTheme.is_active == True
    ).first()
    
    model_config = db.query(AIModelConfiguration).filter(
        AIModelConfiguration.use_case_id == use_case_id,
        AIModelConfiguration.is_active == True
    ).first()
    
    actions = db.query(ActionDefinition).filter(
        ActionDefinition.entity_type == "use_case",
        ActionDefinition.entity_id == use_case_id,
        ActionDefinition.is_active == True
    ).order_by(ActionDefinition.order_index).all()
    
    return {
        "use_case": use_case,
        "content_blocks": blocks,
        "theme": theme,
        "output_theme": output_theme,
        "model_config": model_config,
        "actions": actions,
    }


# ==================== CONTENT PROJECTS ====================

@router.get("/admin/projects")
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    workspace_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all content projects with pagination and filtering"""
    query = db.query(ContentProject)
    
    if status:
        try:
            query = query.filter(ContentProject.status == ContentStatus(status))
        except ValueError:
            # Invalid status value, ignore filter
            pass
    if workspace_type:
        query = query.filter(ContentProject.workspace_type == workspace_type)
    
    total = query.count()
    projects = query.order_by(ContentProject.created_at.desc()).offset(skip).limit(limit).all()
    
    # Get user info for created_by names
    user_ids = {p.created_by for p in projects}
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    user_map = {u.id: u.username for u in users}
    
    return {
        "items": [
            {
                "id": p.id,
                "project_id": p.project_id,
                "name": p.name,
                "description": p.description,
                "workspace_type": p.workspace_type,
                "workspace_id": p.workspace_id,
                "status": p.status.value,
                "change_summary": p.change_summary,
                "created_by": p.created_by,
                "created_by_name": user_map.get(p.created_by, "Unknown"),
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                "submitted_for_review_at": p.submitted_for_review_at.isoformat() if p.submitted_for_review_at else None,
                "published_at": p.published_at.isoformat() if p.published_at else None,
            }
            for p in projects
        ],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/admin/projects")
def create_project(
    name: str,
    description: Optional[str] = None,
    workspace_type: str = Form(...),
    workspace_id: str = Form(...),
    change_summary: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new content project"""
    project_id = f"proj_{uuid.uuid4().hex[:12]}"
    
    project = ContentProject(
        project_id=project_id,
        name=name,
        description=description,
        workspace_type=workspace_type,
        workspace_id=workspace_id,
        status=ContentStatus.DRAFT,
        content_changes={},
        change_summary=change_summary,
        created_by=current_user.id,
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "project_id": project.project_id,
        "name": project.name,
        "status": project.status.value,
    }


@router.post("/admin/projects/{project_id}/submit")
def submit_project_for_review(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit project for review"""
    project = db.query(ContentProject).filter(ContentProject.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = ContentStatus.PENDING_REVIEW
    project.submitted_for_review_at = func.now()
    
    db.commit()
    
    return {"status": "submitted", "project_id": project_id}

