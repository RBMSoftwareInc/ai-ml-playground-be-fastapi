"""
Intelligence Content Schemas
Pydantic models for intelligence content API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.intelligence import ContentCategory, ConfidenceLevel


class IntelligenceContentResponse(BaseModel):
    """Response model for intelligence content"""
    id: int
    content_key: str
    category: str
    industry_id: Optional[str] = None
    use_case_id: Optional[str] = None
    title: Optional[str] = None
    content_text: str
    structured_data: Optional[Dict[str, Any]] = None
    confidence_level: Optional[str] = None
    data_freshness_days: Optional[int] = None
    model_agreement_score: Optional[float] = None
    audience_level: str = "general"
    tone: str = "professional"
    related_content_ids: Optional[List[int]] = None
    
    class Config:
        from_attributes = True


class ContentRequest(BaseModel):
    """Request model for retrieving content"""
    content_key: Optional[str] = None
    category: Optional[str] = None
    industry_id: Optional[str] = None
    use_case_id: Optional[str] = None
    confidence_level: Optional[str] = None
    audience_level: Optional[str] = None
    context_tags: Optional[List[str]] = None


class ExplanationRequest(BaseModel):
    """Request model for getting decision explanations"""
    context: str = Field(..., description="Context of the decision (e.g., 'high_risk', 'approved')")
    industry_id: Optional[str] = None
    use_case_id: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")


class WorkflowComparisonResponse(BaseModel):
    """Response model for workflow comparison"""
    id: int
    comparison_key: str
    industry_id: str
    use_case_id: Optional[str] = None
    conventional_steps: List[Dict[str, Any]]
    ai_driven_steps: List[Dict[str, Any]]
    time_reduction_percent: Optional[float] = None
    error_reduction_percent: Optional[float] = None
    human_intervention_points: Optional[Dict[str, Any]] = None
    timeline_animation_config: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class ModelHonestyResponse(BaseModel):
    """Response model for model honesty metadata"""
    id: int
    model_name: str
    use_case_id: Optional[str] = None
    industry_id: Optional[str] = None
    confidence_percent: Optional[float] = None
    data_coverage_percent: Optional[float] = None
    known_limitations: List[Dict[str, Any]]
    unknown_areas: Optional[List[str]] = None
    uncertainty_factors: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class ConversationRequest(BaseModel):
    """Request model for saving conversations"""
    session_id: str
    user_query: str
    ai_response: str
    current_screen: Optional[str] = None
    industry_id: Optional[str] = None
    use_case_id: Optional[str] = None
    question_intent: Optional[str] = None
    explanation_used: Optional[Dict[str, Any]] = None
    confidence_expressed: Optional[float] = Field(None, ge=0.0, le=1.0)
    depth_level: int = Field(1, ge=1, le=5)


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history"""
    id: int
    session_id: str
    current_screen: Optional[str] = None
    industry_id: Optional[str] = None
    use_case_id: Optional[str] = None
    question_intent: Optional[str] = None
    user_query: str
    ai_response: str
    confidence_expressed: Optional[float] = None
    depth_level: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConfidenceLanguageRequest(BaseModel):
    """Request model for getting confidence language"""
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    industry_id: Optional[str] = None

