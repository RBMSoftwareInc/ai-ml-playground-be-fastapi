"""
Content Management System Models
For admin panel - managing industries, use cases, themes, assets, and AI models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ContentAsset(Base):
    """Media assets (images, icons, files)"""
    __tablename__ = "content_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String(100), unique=True, index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50))  # 'image', 'icon', 'document', 'video'
    mime_type = Column(String(100))
    file_size = Column(Integer)  # in bytes
    width = Column(Integer)  # for images
    height = Column(Integer)  # for images
    alt_text = Column(Text)
    caption = Column(Text)
    tags = Column(JSON)  # Array of tags
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Theme(Base):
    """UI Theme and styling configuration"""
    __tablename__ = "themes"
    
    id = Column(Integer, primary_key=True, index=True)
    theme_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    scope = Column(String(50), nullable=False)  # 'global', 'industry', 'use_case', 'component'
    scope_id = Column(String(100), nullable=True)  # ID of the scoped entity
    
    # Color scheme
    primary_color = Column(String(20))
    secondary_color = Column(String(20))
    accent_color = Column(String(20))
    background_color = Column(String(20))
    text_color = Column(String(20))
    custom_colors = Column(JSON)  # Additional custom colors
    
    # Typography
    font_family = Column(String(100))
    font_sizes = Column(JSON)  # {h1, h2, body, caption, etc.}
    
    # Spacing & Layout
    spacing_scale = Column(JSON)  # Spacing scale
    border_radius = Column(JSON)  # Border radius values
    
    # Component styling
    component_styles = Column(JSON)  # Component-specific styles
    
    # Animations
    animation_config = Column(JSON)  # Animation settings
    
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ContentBlock(Base):
    """Rich content blocks for use cases and industries"""
    __tablename__ = "content_blocks"
    
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(String(100), unique=True, index=True, nullable=False)
    content_type = Column(String(50), nullable=False)  # 'text', 'html', 'markdown', 'json'
    entity_type = Column(String(50), nullable=False)  # 'industry', 'use_case', 'category'
    entity_id = Column(String(100), nullable=False, index=True)
    block_type = Column(String(50))  # 'description', 'details', 'theory', 'benefits', 'how_it_works', 'custom'
    block_key = Column(String(100))  # Specific key for the block (e.g., 'overview', 'benefits_list')
    
    # Content
    title = Column(String(255))
    content = Column(Text)  # Rich text, HTML, or Markdown
    raw_content = Column(JSON)  # Structured content (for rich editors)
    
    # Metadata
    order_index = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)
    
    # SEO & Meta
    meta_title = Column(String(255))
    meta_description = Column(Text)
    keywords = Column(JSON)
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ActionDefinition(Base):
    """Action definitions for use cases (buttons, workflows, etc.)"""
    __tablename__ = "action_definitions"
    
    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(String(100), unique=True, index=True, nullable=False)
    entity_type = Column(String(50), nullable=False)  # 'industry', 'use_case', 'global'
    entity_id = Column(String(100), nullable=True)
    
    name = Column(String(255), nullable=False)
    label = Column(String(255))
    description = Column(Text)
    action_type = Column(String(50), nullable=False)  # 'button', 'link', 'api_call', 'workflow', 'navigation'
    
    # Action configuration
    config = Column(JSON)  # Type-specific configuration
    
    # UI Configuration
    icon = Column(String(50))
    button_style = Column(String(50))  # 'primary', 'secondary', 'outlined', etc.
    button_size = Column(String(50))  # 'small', 'medium', 'large'
    position = Column(String(50))  # 'header', 'body', 'footer', 'sidebar'
    order_index = Column(Integer, default=0)
    
    # Conditions & Visibility
    visibility_conditions = Column(JSON)  # When to show this action
    permissions = Column(JSON)  # Required permissions
    
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OutputTheme(Base):
    """Output visualization and theming for AI results"""
    __tablename__ = "output_themes"
    
    id = Column(Integer, primary_key=True, index=True)
    theme_id = Column(String(100), unique=True, index=True, nullable=False)
    use_case_id = Column(String(100), ForeignKey("use_cases.use_case_id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Visualization type
    visualization_type = Column(String(50))  # 'chart', 'table', 'card', 'timeline', 'map', 'custom'
    
    # Styling
    chart_config = Column(JSON)  # Chart.js or similar config
    color_scheme = Column(JSON)  # Color palette for visualizations
    layout_config = Column(JSON)  # Layout settings
    
    # Data transformation
    data_transform = Column(JSON)  # How to transform API response for display
    template = Column(Text)  # Template for custom visualizations
    
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AIModelConfiguration(Base):
    """AI Model configuration per use case"""
    __tablename__ = "ai_model_configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    config_id = Column(String(100), unique=True, index=True, nullable=False)
    use_case_id = Column(String(100), ForeignKey("use_cases.use_case_id"), nullable=False)
    
    # Model Selection
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False)  # 'classification', 'regression', 'nlp', 'vision', 'forecasting'
    model_provider = Column(String(50))  # 'custom', 'openai', 'anthropic', 'huggingface', 'local'
    model_version = Column(String(50))
    model_endpoint = Column(String(500))
    
    # Configuration
    parameters = Column(JSON)  # Model hyperparameters
    input_schema = Column(JSON)  # Expected input format
    output_schema = Column(JSON)  # Expected output format
    
    # Training Configuration
    training_enabled = Column(Boolean, default=False)
    training_data_source = Column(String(200))
    training_parameters = Column(JSON)
    
    # Testing & Validation
    test_enabled = Column(Boolean, default=False)
    test_dataset_path = Column(String(500))
    test_thresholds = Column(JSON)  # Performance thresholds
    
    # Deployment
    is_active = Column(Boolean, default=False)
    deployment_environment = Column(String(50))  # 'dev', 'staging', 'prod'
    
    # Monitoring
    monitoring_enabled = Column(Boolean, default=False)
    alert_thresholds = Column(JSON)
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ContentAuditLog(Base):
    """Audit log for content changes"""
    __tablename__ = "content_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(100), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # 'create', 'update', 'delete', 'publish', 'unpublish'
    changed_fields = Column(JSON)  # Fields that changed
    old_values = Column(JSON)  # Previous values
    new_values = Column(JSON)  # New values
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    change_reason = Column(Text)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

