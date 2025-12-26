"""
Travel AI Schemas
Decision-intelligence schemas for travel operations, pricing, and personalization
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== EXPLANATION CONTRACT (MANDATORY) ====================

class TravelKeyDriver(BaseModel):
    """Key driver of the travel decision"""
    driver_name: str = Field(..., description="Name of the driver")
    impact_direction: str = Field(..., description="'positive', 'negative', or 'neutral'")
    impact_magnitude: float = Field(..., ge=0.0, le=1.0, description="Magnitude of impact")
    explanation: str = Field(..., description="Why this driver matters")


class TravelUncertaintyFactor(BaseModel):
    """Factor contributing to uncertainty"""
    factor_name: str = Field(..., description="Name of the uncertainty factor")
    uncertainty_level: str = Field(..., description="'low', 'medium', or 'high'")
    explanation: str = Field(..., description="Why this creates uncertainty")


class TravelConfidenceAssessment(BaseModel):
    """Confidence assessment for travel decisions"""
    confidence_level: str = Field(..., description="'low', 'medium', or 'high'")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Numeric confidence score")
    confidence_reason: str = Field(..., description="Why confidence is at this level")
    data_quality: str = Field(..., description="Quality of underlying data")


class TravelExplanation(BaseModel):
    """
    MANDATORY explanation contract for all Travel AI APIs
    Plain English, no jargon, no model names, no equations
    """
    decision_summary: str = Field(..., description="Plain English decision summary")
    confidence: TravelConfidenceAssessment = Field(..., description="Confidence assessment")
    key_drivers: List[TravelKeyDriver] = Field(..., description="Top 3-5 key drivers")
    uncertainty_factors: List[TravelUncertaintyFactor] = Field(..., description="Factors contributing to uncertainty")
    what_this_means: str = Field(..., description="Plain English explanation of what this means")
    time_savings: Optional[str] = Field(None, description="Time savings vs conventional approach")
    model_version: str = Field(..., description="Model version used")
    inference_timestamp: datetime = Field(default_factory=datetime.now)


# ==================== USE CASE 1: DYNAMIC PRICING ENGINE ====================

class DynamicPricingRequest(BaseModel):
    """Dynamic pricing engine request"""
    property_id: str = Field(..., description="Property identifier (hotel, flight route, etc.)")
    target_date: datetime = Field(..., description="Target travel/booking date")
    current_price: Optional[float] = Field(None, description="Current price")
    lead_time_days: Optional[int] = Field(None, description="Days until travel date")
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class DynamicPricingResponse(BaseModel):
    """Dynamic pricing engine response"""
    success: bool = True
    property_id: str
    recommendation_date: datetime = Field(default_factory=datetime.now)
    recommended_price_min: float = Field(..., ge=0.0)
    recommended_price_max: float = Field(..., ge=0.0)
    recommended_price_optimal: float = Field(..., ge=0.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    top_drivers: List[Dict[str, Any]] = Field(..., description="Top factors influencing price")
    demand_surge_indicator: float = Field(..., ge=0.0, le=1.0)
    seasonality_impact: float = Field(..., description="Seasonal adjustment factor")
    explanation: TravelExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== USE CASE 2: DEMAND FORECASTING ====================

class DemandForecastRequest(BaseModel):
    """Demand forecasting request"""
    property_id: str = Field(..., description="Property identifier")
    forecast_horizon_days: Optional[int] = Field(90, ge=7, le=365, description="Days ahead to forecast")
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class DemandForecastResponse(BaseModel):
    """Demand forecasting response"""
    success: bool = True
    property_id: str
    forecast_date: datetime = Field(default_factory=datetime.now)
    forecasted_demand: float = Field(..., ge=0.0)
    confidence_band_lower: float = Field(..., ge=0.0)
    confidence_band_upper: float = Field(..., ge=0.0)
    trend_direction: str = Field(..., description="'increasing', 'decreasing', or 'stable'")
    risk_zones: List[Dict[str, Any]] = Field(..., description="High/medium/low risk periods")
    holiday_impact: float = Field(..., description="Holiday impact on demand")
    explanation: TravelExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== USE CASE 3: PERSONALIZED RECOMMENDATIONS ====================

class PersonalizedRecommendationRequest(BaseModel):
    """Personalized recommendation request"""
    traveler_id: Optional[str] = Field(None, description="Traveler ID (if None, uses request data)")
    destination: Optional[str] = Field(None, description="Destination preference")
    travel_date: Optional[datetime] = Field(None, description="Preferred travel date")
    duration_days: Optional[int] = Field(None, description="Trip duration in days")
    budget: Optional[float] = Field(None, description="Budget constraint")
    travel_style: Optional[str] = Field(None, description="Travel style preference")
    traveler_data: Optional[Dict[str, Any]] = Field(None, description="Traveler profile data if not in database")


class PersonalizedRecommendationResponse(BaseModel):
    """Personalized recommendation response"""
    success: bool = True
    traveler_id: str
    recommendation_date: datetime = Field(default_factory=datetime.now)
    recommended_items: List[Dict[str, Any]] = Field(..., description="Ranked list of recommendations")
    recommendation_reasons: List[Dict[str, Any]] = Field(..., description="Why each item was recommended")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    intent_match_score: float = Field(..., ge=0.0, le=1.0)
    explanation: TravelExplanation  # MANDATORY
    metadata: Optional[Dict[str, Any]] = None


# ==================== USE CASE 4: AI CONCIERGE ====================

class AIConciergeRequest(BaseModel):
    """AI Concierge request"""
    conversation_id: Optional[str] = Field(None, description="Conversation ID (if None, creates new)")
    traveler_id: str = Field(..., description="Traveler ID")
    message: str = Field(..., description="User message")
    travel_state: Optional[str] = Field(None, description="Current travel state")


class AIConciergeResponse(BaseModel):
    """AI Concierge response"""
    success: bool = True
    conversation_id: str
    traveler_id: str
    response_message: str = Field(..., description="AI response message")
    suggested_actions: List[Dict[str, Any]] = Field(..., description="AI-suggested next actions")
    escalation_required: bool = Field(..., description="Whether human escalation is needed")
    travel_state: str = Field(..., description="Detected or updated travel state")
    explanation: TravelExplanation  # MANDATORY
    metadata: Optional[Dict[str, Any]] = None


# ==================== USE CASE 5: ROUTE OPTIMIZATION ====================

class RouteOptimizationRequest(BaseModel):
    """Route optimization request"""
    route_id: Optional[str] = Field(None, description="Route ID (if None, uses origin/destination)")
    origin: str = Field(..., description="Origin location")
    destination: str = Field(..., description="Destination location")
    travel_date: Optional[datetime] = Field(None, description="Travel date")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Route constraints (max_cost, max_duration, etc.)")
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class RouteOptimizationResponse(BaseModel):
    """Route optimization response"""
    success: bool = True
    route_id: str
    optimization_date: datetime = Field(default_factory=datetime.now)
    optimal_route: List[Dict[str, Any]] = Field(..., description="Optimal route segments")
    total_distance_km: float = Field(..., ge=0.0)
    total_duration_minutes: float = Field(..., ge=0.0)
    total_cost: float = Field(..., ge=0.0)
    delay_risk_score: float = Field(..., ge=0.0, le=1.0)
    savings_estimate: float = Field(..., description="Savings vs baseline route")
    explanation: TravelExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== USE CASE 6: HOTEL MATCHING AI ====================

class HotelMatchingRequest(BaseModel):
    """Hotel matching request"""
    traveler_id: Optional[str] = Field(None, description="Traveler ID (if None, uses request data)")
    destination: str = Field(..., description="Destination location")
    check_in_date: datetime = Field(..., description="Check-in date")
    check_out_date: datetime = Field(..., description="Check-out date")
    budget: Optional[float] = Field(None, description="Budget constraint")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Hotel preferences")
    traveler_data: Optional[Dict[str, Any]] = Field(None, description="Traveler profile data if not in database")


class HotelMatchingResponse(BaseModel):
    """Hotel matching response"""
    success: bool = True
    traveler_id: str
    match_date: datetime = Field(default_factory=datetime.now)
    matched_hotels: List[Dict[str, Any]] = Field(..., description="Ranked list of matched hotels")
    match_scores: List[float] = Field(..., description="Similarity scores for each hotel")
    tradeoff_explanations: List[Dict[str, Any]] = Field(..., description="Tradeoffs for each match")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    intent_match_score: float = Field(..., ge=0.0, le=1.0)
    explanation: TravelExplanation  # MANDATORY
    metadata: Optional[Dict[str, Any]] = None

