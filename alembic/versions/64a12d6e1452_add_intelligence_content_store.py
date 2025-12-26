"""Add Intelligence Content Store

Revision ID: 64a12d6e1452
Revises: 2a5ceea0faab
Create Date: 2025-01-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '64a12d6e1452'
down_revision: Union[str, None] = '2a5ceea0faab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE contentcategory AS ENUM ('industry_knowledge', 'workflow_comparison', 'decision_explanation', 'risk_disclaimer', 'analogy', 'confidence_language', 'tooltip', 'conversational_response', 'transformation_step', 'model_limitation')")
    op.execute("CREATE TYPE confidencelevel AS ENUM ('high', 'medium', 'low', 'uncertain')")
    
    # Intelligence Content table
    op.create_table('intelligence_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content_key', sa.String(length=255), nullable=False),
    sa.Column('category', postgresql.ENUM('industry_knowledge', 'workflow_comparison', 'decision_explanation', 'risk_disclaimer', 'analogy', 'confidence_language', 'tooltip', 'conversational_response', 'transformation_step', 'model_limitation', name='contentcategory', create_type=False), nullable=False),
    sa.Column('industry_id', sa.String(length=100), nullable=True),
    sa.Column('use_case_id', sa.String(length=100), nullable=True),
    sa.Column('context_tags', sa.JSON(), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('content_text', sa.Text(), nullable=False),
    sa.Column('structured_data', sa.JSON(), nullable=True),
    sa.Column('confidence_level', postgresql.ENUM('high', 'medium', 'low', 'uncertain', name='confidencelevel', create_type=False), nullable=True),
    sa.Column('data_freshness_days', sa.Integer(), nullable=True),
    sa.Column('model_agreement_score', sa.Float(), nullable=True),
    sa.Column('display_priority', sa.Integer(), nullable=True),
    sa.Column('applicable_scenarios', sa.JSON(), nullable=True),
    sa.Column('conditional_logic', sa.JSON(), nullable=True),
    sa.Column('audience_level', sa.String(length=50), nullable=True),
    sa.Column('tone', sa.String(length=50), nullable=True),
    sa.Column('version', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_deprecated', sa.Boolean(), nullable=True),
    sa.Column('related_content_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('embedding', sa.JSON(), nullable=True),
    sa.Column('embedding_model', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_intelligence_content_id'), 'intelligence_content', ['id'], unique=False)
    op.create_index(op.f('ix_intelligence_content_content_key'), 'intelligence_content', ['content_key'], unique=False)
    op.create_index('ix_intelligence_content_category', 'intelligence_content', ['category'], unique=False)
    op.create_index('ix_intelligence_content_industry_id', 'intelligence_content', ['industry_id'], unique=False)
    op.create_index('ix_intelligence_content_use_case_id', 'intelligence_content', ['use_case_id'], unique=False)
    op.create_index('ix_intelligence_content_confidence_level', 'intelligence_content', ['confidence_level'], unique=False)
    op.create_index('ix_intelligence_content_is_active', 'intelligence_content', ['is_active'], unique=False)
    
    # Intelligence Conversation table
    op.create_table('intelligence_conversations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('current_screen', sa.String(length=255), nullable=True),
    sa.Column('industry_id', sa.String(length=100), nullable=True),
    sa.Column('use_case_id', sa.String(length=100), nullable=True),
    sa.Column('question_intent', sa.String(length=255), nullable=True),
    sa.Column('user_query', sa.Text(), nullable=False),
    sa.Column('ai_response', sa.Text(), nullable=False),
    sa.Column('explanation_used', sa.JSON(), nullable=True),
    sa.Column('confidence_expressed', sa.Float(), nullable=True),
    sa.Column('depth_level', sa.Integer(), nullable=True),
    sa.Column('conversation_history_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_intelligence_conversations_id'), 'intelligence_conversations', ['id'], unique=False)
    op.create_index('ix_intelligence_conversations_session_id', 'intelligence_conversations', ['session_id'], unique=False)
    op.create_index('ix_intelligence_conversations_user_id', 'intelligence_conversations', ['user_id'], unique=False)
    
    # Workflow Comparison table
    op.create_table('workflow_comparisons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comparison_key', sa.String(length=255), nullable=False),
    sa.Column('industry_id', sa.String(length=100), nullable=False),
    sa.Column('use_case_id', sa.String(length=100), nullable=True),
    sa.Column('conventional_steps', sa.JSON(), nullable=False),
    sa.Column('ai_driven_steps', sa.JSON(), nullable=False),
    sa.Column('time_reduction_percent', sa.Float(), nullable=True),
    sa.Column('error_reduction_percent', sa.Float(), nullable=True),
    sa.Column('human_intervention_points', sa.JSON(), nullable=True),
    sa.Column('timeline_animation_config', sa.JSON(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_comparisons_id'), 'workflow_comparisons', ['id'], unique=False)
    op.create_index('ix_workflow_comparisons_comparison_key', 'workflow_comparisons', ['comparison_key'], unique=False)
    op.create_index('ix_workflow_comparisons_industry_id', 'workflow_comparisons', ['industry_id'], unique=False)
    op.create_index('ix_workflow_comparisons_use_case_id', 'workflow_comparisons', ['use_case_id'], unique=False)
    op.create_index('ix_workflow_comparisons_is_active', 'workflow_comparisons', ['is_active'], unique=False)
    
    # Model Honesty Metadata table
    op.create_table('model_honesty_metadata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_name', sa.String(length=255), nullable=False),
    sa.Column('use_case_id', sa.String(length=100), nullable=True),
    sa.Column('industry_id', sa.String(length=100), nullable=True),
    sa.Column('confidence_percent', sa.Float(), nullable=True),
    sa.Column('data_coverage_percent', sa.Float(), nullable=True),
    sa.Column('known_limitations', sa.JSON(), nullable=False),
    sa.Column('unknown_areas', sa.JSON(), nullable=True),
    sa.Column('uncertainty_factors', sa.JSON(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_honesty_metadata_id'), 'model_honesty_metadata', ['id'], unique=False)
    op.create_index('ix_model_honesty_metadata_model_name', 'model_honesty_metadata', ['model_name'], unique=False)
    op.create_index('ix_model_honesty_metadata_use_case_id', 'model_honesty_metadata', ['use_case_id'], unique=False)
    op.create_index('ix_model_honesty_metadata_industry_id', 'model_honesty_metadata', ['industry_id'], unique=False)
    op.create_index('ix_model_honesty_metadata_is_active', 'model_honesty_metadata', ['is_active'], unique=False)


def downgrade() -> None:
    # Drop tables
    op.drop_index('ix_model_honesty_metadata_is_active', table_name='model_honesty_metadata')
    op.drop_index('ix_model_honesty_metadata_industry_id', table_name='model_honesty_metadata')
    op.drop_index('ix_model_honesty_metadata_use_case_id', table_name='model_honesty_metadata')
    op.drop_index('ix_model_honesty_metadata_model_name', table_name='model_honesty_metadata')
    op.drop_index(op.f('ix_model_honesty_metadata_id'), table_name='model_honesty_metadata')
    op.drop_table('model_honesty_metadata')
    
    op.drop_index('ix_workflow_comparisons_is_active', table_name='workflow_comparisons')
    op.drop_index('ix_workflow_comparisons_use_case_id', table_name='workflow_comparisons')
    op.drop_index('ix_workflow_comparisons_industry_id', table_name='workflow_comparisons')
    op.drop_index('ix_workflow_comparisons_comparison_key', table_name='workflow_comparisons')
    op.drop_index(op.f('ix_workflow_comparisons_id'), table_name='workflow_comparisons')
    op.drop_table('workflow_comparisons')
    
    op.drop_index('ix_intelligence_conversations_user_id', table_name='intelligence_conversations')
    op.drop_index('ix_intelligence_conversations_session_id', table_name='intelligence_conversations')
    op.drop_index(op.f('ix_intelligence_conversations_id'), table_name='intelligence_conversations')
    op.drop_table('intelligence_conversations')
    
    op.drop_index('ix_intelligence_content_is_active', table_name='intelligence_content')
    op.drop_index('ix_intelligence_content_confidence_level', table_name='intelligence_content')
    op.drop_index('ix_intelligence_content_use_case_id', table_name='intelligence_content')
    op.drop_index('ix_intelligence_content_industry_id', table_name='intelligence_content')
    op.drop_index('ix_intelligence_content_category', table_name='intelligence_content')
    op.drop_index(op.f('ix_intelligence_content_content_key'), table_name='intelligence_content')
    op.drop_index(op.f('ix_intelligence_content_id'), table_name='intelligence_content')
    op.drop_table('intelligence_content')
    
    # Drop enum types
    op.execute("DROP TYPE IF EXISTS confidencelevel")
    op.execute("DROP TYPE IF EXISTS contentcategory")

