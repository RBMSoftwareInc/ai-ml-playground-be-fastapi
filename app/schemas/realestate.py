"""
Real Estate Industry Schemas
Request/Response models for Real Estate AI endpoints
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== PROPERTY VALUATION ====================

class PropertyData(BaseModel):
    """Property data for valuation"""
    address: str
    square_feet: int
    bedrooms: int
    bathrooms: int
    year_built: int
    property_type: str
    zip_code: str


class PropertyValuationRequest(BaseModel):
    """Property valuation request"""
    property_data: PropertyData


class ComparableProperty(BaseModel):
    """Comparable property"""
    address: str
    price: float
    similarity: float


class ValueDriver(BaseModel):
    """Value driver factor"""
    factor: str
    impact: float
    direction: str  # 'positive', 'negative', 'neutral'


class PropertyValuationResponse(BaseModel):
    """Property valuation response"""
    success: bool = True
    estimated_value_low: float
    estimated_value_high: float
    estimated_value_mid: float
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    valuation_flag: str = Field(..., description="'undervalued', 'fair_value', 'overpriced'")
    top_drivers: List[ValueDriver]
    comparables: List[ComparableProperty]
    metadata: Optional[Dict[str, Any]] = None


# ==================== MARKET TREND ANALYSIS ====================

class MarketTrendRequest(BaseModel):
    """Market trend analysis request"""
    location: str
    time_horizon_months: int = Field(6, ge=1, le=24)


class ForecastMonth(BaseModel):
    """Monthly forecast data"""
    month: int
    price_change_pct: float
    confidence_high: float
    confidence_low: float


class KeyIndicator(BaseModel):
    """Key market indicator"""
    indicator: str
    trend: str  # 'up', 'down', 'stable'
    impact: str  # 'high', 'medium', 'low'


class MarketTrendResponse(BaseModel):
    """Market trend analysis response"""
    success: bool = True
    market_pulse: str = Field(..., description="'cooling', 'stable', 'heating'")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    forecast_months: List[ForecastMonth]
    regime: str
    key_indicators: List[KeyIndicator]
    metadata: Optional[Dict[str, Any]] = None


# ==================== INVESTMENT OPPORTUNITY SCORING ====================

class PropertyInput(BaseModel):
    """Property input for scoring"""
    id: int
    address: str
    price: float
    type: str


class InvestmentScoringRequest(BaseModel):
    """Investment opportunity scoring request"""
    properties: List[PropertyInput]


class ScoredProperty(BaseModel):
    """Scored property result"""
    property_id: int
    opportunity_score: float = Field(..., ge=0.0, le=100.0)
    risk_adjusted_roi: float
    investment_profile: str = Field(..., description="'safe', 'balanced', 'aggressive'")
    yield_pct: float = Field(..., alias="yield", description="Annual yield percentage")
    appreciation_potential: float
    liquidity_score: float = Field(..., ge=0.0, le=1.0)
    risk_exposure: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    
    class Config:
        populate_by_name = True


class InvestmentScoringResponse(BaseModel):
    """Investment opportunity scoring response"""
    success: bool = True
    scored_properties: List[ScoredProperty]
    metadata: Optional[Dict[str, Any]] = None


# ==================== LEAD SCORING ====================

class LeadInput(BaseModel):
    """Lead input for scoring"""
    id: int
    name: str
    type: str  # 'Buyer' or 'Seller'
    inquiries: int
    budget: float
    engagement: str  # 'high', 'medium', 'low'


class LeadScoringRequest(BaseModel):
    """Lead scoring request"""
    leads: List[LeadInput]


class LeadFactor(BaseModel):
    """Lead scoring factor"""
    factor: str
    impact: float
    direction: str  # 'positive', 'negative', 'neutral'


class ScoredLead(BaseModel):
    """Scored lead result"""
    lead_id: int
    conversion_probability: float = Field(..., ge=0.0, le=1.0)
    priority: str = Field(..., description="'call_now', 'nurture', 'ignore'")
    intent_score: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    factors: List[LeadFactor]


class LeadScoringResponse(BaseModel):
    """Lead scoring response"""
    success: bool = True
    scored_leads: List[ScoredLead]
    metadata: Optional[Dict[str, Any]] = None


# ==================== PROJECT RISK ASSESSMENT ====================

class ProjectData(BaseModel):
    """Project data for risk assessment"""
    project_name: str
    budget: float
    timeline_months: int
    contractor_history_score: float = Field(..., ge=0.0, le=1.0)
    complexity: str = Field(..., description="'low', 'medium', 'high'")


class ProjectRiskRequest(BaseModel):
    """Project risk assessment request"""
    project_data: ProjectData


class ProjectRisk(BaseModel):
    """Project risk detail"""
    category: str  # 'Cost', 'Time', 'Quality'
    risk_name: str
    probability: float = Field(..., ge=0.0, le=1.0)
    impact: str  # 'high', 'medium', 'low'
    description: str
    mitigation: str


class ProjectRiskResponse(BaseModel):
    """Project risk assessment response"""
    success: bool = True
    overall_risk_level: str = Field(..., description="'low', 'medium', 'high'")
    risk_scores: Dict[str, float]  # cost_risk, time_risk, quality_risk
    top_risks: List[ProjectRisk]
    early_warnings: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


# ==================== SMART BUILDING ANALYTICS ====================

class BuildingData(BaseModel):
    """Building data for analytics"""
    building_name: str
    square_feet: int
    age_years: int
    occupancy_rate: float = Field(..., ge=0.0, le=1.0)


class SmartBuildingRequest(BaseModel):
    """Smart building analytics request"""
    building_data: BuildingData


class CostLeakageIndicator(BaseModel):
    """Cost leakage indicator"""
    category: str  # 'HVAC', 'Lighting', 'Water'
    estimated_loss: float
    severity: str  # 'high', 'medium', 'low'


class MaintenanceRecommendation(BaseModel):
    """Maintenance recommendation"""
    priority: str  # 'high', 'medium', 'low'
    system: str
    issue: str
    cost: float
    urgency: str
    description: str


class SmartBuildingResponse(BaseModel):
    """Smart building analytics response"""
    success: bool = True
    building_health_score: float = Field(..., ge=0.0, le=1.0)
    cost_leakage_indicators: List[CostLeakageIndicator]
    maintenance_recommendations: List[MaintenanceRecommendation]
    energy_optimization_potential: float = Field(..., ge=0.0, le=1.0)
    predictive_insights: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None
