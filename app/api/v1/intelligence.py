"""
Intelligence Content API Routes
API endpoints for the central Intelligence Content Store
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.intelligence_service import IntelligenceService
from app.schemas.intelligence import (
    IntelligenceContentResponse,
    ContentRequest,
    ExplanationRequest,
    WorkflowComparisonResponse,
    ModelHonestyResponse,
    ConversationRequest,
    ConversationHistoryResponse,
    ConfidenceLanguageRequest
)
from app.models.intelligence import ContentCategory, ConfidenceLevel

router = APIRouter(tags=["Intelligence"])


@router.get("/content", response_model=IntelligenceContentResponse)
async def get_intelligence_content(
    content_key: Optional[str] = Query(None, description="Specific content key to retrieve"),
    category: Optional[str] = Query(None, description="Content category filter"),
    industry_id: Optional[str] = Query(None, description="Industry ID filter"),
    use_case_id: Optional[str] = Query(None, description="Use case ID filter"),
    confidence_level: Optional[str] = Query(None, description="Confidence level filter"),
    audience_level: Optional[str] = Query(None, description="Audience level filter"),
    db: Session = Depends(get_db)
):
    """
    Retrieve intelligence content by key or context
    """
    try:
        service = IntelligenceService(db)
        
        category_enum = None
        if category:
            try:
                category_enum = ContentCategory(category)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        content = service.get_content(
            content_key=content_key,
            category=category_enum,
            industry_id=industry_id,
            use_case_id=use_case_id,
            confidence_level=confidence_level,
            audience_level=audience_level
        )
        
        if not content:
            raise HTTPException(status_code=404, detail="Intelligence content not found")
        
        return IntelligenceContentResponse.model_validate(content)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving intelligence content: {str(e)}")


@router.get("/content/list", response_model=List[IntelligenceContentResponse])
async def list_intelligence_content(
    category: Optional[str] = Query(None, description="Content category filter"),
    industry_id: Optional[str] = Query(None, description="Industry ID filter"),
    use_case_id: Optional[str] = Query(None, description="Use case ID filter"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    List multiple intelligence content items
    """
    try:
        service = IntelligenceService(db)
        
        category_enum = None
        if category:
            try:
                category_enum = ContentCategory(category)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        content_list = service.get_multiple_content(
            category=category_enum,
            industry_id=industry_id,
            use_case_id=use_case_id,
            limit=limit
        )
        
        return [IntelligenceContentResponse.model_validate(c) for c in content_list]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing intelligence content: {str(e)}")


@router.post("/explanation", response_model=IntelligenceContentResponse)
async def get_decision_explanation(
    request: ExplanationRequest,
    db: Session = Depends(get_db)
):
    """
    Get decision explanation content based on context and confidence score
    """
    try:
        service = IntelligenceService(db)
        
        content = service.get_explanation(
            context=request.context,
            industry_id=request.industry_id,
            use_case_id=request.use_case_id,
            confidence_score=request.confidence_score
        )
        
        if not content:
            raise HTTPException(status_code=404, detail="Explanation content not found")
        
        return IntelligenceContentResponse.model_validate(content)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving explanation: {str(e)}")


@router.get("/workflow-comparison", response_model=WorkflowComparisonResponse)
async def get_workflow_comparison(
    industry_id: str = Query(..., description="Industry ID"),
    use_case_id: Optional[str] = Query(None, description="Use case ID (optional)"),
    db: Session = Depends(get_db)
):
    """
    Get Conventional vs AI workflow comparison
    """
    try:
        service = IntelligenceService(db)
        
        comparison = service.get_workflow_comparison(
            industry_id=industry_id,
            use_case_id=use_case_id
        )
        
        if not comparison:
            raise HTTPException(status_code=404, detail="Workflow comparison not found")
        
        return WorkflowComparisonResponse.model_validate(comparison)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving workflow comparison: {str(e)}")


@router.get("/model-honesty", response_model=ModelHonestyResponse)
async def get_model_honesty(
    model_name: str = Query(..., description="Model name"),
    use_case_id: Optional[str] = Query(None, description="Use case ID (optional)"),
    industry_id: Optional[str] = Query(None, description="Industry ID (optional)"),
    db: Session = Depends(get_db)
):
    """
    Get model honesty metadata (confidence, data coverage, limitations)
    """
    try:
        service = IntelligenceService(db)
        
        honesty_metadata = service.get_model_honesty_metadata(
            model_name=model_name,
            use_case_id=use_case_id,
            industry_id=industry_id
        )
        
        if not honesty_metadata:
            raise HTTPException(status_code=404, detail="Model honesty metadata not found")
        
        return ModelHonestyResponse.model_validate(honesty_metadata)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving model honesty metadata: {str(e)}")


@router.post("/conversation", response_model=dict)
async def save_conversation(
    request: ConversationRequest,
    db: Session = Depends(get_db)
):
    """
    Save a conversation fragment for contextual navigation
    """
    try:
        service = IntelligenceService(db)
        
        conversation = service.save_conversation(
            session_id=request.session_id,
            user_query=request.user_query,
            ai_response=request.ai_response,
            current_screen=request.current_screen,
            industry_id=request.industry_id,
            use_case_id=request.use_case_id,
            question_intent=request.question_intent,
            explanation_used=request.explanation_used,
            confidence_expressed=request.confidence_expressed,
            depth_level=request.depth_level
        )
        
        return {"success": True, "conversation_id": conversation.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving conversation: {str(e)}")


@router.post("/conversation/generate", response_model=dict)
async def generate_conversation_response(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Generate a conversational AI response based on user query and context
    This endpoint uses the Intelligence Content Store to provide context-aware responses
    """
    try:
        service = IntelligenceService(db)
        user_query = request.get("user_query", "")
        context = request.get("context", {})
        
        # Get relevant intelligence content for context
        industry_id = context.get("industry_id")
        use_case_id = context.get("use_case_id")
        
        # Retrieve relevant content from Intelligence Store
        relevant_content = service.get_multiple_content(
            industry_id=industry_id,
            use_case_id=use_case_id,
            limit=5
        )
        
        # Generate response based on content (simplified - in production would use LLM)
        ai_response = "I understand. How can I help you?"
        confidence = 0.8
        
        if relevant_content:
            # Use first relevant content item to inform response
            first_content = relevant_content[0]
            ai_response = f"Based on the context, {first_content.content_text[:200]}... What would you like to know more about?"
            confidence = 0.85
        
        # Save conversation
        conversation = service.save_conversation(
            session_id=request.get("session_id"),
            user_query=user_query,
            ai_response=ai_response,
            current_screen=context.get("current_screen"),
            industry_id=industry_id,
            use_case_id=use_case_id,
            confidence_expressed=confidence
        )
        
        return {
            "success": True,
            "ai_response": ai_response,
            "confidence_expressed": confidence,
            "conversation_id": conversation.id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating conversation response: {str(e)}")


@router.get("/conversation/history", response_model=List[ConversationHistoryResponse])
async def get_conversation_history(
    session_id: str = Query(..., description="Session ID"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get conversation history for a session
    """
    try:
        service = IntelligenceService(db)
        
        history = service.get_conversation_history(
            session_id=session_id,
            limit=limit
        )
        
        # Return empty list if no history found
        if not history:
            return []
        
        # Convert to response models
        return [ConversationHistoryResponse.model_validate(c) for c in history]
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error retrieving conversation history: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/confidence-language", response_model=IntelligenceContentResponse)
async def get_confidence_language(
    request: ConfidenceLanguageRequest,
    db: Session = Depends(get_db)
):
    """
    Get human-readable confidence language based on confidence score
    """
    try:
        service = IntelligenceService(db)
        
        content = service.get_confidence_language(
            confidence_score=request.confidence_score,
            industry_id=request.industry_id
        )
        
        if not content:
            raise HTTPException(status_code=404, detail="Confidence language not found")
        
        return IntelligenceContentResponse.model_validate(content)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving confidence language: {str(e)}")
