"""
Intelligence Content Store Models
Central intelligence layer that powers all industries, use cases, explanations, and conversations
Replaces static text with DB-driven, dynamic intelligence content
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ContentCategory(str, enum.Enum):
    """Categories of intelligence content"""
    INDUSTRY_KNOWLEDGE = "industry_knowledge"
    WORKFLOW_COMPARISON = "workflow_comparison"  # Conventional vs AI
    DECISION_EXPLANATION = "decision_explanation"
    RISK_DISCLAIMER = "risk_disclaimer"
    ANALOGY = "analogy"  # For laypersons
    CONFIDENCE_LANGUAGE = "confidence_language"
    TOOLTIP = "tooltip"
    CONVERSATIONAL_RESPONSE = "conversational_response"
    TRANSFORMATION_STEP = "transformation_step"  # For Category 2
    MODEL_LIMITATION = "model_limitation"  # For Category 8


class ConfidenceLevel(str, enum.Enum):
    """Confidence levels for intelligence content"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


class IntelligenceContent(Base):
    """
    Central Intelligence Content Store
    Stores all dynamic content that replaces static UI text
    """
    __tablename__ = "intelligence_content"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content identification
    content_key = Column(String(255), nullable=False, index=True)  # Unique identifier (e.g., "fintech.credit_risk.decision_explanation.high_risk")
    category = Column(Enum(ContentCategory), nullable=False, index=True)
    
    # Context for content retrieval
    industry_id = Column(String(100), nullable=True, index=True)  # Optional: specific industry
    use_case_id = Column(String(100), nullable=True, index=True)  # Optional: specific use case
    context_tags = Column(JSON)  # Additional context tags for semantic matching
    
    # Content data
    title = Column(String(500), nullable=True)  # Short title/heading
    content_text = Column(Text, nullable=False)  # Main content (can be markdown)
    structured_data = Column(JSON)  # For structured content (e.g., workflow steps, comparison data)
    
    # Intelligence metadata
    confidence_level = Column(Enum(ConfidenceLevel), nullable=True, index=True)
    data_freshness_days = Column(Integer, nullable=True)  # How fresh the underlying data is
    model_agreement_score = Column(Float, nullable=True)  # Agreement between multiple models (0.0-1.0)
    
    # Usage context
    display_priority = Column(Integer, default=100)  # Higher = more important (for ordering)
    applicable_scenarios = Column(JSON)  # Scenarios where this content applies
    conditional_logic = Column(JSON)  # Conditions for when to show this content
    
    # Language and personalization
    audience_level = Column(String(50), default="general")  # 'layperson', 'general', 'technical', 'expert'
    tone = Column(String(50), default="professional")  # 'professional', 'conversational', 'formal'
    
    # Versioning and lifecycle
    version = Column(String(50), default="1.0.0")
    is_active = Column(Boolean, default=True, index=True)
    is_deprecated = Column(Boolean, default=False)
    
    # Relationships
    related_content_ids = Column(JSON)  # IDs of related intelligence content
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)  # Track usage
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Embedding for semantic search (optional, for future AI-powered retrieval)
    embedding = Column(JSON)
    embedding_model = Column(String(100))


class IntelligenceConversation(Base):
    """
    Stores conversation fragments for contextual navigation (Category 6)
    """
    __tablename__ = "intelligence_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Session identification
    session_id = Column(String(255), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # Context
    current_screen = Column(String(255), nullable=True)  # Current page/component
    industry_id = Column(String(100), nullable=True)
    use_case_id = Column(String(100), nullable=True)
    
    # Conversation content
    question_intent = Column(String(255), nullable=True)  # Classified intent
    user_query = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    
    # Intelligence content used
    explanation_used = Column(JSON)  # Reference to IntelligenceContent used
    confidence_expressed = Column(Float, nullable=True)  # Confidence shown to user
    
    # Conversation metadata
    depth_level = Column(Integer, default=1)  # Explanation depth requested
    conversation_history_ids = Column(JSON)  # IDs of previous conversation fragments in this session
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WorkflowComparison(Base):
    """
    Stores Conventional vs AI workflow comparisons (Category 2)
    """
    __tablename__ = "workflow_comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identification
    comparison_key = Column(String(255), nullable=False, index=True)
    industry_id = Column(String(100), nullable=False, index=True)
    use_case_id = Column(String(100), nullable=True, index=True)
    
    # Workflow data
    conventional_steps = Column(JSON, nullable=False)  # [{step_name, description, time_hours, error_probability, human_dependencies}]
    ai_driven_steps = Column(JSON, nullable=False)  # [{step_name, description, time_seconds, confidence_score, learning_loop}]
    
    # Transformation metrics
    time_reduction_percent = Column(Float, nullable=True)
    error_reduction_percent = Column(Float, nullable=True)
    human_intervention_points = Column(JSON)  # Where humans intervene now vs before
    
    # Visual configuration
    timeline_animation_config = Column(JSON)  # Animation settings for timeline slider
    
    # Metadata
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)


class ModelHonestyMetadata(Base):
    """
    Stores model honesty and trust information (Category 8)
    """
    __tablename__ = "model_honesty_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Model identification
    model_name = Column(String(255), nullable=False, index=True)
    use_case_id = Column(String(100), nullable=True, index=True)
    industry_id = Column(String(100), nullable=True, index=True)
    
    # Honesty metrics
    confidence_percent = Column(Float, nullable=True)  # Default confidence %
    data_coverage_percent = Column(Float, nullable=True)  # Data coverage %
    known_limitations = Column(JSON, nullable=False)  # [{limitation_text, severity, mitigation}]
    
    # What model does NOT know
    unknown_areas = Column(JSON)  # Areas the model explicitly doesn't handle
    
    # Uncertainty indicators
    uncertainty_factors = Column(JSON)  # Factors that increase uncertainty
    
    # Metadata
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

