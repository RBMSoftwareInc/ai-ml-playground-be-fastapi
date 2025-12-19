"""
Common schemas used across all endpoints
"""
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime


class StandardResponse(BaseModel):
    """Standard API response format"""
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None
    confidence: Optional[float] = None
    recommendations: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = False
    error: str
    code: str

