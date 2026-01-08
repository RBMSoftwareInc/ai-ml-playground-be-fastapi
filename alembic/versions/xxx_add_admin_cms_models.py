"""add admin cms auth workflow models

Revision ID: add_admin_cms_auth
Revises: 64a12d6e1452
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'add_admin_cms_auth'
down_revision = '64a12d6e1452'  # Update this to the latest revision
branch_labels = None
depends_on = None


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database"""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade():
    # Auth & RBAC Tables First (needed for foreign keys)
    if not table_exists('roles'):
        op.create_table(
            'roles',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('role_name', sa.String(length=50), nullable=False),
            sa.Column('display_name', sa.String(length=100), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('is_system', sa.Boolean(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('role_name')
        )
        op.create_index(op.f('ix_roles_role_name'), 'roles', ['role_name'], unique=True)
        op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)

    if not table_exists('permissions'):
        op.create_table(
            'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('permission_name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('resource', sa.String(length=50), nullable=True),
        sa.Column('action', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('permission_name')
        )
        op.create_index(op.f('ix_permissions_permission_name'), 'permissions', ['permission_name'], unique=True)
        op.create_index(op.f('ix_permissions_id'), 'permissions', ['id'], unique=False)

    if not table_exists('user_roles'):
        op.create_table(
            'user_roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('assigned_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['assigned_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_user_roles_id'), 'user_roles', ['id'], unique=False)

    if not table_exists('role_permissions'):
        op.create_table(
            'role_permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_role_permissions_id'), 'role_permissions', ['id'], unique=False)

    if not table_exists('refresh_tokens'):
        op.create_table(
            'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
        )
        op.create_index(op.f('ix_refresh_tokens_token'), 'refresh_tokens', ['token'], unique=True)
        op.create_index(op.f('ix_refresh_tokens_id'), 'refresh_tokens', ['id'], unique=False)

    if not table_exists('login_attempts'):
        op.create_table(
            'login_attempts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=True),
        sa.Column('failure_reason', sa.String(length=100), nullable=True),
        sa.Column('attempted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_login_attempts_email'), 'login_attempts', ['email'], unique=False)
        op.create_index(op.f('ix_login_attempts_attempted_at'), 'login_attempts', ['attempted_at'], unique=False)

    # CMS Workflow Tables
    # Create enum type if it doesn't exist
    bind = op.get_bind()
    enum_exists = False
    try:
        result = bind.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'contentstatus'"))
        enum_exists = result.fetchone() is not None
    except:
        pass
    
    if not enum_exists:
        op.execute("CREATE TYPE contentstatus AS ENUM ('draft', 'pending_review', 'approved', 'published', 'rejected', 'archived')")
    
    if not table_exists('content_versions_new'):
        op.create_table(
            'content_versions_new',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('entity_type', sa.String(length=50), nullable=False),
            sa.Column('entity_id', sa.String(length=100), nullable=False),
            sa.Column('version_number', sa.Integer(), nullable=False),
            sa.Column('version_label', sa.String(length=50), nullable=True),
            sa.Column('content_snapshot', postgresql.JSON(astext_type=sa.Text()), nullable=False),
            sa.Column('status', postgresql.ENUM('draft', 'pending_review', 'approved', 'published', 'rejected', 'archived', name='contentstatus', create_type=False), nullable=False),
            sa.Column('is_published', sa.Boolean(), nullable=True),
            sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('published_by', sa.Integer(), nullable=True),
            sa.Column('change_summary', sa.Text(), nullable=True),
            sa.Column('created_by', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
            sa.ForeignKeyConstraint(['published_by'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_content_versions_new_entity_type'), 'content_versions_new', ['entity_type'], unique=False)
        op.create_index(op.f('ix_content_versions_new_entity_id'), 'content_versions_new', ['entity_id'], unique=False)
        op.create_index(op.f('ix_content_versions_new_status'), 'content_versions_new', ['status'], unique=False)
        op.create_index(op.f('ix_content_versions_new_is_published'), 'content_versions_new', ['is_published'], unique=False)
        op.create_index(op.f('ix_content_versions_new_created_at'), 'content_versions_new', ['created_at'], unique=False)

    if not table_exists('content_approvals'):
        op.create_table(
            'content_approvals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('version_id', sa.Integer(), nullable=False),
        sa.Column('approver_id', sa.Integer(), nullable=False),
        sa.Column('approver_role', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('approval_order', sa.Integer(), nullable=False),
        sa.Column('requested_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['version_id'], ['content_versions_new.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_content_approvals_id'), 'content_approvals', ['id'], unique=False)

    if not table_exists('workflow_definitions'):
        op.create_table(
            'workflow_definitions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workflow_name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('entity_type', sa.String(length=50), nullable=True),
        sa.Column('approval_steps', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('requires_all_approvers', sa.Boolean(), nullable=True),
        sa.Column('auto_publish_on_approval', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('workflow_name')
        )
        op.create_index(op.f('ix_workflow_definitions_id'), 'workflow_definitions', ['id'], unique=False)

    if not table_exists('content_schedules'):
        op.create_table(
            'content_schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=100), nullable=False),
        sa.Column('version_id', sa.Integer(), nullable=True),
        sa.Column('scheduled_publish_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('scheduled_unpublish_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('executed_by', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['executed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['version_id'], ['content_versions_new.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_content_schedules_scheduled_publish_at'), 'content_schedules', ['scheduled_publish_at'], unique=False)

    if not table_exists('cms_settings'):
        op.create_table(
            'cms_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setting_key', sa.String(length=100), nullable=False),
        sa.Column('setting_value', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('setting_type', sa.String(length=50), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('setting_key')
        )
        op.create_index(op.f('ix_cms_settings_setting_key'), 'cms_settings', ['setting_key'], unique=True)

    # Admin CMS Tables
    # Content Assets
    if not table_exists('content_assets'):
        op.create_table(
            'content_assets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.String(length=100), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=True),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('alt_text', sa.Text(), nullable=True),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('asset_id')
        )
        op.create_index(op.f('ix_content_assets_asset_id'), 'content_assets', ['asset_id'], unique=True)
        op.create_index(op.f('ix_content_assets_id'), 'content_assets', ['id'], unique=False)

    # Themes
    if not table_exists('themes'):
        op.create_table(
            'themes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('theme_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('scope', sa.String(length=50), nullable=False),
        sa.Column('scope_id', sa.String(length=100), nullable=True),
        sa.Column('primary_color', sa.String(length=20), nullable=True),
        sa.Column('secondary_color', sa.String(length=20), nullable=True),
        sa.Column('accent_color', sa.String(length=20), nullable=True),
        sa.Column('background_color', sa.String(length=20), nullable=True),
        sa.Column('text_color', sa.String(length=20), nullable=True),
        sa.Column('custom_colors', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('font_family', sa.String(length=100), nullable=True),
        sa.Column('font_sizes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('spacing_scale', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('border_radius', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('component_styles', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('animation_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('theme_id')
        )
        op.create_index(op.f('ix_themes_theme_id'), 'themes', ['theme_id'], unique=True)
        op.create_index(op.f('ix_themes_id'), 'themes', ['id'], unique=False)

    # Content Blocks
    if not table_exists('content_blocks'):
        op.create_table(
            'content_blocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('block_id', sa.String(length=100), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=100), nullable=False),
        sa.Column('block_type', sa.String(length=50), nullable=True),
        sa.Column('block_key', sa.String(length=100), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('raw_content', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('is_visible', sa.Boolean(), nullable=True),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('keywords', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('block_id')
        )
        op.create_index(op.f('ix_content_blocks_block_id'), 'content_blocks', ['block_id'], unique=True)
        op.create_index(op.f('ix_content_blocks_entity_id'), 'content_blocks', ['entity_id'], unique=False)
        op.create_index(op.f('ix_content_blocks_id'), 'content_blocks', ['id'], unique=False)

    # Action Definitions
    if not table_exists('action_definitions'):
        op.create_table(
            'action_definitions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('action_id', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=100), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('button_style', sa.String(length=50), nullable=True),
        sa.Column('button_size', sa.String(length=50), nullable=True),
        sa.Column('position', sa.String(length=50), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('visibility_conditions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('action_id')
        )
        op.create_index(op.f('ix_action_definitions_action_id'), 'action_definitions', ['action_id'], unique=True)
        op.create_index(op.f('ix_action_definitions_id'), 'action_definitions', ['id'], unique=False)

    # Output Themes
    if not table_exists('output_themes'):
        op.create_table(
            'output_themes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('theme_id', sa.String(length=100), nullable=False),
        sa.Column('use_case_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('visualization_type', sa.String(length=50), nullable=True),
        sa.Column('chart_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('color_scheme', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('layout_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('data_transform', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('template', sa.Text(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['use_case_id'], ['use_cases.use_case_id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('theme_id')
        )
        op.create_index(op.f('ix_output_themes_theme_id'), 'output_themes', ['theme_id'], unique=True)
        op.create_index(op.f('ix_output_themes_id'), 'output_themes', ['id'], unique=False)

    # AI Model Configurations
    if not table_exists('ai_model_configurations'):
        op.create_table(
            'ai_model_configurations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('config_id', sa.String(length=100), nullable=False),
        sa.Column('use_case_id', sa.String(length=100), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('model_type', sa.String(length=50), nullable=False),
        sa.Column('model_provider', sa.String(length=50), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('model_endpoint', sa.String(length=500), nullable=True),
        sa.Column('parameters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('input_schema', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('output_schema', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('training_enabled', sa.Boolean(), nullable=True),
        sa.Column('training_data_source', sa.String(length=200), nullable=True),
        sa.Column('training_parameters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('test_enabled', sa.Boolean(), nullable=True),
        sa.Column('test_dataset_path', sa.String(length=500), nullable=True),
        sa.Column('test_thresholds', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('deployment_environment', sa.String(length=50), nullable=True),
        sa.Column('monitoring_enabled', sa.Boolean(), nullable=True),
        sa.Column('alert_thresholds', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['use_case_id'], ['use_cases.use_case_id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('config_id')
        )
        op.create_index(op.f('ix_ai_model_configurations_config_id'), 'ai_model_configurations', ['config_id'], unique=True)
        op.create_index(op.f('ix_ai_model_configurations_id'), 'ai_model_configurations', ['id'], unique=False)

    # Content Audit Logs
    if not table_exists('content_audit_logs'):
        op.create_table(
            'content_audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('changed_fields', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('old_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('new_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('changed_by', sa.Integer(), nullable=True),
        sa.Column('change_reason', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_content_audit_logs_entity_id'), 'content_audit_logs', ['entity_id'], unique=False)
        op.create_index(op.f('ix_content_audit_logs_created_at'), 'content_audit_logs', ['created_at'], unique=False)


def downgrade():
    # Admin CMS Tables
    op.drop_index(op.f('ix_content_audit_logs_created_at'), table_name='content_audit_logs')
    op.drop_index(op.f('ix_content_audit_logs_entity_id'), table_name='content_audit_logs')
    op.drop_table('content_audit_logs')
    op.drop_index(op.f('ix_ai_model_configurations_id'), table_name='ai_model_configurations')
    op.drop_index(op.f('ix_ai_model_configurations_config_id'), table_name='ai_model_configurations')
    op.drop_table('ai_model_configurations')
    op.drop_index(op.f('ix_output_themes_id'), table_name='output_themes')
    op.drop_index(op.f('ix_output_themes_theme_id'), table_name='output_themes')
    op.drop_table('output_themes')
    op.drop_index(op.f('ix_action_definitions_id'), table_name='action_definitions')
    op.drop_index(op.f('ix_action_definitions_action_id'), table_name='action_definitions')
    op.drop_table('action_definitions')
    op.drop_index(op.f('ix_content_blocks_id'), table_name='content_blocks')
    op.drop_index(op.f('ix_content_blocks_entity_id'), table_name='content_blocks')
    op.drop_index(op.f('ix_content_blocks_block_id'), table_name='content_blocks')
    op.drop_table('content_blocks')
    op.drop_index(op.f('ix_themes_id'), table_name='themes')
    op.drop_index(op.f('ix_themes_theme_id'), table_name='themes')
    op.drop_table('themes')
    op.drop_index(op.f('ix_content_assets_id'), table_name='content_assets')
    op.drop_index(op.f('ix_content_assets_asset_id'), table_name='content_assets')
    op.drop_table('content_assets')
    
    # CMS Workflow Tables
    op.drop_index(op.f('ix_cms_settings_setting_key'), table_name='cms_settings')
    op.drop_table('cms_settings')
    op.drop_index(op.f('ix_content_schedules_scheduled_publish_at'), table_name='content_schedules')
    op.drop_table('content_schedules')
    op.drop_index(op.f('ix_workflow_definitions_id'), table_name='workflow_definitions')
    op.drop_table('workflow_definitions')
    op.drop_index(op.f('ix_content_approvals_id'), table_name='content_approvals')
    op.drop_table('content_approvals')
    op.drop_index(op.f('ix_content_versions_new_created_at'), table_name='content_versions_new')
    op.drop_index(op.f('ix_content_versions_new_is_published'), table_name='content_versions_new')
    op.drop_index(op.f('ix_content_versions_new_status'), table_name='content_versions_new')
    op.drop_index(op.f('ix_content_versions_new_entity_id'), table_name='content_versions_new')
    op.drop_index(op.f('ix_content_versions_new_entity_type'), table_name='content_versions_new')
    op.drop_table('content_versions_new')
    op.execute('DROP TYPE IF EXISTS contentstatus')
    
    # Auth Tables
    op.drop_index(op.f('ix_login_attempts_attempted_at'), table_name='login_attempts')
    op.drop_index(op.f('ix_login_attempts_email'), table_name='login_attempts')
    op.drop_table('login_attempts')
    op.drop_index(op.f('ix_refresh_tokens_id'), table_name='refresh_tokens')
    op.drop_index(op.f('ix_refresh_tokens_token'), table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
    op.drop_index(op.f('ix_role_permissions_id'), table_name='role_permissions')
    op.drop_table('role_permissions')
    op.drop_index(op.f('ix_user_roles_id'), table_name='user_roles')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_permissions_id'), table_name='permissions')
    op.drop_index(op.f('ix_permissions_permission_name'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_index(op.f('ix_roles_role_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_content_audit_logs_created_at'), table_name='content_audit_logs')
    op.drop_index(op.f('ix_content_audit_logs_entity_id'), table_name='content_audit_logs')
    op.drop_table('content_audit_logs')
    op.drop_index(op.f('ix_ai_model_configurations_id'), table_name='ai_model_configurations')
    op.drop_index(op.f('ix_ai_model_configurations_config_id'), table_name='ai_model_configurations')
    op.drop_table('ai_model_configurations')
    op.drop_index(op.f('ix_output_themes_id'), table_name='output_themes')
    op.drop_index(op.f('ix_output_themes_theme_id'), table_name='output_themes')
    op.drop_table('output_themes')
    op.drop_index(op.f('ix_action_definitions_id'), table_name='action_definitions')
    op.drop_index(op.f('ix_action_definitions_action_id'), table_name='action_definitions')
    op.drop_table('action_definitions')
    op.drop_index(op.f('ix_content_blocks_id'), table_name='content_blocks')
    op.drop_index(op.f('ix_content_blocks_entity_id'), table_name='content_blocks')
    op.drop_index(op.f('ix_content_blocks_block_id'), table_name='content_blocks')
    op.drop_table('content_blocks')
    op.drop_index(op.f('ix_themes_id'), table_name='themes')
    op.drop_index(op.f('ix_themes_theme_id'), table_name='themes')
    op.drop_table('themes')
    op.drop_index(op.f('ix_content_assets_id'), table_name='content_assets')
    op.drop_index(op.f('ix_content_assets_asset_id'), table_name='content_assets')
    op.drop_table('content_assets')

