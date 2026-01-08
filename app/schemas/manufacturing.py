"""
Manufacturing Industry Schemas
Request/Response models for Manufacturing AI endpoints
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== PREDICTIVE MAINTENANCE ====================

class MachineInput(BaseModel):
    """Machine data for maintenance prediction"""
    id: int
    name: str
    hours_operation: int
    last_maintenance: str


class PredictiveMaintenanceRequest(BaseModel):
    """Predictive maintenance request"""
    sub_industry: str = Field(..., description="'automotive', 'electronics', 'process'")
    machines: List[MachineInput]


class FailureIndicator(BaseModel):
    """Failure indicator"""
    indicator: str
    severity: str  # 'high', 'medium', 'low'
    contribution: float


class MachineHealth(BaseModel):
    """Machine health prediction"""
    machine_id: int
    failure_probability_7d: float = Field(..., ge=0.0, le=1.0)
    failure_probability_30d: float = Field(..., ge=0.0, le=1.0)
    failure_probability_90d: float = Field(..., ge=0.0, le=1.0)
    remaining_useful_life_days: int
    top_indicators: List[FailureIndicator]
    risk_level: str = Field(..., description="'low', 'medium', 'high'")


class PredictiveMaintenanceResponse(BaseModel):
    """Predictive maintenance response"""
    success: bool = True
    machine_health: List[MachineHealth]
    metadata: Optional[Dict[str, Any]] = None


# ==================== ENERGY OPTIMIZATION ====================

class EnergyOptimizationRequest(BaseModel):
    """Energy optimization request"""
    sub_industry: str = Field(..., description="'automotive', 'electronics', 'process'")


class CostLeakageIndicator(BaseModel):
    """Cost leakage indicator"""
    zone: str
    waste_kwh: float
    severity: str  # 'high', 'medium', 'low'
    recommendation: str


class EnergyRecommendation(BaseModel):
    """Energy optimization recommendation"""
    action: str
    savings_kwh: float
    priority: str  # 'high', 'medium', 'low'


class EnergyOptimizationResponse(BaseModel):
    """Energy optimization response"""
    success: bool = True
    total_consumption: float
    potential_savings: float
    savings_percentage: float = Field(..., ge=0.0, le=1.0)
    cost_leakage_indicators: List[CostLeakageIndicator]
    recommendations: List[EnergyRecommendation]
    metadata: Optional[Dict[str, Any]] = None


# ==================== VISUAL QUALITY INSPECTION ====================

class QualityVisionRequest(BaseModel):
    """Visual quality inspection request"""
    sub_industry: str = Field(..., description="'automotive', 'electronics', 'process'")


class DefectDetail(BaseModel):
    """Defect detail"""
    id: int
    type: str
    severity: str  # 'high', 'medium', 'low'
    confidence: float = Field(..., ge=0.0, le=1.0)
    bounding_box: List[int]
    explanation: str


class InspectionSummary(BaseModel):
    """Inspection summary"""
    passed: int
    rejected: int
    review: int


class QualityVisionResponse(BaseModel):
    """Visual quality inspection response"""
    success: bool = True
    total_inspected: int
    defect_count: int
    defect_rate: float = Field(..., ge=0.0, le=1.0)
    defects: List[DefectDetail]
    summary: InspectionSummary
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


# ==================== PROCESS OPTIMIZATION ====================

class ProcessParameters(BaseModel):
    """Process parameters"""
    temperature: float
    pressure: float
    speed: float


class ProcessOptimizationRequest(BaseModel):
    """Process optimization request"""
    sub_industry: str = Field(..., description="'automotive', 'electronics', 'process'")
    parameters: ProcessParameters


class ParameterImpact(BaseModel):
    """Parameter impact analysis"""
    parameter: str
    impact: float = Field(..., ge=0.0, le=1.0)
    optimal_value: float
    safe_range: List[float]
    current_value: float


class ProcessRecommendation(BaseModel):
    """Process optimization recommendation"""
    parameter: str
    change: float
    direction: str  # 'increase', 'decrease'
    impact: str


class ProcessOptimizationResponse(BaseModel):
    """Process optimization response"""
    success: bool = True
    current_yield: float = Field(..., ge=0.0, le=1.0)
    optimal_yield: float = Field(..., ge=0.0, le=1.0)
    yield_improvement: float = Field(..., ge=0.0, le=1.0)
    parameter_impacts: List[ParameterImpact]
    recommendations: List[ProcessRecommendation]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


# ==================== DEMAND PLANNING ====================

class DemandPlanningRequest(BaseModel):
    """Demand planning request"""
    sub_industry: str = Field(..., description="'automotive', 'electronics', 'process'")
    time_horizon_weeks: int = Field(4, ge=1, le=52)


class ForecastWeek(BaseModel):
    """Weekly demand forecast"""
    week: int
    demand_low: float
    demand_mid: float
    demand_high: float
    confidence: float = Field(..., ge=0.0, le=1.0)


class DemandPlanningResponse(BaseModel):
    """Demand planning response"""
    success: bool = True
    forecast_weeks: List[ForecastWeek]
    conservative_plan: float
    aggressive_plan: float
    stockout_risk: float = Field(..., ge=0.0, le=1.0)
    overstock_risk: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None


# ==================== SUPPLY CHAIN OPTIMIZATION ====================

class SupplyOptimizationRequest(BaseModel):
    """Supply chain optimization request"""
    sub_industry: str = Field(..., description="'automotive', 'electronics', 'process'")


class SupplierInfo(BaseModel):
    """Supplier information"""
    id: int
    name: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    performance_score: float = Field(..., ge=0.0, le=1.0)
    location: str
    lead_time_days: int
    risk_level: str = Field(..., description="'low', 'medium', 'high'")


class BottleneckAlert(BaseModel):
    """Supply chain bottleneck"""
    component: str
    impact: str  # 'high', 'critical'
    supplier: str
    delay_risk: float = Field(..., ge=0.0, le=1.0)
    alternative_available: bool


class AlternativeSourcing(BaseModel):
    """Alternative sourcing option"""
    component: str
    current_supplier: str
    alternative: str
    lead_time_improvement: int  # days (negative = faster)
    cost_delta: float  # percentage change


class SupplyOptimizationResponse(BaseModel):
    """Supply chain optimization response"""
    success: bool = True
    suppliers: List[SupplierInfo]
    bottlenecks: List[BottleneckAlert]
    alternative_sourcing: List[AlternativeSourcing]
    overall_risk: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[Dict[str, Any]] = None
