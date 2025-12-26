"""
Intelligence Content Service
Service layer for retrieving and managing intelligence content from the central store
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.intelligence import (
    IntelligenceContent, IntelligenceConversation, WorkflowComparison, 
    ModelHonestyMetadata, ContentCategory, ConfidenceLevel
)
from sqlalchemy import cast, String


class IntelligenceService:
    """Service for managing intelligence content"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_content(
        self,
        content_key: Optional[str] = None,
        category: Optional[ContentCategory] = None,
        industry_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        confidence_level: Optional[ConfidenceLevel] = None,
        audience_level: Optional[str] = None,
        context_tags: Optional[List[str]] = None
    ) -> Optional[IntelligenceContent]:
        """
        Retrieve intelligence content by key or context
        """
        query = self.db.query(IntelligenceContent).filter(
            IntelligenceContent.is_active == True,
            IntelligenceContent.is_deprecated == False
        )
        
        if content_key:
            query = query.filter(IntelligenceContent.content_key == content_key)
        
        if category:
            # Use enum value (string) for SQLAlchemy comparison
            # SQLAlchemy Enum columns need the string value, not the enum object
            category_value = category.value if hasattr(category, 'value') else str(category)
            query = query.filter(cast(IntelligenceContent.category, String) == category_value)
        
        if industry_id:
            query = query.filter(
                or_(
                    IntelligenceContent.industry_id == industry_id,
                    IntelligenceContent.industry_id.is_(None)  # Also get global content
                )
            )
        
        if use_case_id:
            query = query.filter(
                or_(
                    IntelligenceContent.use_case_id == use_case_id,
                    IntelligenceContent.use_case_id.is_(None)  # Also get industry-level content
                )
            )
        
        if confidence_level:
            query = query.filter(IntelligenceContent.confidence_level == confidence_level)
        
        if audience_level:
            query = query.filter(IntelligenceContent.audience_level == audience_level)
        
        # Order by priority and specificity (use_case > industry > global)
        query = query.order_by(
            IntelligenceContent.use_case_id.isnot(None).desc(),  # Prefer use_case specific
            IntelligenceContent.industry_id.isnot(None).desc(),  # Then industry specific
            IntelligenceContent.display_priority.desc(),
            IntelligenceContent.created_at.desc()
        )
        
        return query.first()
    
    def get_multiple_content(
        self,
        category: Optional[ContentCategory] = None,
        industry_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        limit: int = 10
    ) -> List[IntelligenceContent]:
        """
        Retrieve multiple intelligence content items
        """
        query = self.db.query(IntelligenceContent).filter(
            IntelligenceContent.is_active == True,
            IntelligenceContent.is_deprecated == False
        )
        
        if category:
            # Use enum value (string) for SQLAlchemy comparison
            # SQLAlchemy Enum columns need the string value, not the enum object
            category_value = category.value if hasattr(category, 'value') else str(category)
            query = query.filter(cast(IntelligenceContent.category, String) == category_value)
        
        if industry_id:
            query = query.filter(
                or_(
                    IntelligenceContent.industry_id == industry_id,
                    IntelligenceContent.industry_id.is_(None)
                )
            )
        
        if use_case_id:
            query = query.filter(
                or_(
                    IntelligenceContent.use_case_id == use_case_id,
                    IntelligenceContent.use_case_id.is_(None)
                )
            )
        
        query = query.order_by(
            IntelligenceContent.display_priority.desc(),
            IntelligenceContent.created_at.desc()
        ).limit(limit)
        
        return query.all()
    
    def get_explanation(
        self,
        context: str,
        industry_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> Optional[IntelligenceContent]:
        """
        Get decision explanation content based on context and confidence
        """
        # Determine confidence level from score
        confidence_level = None
        if confidence_score is not None:
            if confidence_score >= 0.8:
                confidence_level = ConfidenceLevel.HIGH
            elif confidence_score >= 0.6:
                confidence_level = ConfidenceLevel.MEDIUM
            elif confidence_score >= 0.4:
                confidence_level = ConfidenceLevel.LOW
            else:
                confidence_level = ConfidenceLevel.UNCERTAIN
        
        # Try to find specific explanation first
        content_key = f"{industry_id or 'global'}.{use_case_id or 'general'}.decision_explanation.{context}"
        content = self.get_content(
            content_key=content_key,
            category=ContentCategory.DECISION_EXPLANATION,
            industry_id=industry_id,
            use_case_id=use_case_id,
            confidence_level=confidence_level
        )
        
        # Fallback to generic explanation
        if not content:
            content = self.get_content(
                category=ContentCategory.DECISION_EXPLANATION,
                industry_id=industry_id,
                confidence_level=confidence_level
            )
        
        return content
    
    def get_workflow_comparison(
        self,
        industry_id: str,
        use_case_id: Optional[str] = None
    ) -> Optional[WorkflowComparison]:
        """
        Get conventional vs AI workflow comparison
        """
        query = self.db.query(WorkflowComparison).filter(
            WorkflowComparison.is_active == True,
            WorkflowComparison.industry_id == industry_id
        )
        
        if use_case_id:
            query = query.filter(WorkflowComparison.use_case_id == use_case_id)
        
        return query.order_by(WorkflowComparison.created_at.desc()).first()
    
    def get_model_honesty_metadata(
        self,
        model_name: str,
        use_case_id: Optional[str] = None,
        industry_id: Optional[str] = None
    ) -> Optional[ModelHonestyMetadata]:
        """
        Get model honesty and trust metadata
        """
        query = self.db.query(ModelHonestyMetadata).filter(
            ModelHonestyMetadata.is_active == True,
            ModelHonestyMetadata.model_name == model_name
        )
        
        if use_case_id:
            query = query.filter(ModelHonestyMetadata.use_case_id == use_case_id)
        
        if industry_id:
            query = query.filter(ModelHonestyMetadata.industry_id == industry_id)
        
        return query.order_by(ModelHonestyMetadata.created_at.desc()).first()
    
    def save_conversation(
        self,
        session_id: str,
        user_query: str,
        ai_response: str,
        current_screen: Optional[str] = None,
        industry_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        question_intent: Optional[str] = None,
        explanation_used: Optional[Dict] = None,
        confidence_expressed: Optional[float] = None,
        depth_level: int = 1,
        user_id: Optional[int] = None
    ) -> IntelligenceConversation:
        """
        Save a conversation fragment for contextual navigation
        """
        conversation = IntelligenceConversation(
            session_id=session_id,
            user_id=user_id,
            current_screen=current_screen,
            industry_id=industry_id,
            use_case_id=use_case_id,
            question_intent=question_intent,
            user_query=user_query,
            ai_response=ai_response,
            explanation_used=explanation_used,
            confidence_expressed=confidence_expressed,
            depth_level=depth_level
        )
        
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[IntelligenceConversation]:
        """
        Get conversation history for a session
        """
        return self.db.query(IntelligenceConversation).filter(
            IntelligenceConversation.session_id == session_id
        ).order_by(
            IntelligenceConversation.created_at.desc()
        ).limit(limit).all()
    
    def get_confidence_language(
        self,
        confidence_score: float,
        industry_id: Optional[str] = None
    ) -> Optional[IntelligenceContent]:
        """
        Get human-readable confidence language
        """
        confidence_level = None
        if confidence_score >= 0.8:
            confidence_level = ConfidenceLevel.HIGH
        elif confidence_score >= 0.6:
            confidence_level = ConfidenceLevel.MEDIUM
        elif confidence_score >= 0.4:
            confidence_level = ConfidenceLevel.LOW
        else:
            confidence_level = ConfidenceLevel.UNCERTAIN
        
        return self.get_content(
            category=ContentCategory.CONFIDENCE_LANGUAGE,
            industry_id=industry_id,
            confidence_level=confidence_level
        )

