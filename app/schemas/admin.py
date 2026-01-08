"""
Admin Panel Schemas
Pydantic schemas for content management, themes, assets, and AI model configuration
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime


# Content Asset Schemas
class ContentAssetBase(BaseModel):
    filename: str
    file_type: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    tags: Optional[List[str]] = None


class ContentAssetCreate(ContentAssetBase):
    pass


class ContentAssetUpdate(BaseModel):
    filename: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ContentAsset(ContentAssetBase):
    id: int
    asset_id: str
    file_path: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Theme Schemas
class ThemeBase(BaseModel):
    name: str
    description: Optional[str] = None
    scope: str  # 'global', 'industry', 'use_case', 'component'
    scope_id: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    custom_colors: Optional[Dict[str, str]] = None
    font_family: Optional[str] = None
    font_sizes: Optional[Dict[str, str]] = None
    spacing_scale: Optional[Dict[str, str]] = None
    border_radius: Optional[Dict[str, str]] = None
    component_styles: Optional[Dict[str, Any]] = None
    animation_config: Optional[Dict[str, Any]] = None


class ThemeCreate(ThemeBase):
    pass


class ThemeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    custom_colors: Optional[Dict[str, str]] = None
    font_family: Optional[str] = None
    font_sizes: Optional[Dict[str, str]] = None
    spacing_scale: Optional[Dict[str, str]] = None
    border_radius: Optional[Dict[str, str]] = None
    component_styles: Optional[Dict[str, Any]] = None
    animation_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Theme(ThemeBase):
    id: int
    theme_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Content Block Schemas
class ContentBlockBase(BaseModel):
    content_type: str  # 'text', 'html', 'markdown', 'json'
    entity_type: str  # 'industry', 'use_case', 'category'
    entity_id: str
    block_type: Optional[str] = None
    block_key: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    raw_content: Optional[Dict[str, Any]] = None
    order_index: int = 0
    is_visible: bool = True
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None


class ContentBlockCreate(ContentBlockBase):
    pass


class ContentBlockUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    raw_content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None
    is_visible: Optional[bool] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[List[str]] = None


class ContentBlock(ContentBlockBase):
    id: int
    block_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Action Definition Schemas
class ActionDefinitionBase(BaseModel):
    entity_type: str
    entity_id: Optional[str] = None
    name: str
    label: Optional[str] = None
    description: Optional[str] = None
    action_type: str  # 'button', 'link', 'api_call', 'workflow', 'navigation'
    config: Optional[Dict[str, Any]] = None
    icon: Optional[str] = None
    button_style: Optional[str] = None
    button_size: Optional[str] = None
    position: Optional[str] = None
    order_index: int = 0
    visibility_conditions: Optional[Dict[str, Any]] = None
    permissions: Optional[List[str]] = None


class ActionDefinitionCreate(ActionDefinitionBase):
    pass


class ActionDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    icon: Optional[str] = None
    button_style: Optional[str] = None
    button_size: Optional[str] = None
    position: Optional[str] = None
    order_index: Optional[int] = None
    visibility_conditions: Optional[Dict[str, Any]] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ActionDefinition(ActionDefinitionBase):
    id: int
    action_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Output Theme Schemas
class OutputThemeBase(BaseModel):
    use_case_id: str
    name: str
    description: Optional[str] = None
    visualization_type: Optional[str] = None
    chart_config: Optional[Dict[str, Any]] = None
    color_scheme: Optional[Dict[str, Any]] = None
    layout_config: Optional[Dict[str, Any]] = None
    data_transform: Optional[Dict[str, Any]] = None
    template: Optional[str] = None
    is_default: bool = False


class OutputThemeCreate(OutputThemeBase):
    pass


class OutputThemeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visualization_type: Optional[str] = None
    chart_config: Optional[Dict[str, Any]] = None
    color_scheme: Optional[Dict[str, Any]] = None
    layout_config: Optional[Dict[str, Any]] = None
    data_transform: Optional[Dict[str, Any]] = None
    template: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class OutputTheme(OutputThemeBase):
    id: int
    theme_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# AI Model Configuration Schemas
class AIModelConfigurationBase(BaseModel):
    use_case_id: str
    model_name: str
    model_type: str
    model_provider: Optional[str] = None
    model_version: Optional[str] = None
    model_endpoint: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    training_enabled: bool = False
    training_data_source: Optional[str] = None
    training_parameters: Optional[Dict[str, Any]] = None
    test_enabled: bool = False
    test_dataset_path: Optional[str] = None
    test_thresholds: Optional[Dict[str, Any]] = None
    deployment_environment: Optional[str] = None
    monitoring_enabled: bool = False
    alert_thresholds: Optional[Dict[str, Any]] = None


class AIModelConfigurationCreate(AIModelConfigurationBase):
    pass


class AIModelConfigurationUpdate(BaseModel):
    model_name: Optional[str] = None
    model_type: Optional[str] = None
    model_provider: Optional[str] = None
    model_version: Optional[str] = None
    model_endpoint: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    training_enabled: Optional[bool] = None
    training_data_source: Optional[str] = None
    training_parameters: Optional[Dict[str, Any]] = None
    test_enabled: Optional[bool] = None
    test_dataset_path: Optional[str] = None
    test_thresholds: Optional[Dict[str, Any]] = None
    deployment_environment: Optional[str] = None
    monitoring_enabled: Optional[bool] = None
    alert_thresholds: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class AIModelConfiguration(AIModelConfigurationBase):
    id: int
    config_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Industry & Use Case Admin Schemas
class IndustryAdminUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    tagline: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    is_active: Optional[bool] = None


class UseCaseAdminUpdate(BaseModel):
    display_name: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    theory_content: Optional[str] = None
    icon: Optional[str] = None
    keywords: Optional[List[str]] = None
    tips: Optional[List[str]] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None
    meta_data: Optional[Dict[str, Any]] = None


# Bulk Operations
class BulkContentUpdate(BaseModel):
    entity_type: str
    entity_id: str
    blocks: List[ContentBlockCreate]


class BulkActionUpdate(BaseModel):
    entity_type: str
    entity_id: str
    actions: List[ActionDefinitionCreate]

