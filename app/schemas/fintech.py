"""
Fintech Industry Schemas
Explanation contracts and request/response models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# ==================== EXPLANATION CONTRACT (MANDATORY) ====================
# Decision Walkthrough Tab Structure - 7 Sections

class InfluencingFactor(BaseModel):
    """Top influencing factor for Decision Walkthrough"""
    factor_name: str = Field(..., description="Name of the factor")
    influence_direction: str = Field(..., description="'increase' or 'decrease'")
    short_reason: str = Field(..., description="Brief explanation of why this factor matters")


class ConfidenceAssessment(BaseModel):
    """Confidence assessment for Decision Walkthrough"""
    confidence_level: str = Field(..., description="'low', 'medium', or 'high'")
    confidence_reason: str = Field(..., description="Why confidence is at this level")
    known_limitations: str = Field(..., description="What limits confidence in this decision")


class HumanReviewGuidance(BaseModel):
    """Human review guidance for Decision Walkthrough"""
    review_recommended: bool = Field(..., description="Whether human review is recommended")
    review_reason: str = Field(..., description="Why review is or isn't recommended")


class ContributingFactor(BaseModel):
    """Top contributing factor to decision (legacy support)"""
    factor_name: str
    impact_score: float = Field(..., ge=0.0, le=1.0)
    direction: str = Field(..., description="'increases' or 'decreases' risk/score")
    explanation: str


class SensitivityAnalysis(BaseModel):
    """Sensitivity analysis for decision"""
    parameter: str
    baseline_value: Any
    sensitivity_range: Dict[str, Any]
    impact_description: str


class ScenarioImpact(BaseModel):
    """Impact of scenario on decision"""
    scenario_name: str
    scenario_adjustment: Dict[str, Any]
    decision_change: str
    confidence_impact: float


class ExplanationObject(BaseModel):
    """
    MANDATORY explanation contract for all Fintech APIs
    Every API response must include this explanation object
    Maps 1-to-1 with Decision Walkthrough Tab UI (7 sections)
    """
    # Section 1: What Question Was Answered?
    decision_objective: str = Field(..., description="Plain sentence describing what question was answered")
    
    # Section 2: What Information Was Considered
    information_categories: List[str] = Field(..., description="High-level categories of information used (4-5 items)")
    
    # Section 3: How the System Reached This Decision
    decision_flow: List[str] = Field(..., description="Ordered list of reasoning steps in plain language (4-5 steps)")
    
    # Section 4: What Influenced This Result the Most
    top_influencing_factors: List[InfluencingFactor] = Field(..., description="Ranked list of top 3-5 factors with explanations")
    
    # Section 5: Confidence & Reliability of This Decision
    confidence_assessment: ConfidenceAssessment = Field(..., description="Confidence level, reason, and limitations")
    
    # Section 6: What Would Change This Outcome?
    sensitivity_triggers: List[str] = Field(..., description="Conditions that would materially change the outcome (3 items)")
    
    # Section 7: Human Review Guidance
    human_review_guidance: HumanReviewGuidance = Field(..., description="Whether review is recommended and why")
    
    # Legacy fields (maintained for backward compatibility)
    decision_summary: str = Field(..., description="Human-readable decision summary")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in decision (0.0 to 1.0)")
    top_contributing_factors: List[ContributingFactor] = Field(..., description="Ranked list of top factors")
    sensitivity_analysis: Optional[List[SensitivityAnalysis]] = Field(None, description="Sensitivity to parameter changes")
    scenario_impact: Optional[ScenarioImpact] = Field(None, description="Impact of selected scenario")
    uncertainty_notes: Optional[str] = Field(None, description="Notes on uncertainty and limitations")
    human_review_recommended: bool = Field(..., description="Whether human review is recommended")
    model_version: str = Field(..., description="Model version used for inference")
    inference_timestamp: datetime = Field(default_factory=datetime.now)


# ==================== MODULE 1: CREDIT RISK ====================

class CreditRiskRequest(BaseModel):
    """Credit risk assessment request"""
    borrower_id: Optional[str] = None
    scenario: str = Field(..., description="Scenario name: 'stable_economy', 'rising_rates', 'economic_downturn', 'high_inflation'")
    borrower_data: Optional[Dict[str, Any]] = Field(None, description="Borrower profile data if not in database")


class CreditRiskResponse(BaseModel):
    """Credit risk assessment response"""
    success: bool = True
    borrower_id: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str = Field(..., description="'low', 'medium', 'high', 'very_high'")
    default_probability: float = Field(..., ge=0.0, le=1.0)
    loss_given_default_estimate: float = Field(..., ge=0.0, le=1.0)
    recommendation: str
    explanation: ExplanationObject  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== MODULE 2: FRAUD DETECTION ====================

class FraudDetectionRequest(BaseModel):
    """Fraud detection request"""
    transaction_id: Optional[str] = None
    scenario: str = Field(..., description="Scenario name: 'normal_behavior', 'velocity_spike', 'geo_shift', 'coordinated_fraud'")
    transaction_data: Dict[str, Any] = Field(..., description="Transaction event data")


class FraudDetectionResponse(BaseModel):
    """Fraud detection response"""
    success: bool = True
    transaction_id: str
    fraud_probability: float = Field(..., ge=0.0, le=1.0)
    fraud_flag: bool
    fraud_type: Optional[str] = Field(None, description="Type of fraud if detected")
    risk_level: str = Field(..., description="'low', 'medium', 'high', 'critical'")
    recommendation: str
    explanation: ExplanationObject  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== MODULE 3: KYC / AML ====================

class KYCRiskRequest(BaseModel):
    """KYC/AML risk assessment request"""
    customer_id: Optional[str] = None
    scenario: str = Field(..., description="Scenario name: 'low_risk_retail', 'high_risk_jurisdiction', 'pep_profile', 'networked_entity'")
    customer_data: Optional[Dict[str, Any]] = Field(None, description="Customer identity data if not in database")


class KYCRiskResponse(BaseModel):
    """KYC/AML risk assessment response"""
    success: bool = True
    customer_id: str
    aml_risk_score: float = Field(..., ge=0.0, le=1.0)
    aml_risk_level: str = Field(..., description="'low', 'medium', 'high', 'very_high'")
    escalation_required: bool
    kyc_status: str = Field(..., description="'approved', 'pending_review', 'rejected', 'escalated'")
    recommendation: str
    explanation: ExplanationObject  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== MODULE 4: MARKET SIGNAL INTELLIGENCE ====================

class MarketSignalRequest(BaseModel):
    """Market signal intelligence request"""
    market_id: str
    scenario: str = Field(..., description="Scenario name: 'calm_market', 'news_uncertainty', 'liquidity_stress', 'macro_shock'")
    time_horizon_days: Optional[int] = Field(30, ge=1, le=365)


class MarketSignalResponse(BaseModel):
    """Market signal intelligence response"""
    success: bool = True
    market_id: str
    market_stress_state: str = Field(..., description="'calm', 'stressed', 'volatile'")
    stress_score: float = Field(..., ge=0.0, le=1.0)
    sentiment_index: float = Field(..., ge=-1.0, le=1.0)
    volatility_forecast: float = Field(..., ge=0.0)
    recommendation: str
    explanation: ExplanationObject  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== MODULE 5: MARKET REGIME SIMULATION ====================

class RegimeSimulationRequest(BaseModel):
    """Market regime simulation request"""
    market_id: str
    scenario: str = Field(..., description="Scenario name: 'volatility_expansion', 'correlation_breakdown', 'liquidity_freeze'")
    simulation_horizon_days: int = Field(30, ge=1, le=365)
    stress_level: Optional[float] = Field(None, ge=0.0, le=1.0)


class RegimeSimulationResponse(BaseModel):
    """Market regime simulation response"""
    success: bool = True
    market_id: str
    current_regime: str = Field(..., description="Current regime label")
    regime_confidence: float = Field(..., ge=0.0, le=1.0)
    projected_regime: str = Field(..., description="Projected regime")
    transition_probability: float = Field(..., ge=0.0, le=1.0)
    stress_indicators: Dict[str, float]
    recommendation: str
    explanation: ExplanationObject  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# ==================== MARKET & DIGITAL ASSET INTELLIGENCE (FINTECH) ====================

class HistoricalAnalog(BaseModel):
    """Historical period similar to current conditions"""
    period_start: str = Field(..., description="Start date of historical period")
    period_end: str = Field(..., description="End date of historical period")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity to current conditions")
    outcome_summary: str = Field(..., description="What happened during this period")


class KeyDriver(BaseModel):
    """Key driver of the signal"""
    driver_name: str = Field(..., description="Name of the driver")
    impact_direction: str = Field(..., description="'positive', 'negative', or 'neutral'")
    impact_magnitude: float = Field(..., ge=0.0, le=1.0, description="Magnitude of impact")
    explanation: str = Field(..., description="Why this driver matters")


class UncertaintyFactor(BaseModel):
    """Factor contributing to uncertainty"""
    factor_name: str = Field(..., description="Name of the uncertainty factor")
    uncertainty_level: str = Field(..., description="'low', 'medium', or 'high'")
    explanation: str = Field(..., description="Why this creates uncertainty")


class SignalSummary(BaseModel):
    """Summary of the signal"""
    signal_type: str = Field(..., description="Type of signal")
    signal_direction: str = Field(..., description="Direction of signal")
    signal_strength: float = Field(..., ge=0.0, le=1.0, description="Strength of signal")
    time_horizon: str = Field(..., description="Relevant time horizon")


class MarketIntelligenceConfidenceAssessment(BaseModel):
    """Confidence assessment for market intelligence signals"""
    confidence_level: str = Field(..., description="'low', 'medium', or 'high'")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Numeric confidence score")
    confidence_reason: str = Field(..., description="Why confidence is at this level")
    data_quality: str = Field(..., description="Quality of underlying data")


class MarketIntelligenceExplanation(BaseModel):
    """
    MANDATORY explanation contract for Market & Digital Asset Intelligence APIs
    Plain English, no jargon, no model names, no equations
    """
    signal_summary: SignalSummary = Field(..., description="Summary of the signal")
    confidence: MarketIntelligenceConfidenceAssessment = Field(..., description="Confidence assessment")
    key_drivers: List[KeyDriver] = Field(..., description="Top 3-5 key drivers")
    historical_analogs: List[HistoricalAnalog] = Field(..., description="Top 3 historical similar periods")
    uncertainty_factors: List[UncertaintyFactor] = Field(..., description="Factors contributing to uncertainty")
    what_this_means: str = Field(..., description="Plain English explanation of what this means")
    model_version: str = Field(..., description="Model version used")
    inference_timestamp: datetime = Field(default_factory=datetime.now)


# Module 1: Commodity Trend Intelligence
class CommodityTrendRequest(BaseModel):
    """Commodity trend intelligence request"""
    asset_id: str = Field(..., description="Commodity asset ID (e.g., 'gold', 'silver', 'oil')")
    lookback_days: Optional[int] = Field(90, ge=30, le=365, description="Days of historical data to consider")
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class CommodityTrendResponse(BaseModel):
    """Commodity trend intelligence response"""
    success: bool = True
    asset_id: str
    signal_date: datetime = Field(default_factory=datetime.now)
    directional_bias: str = Field(..., description="'up', 'down', or 'sideways'")
    confidence_band_lower: float = Field(..., ge=0.0, le=1.0)
    confidence_band_upper: float = Field(..., ge=0.0, le=1.0)
    trend_strength: float = Field(..., ge=0.0, le=1.0)
    volatility_estimate: float = Field(..., ge=0.0)
    similar_periods: List[Dict[str, Any]] = Field(..., description="Top 3 historical analogs")
    explanation: MarketIntelligenceExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# Module 2: Market Regime Signals (additional to existing RegimeSimulation)
class MarketRegimeIntelligenceRequest(BaseModel):
    """Market regime intelligence request"""
    market_id: str = Field(..., description="Market identifier")
    lookback_days: Optional[int] = Field(90, ge=30, le=365)
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class MarketRegimeIntelligenceResponse(BaseModel):
    """Market regime intelligence response"""
    success: bool = True
    market_id: str
    signal_date: datetime = Field(default_factory=datetime.now)
    current_regime: str = Field(..., description="Current regime label")
    regime_probability: float = Field(..., ge=0.0, le=1.0)
    stability_score: float = Field(..., ge=0.0, le=1.0)
    transition_probability: float = Field(..., ge=0.0, le=1.0)
    transition_likelihoods: Dict[str, float] = Field(..., description="Probabilities to other regimes")
    explanation: MarketIntelligenceExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# Module 3: Digital Asset Adoption Intelligence
class DigitalAssetAdoptionRequest(BaseModel):
    """Digital asset adoption intelligence request"""
    country_code: Optional[str] = Field(None, description="Country code (if None, returns global/regional)")
    lookback_days: Optional[int] = Field(180, ge=30, le=730)
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class DigitalAssetAdoptionResponse(BaseModel):
    """Digital asset adoption intelligence response"""
    success: bool = True
    country_code: Optional[str]
    signal_date: datetime = Field(default_factory=datetime.now)
    adoption_phase: str = Field(..., description="'early', 'growth', 'maturation', or 'saturation'")
    momentum_score: float = Field(..., ge=-1.0, le=1.0)
    growth_rate: float = Field(..., description="Percentage growth rate")
    acceleration_indicator: float = Field(..., ge=-1.0, le=1.0)
    regional_rank: Optional[int] = Field(None, description="Rank among regions")
    explanation: MarketIntelligenceExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None


# Module 4: Exchange & Market Risk Mapping
class ExchangeRiskRequest(BaseModel):
    """Exchange risk mapping request"""
    exchange_id: Optional[str] = Field(None, description="Exchange ID (if None, returns aggregate market risk)")
    scenario: Optional[str] = Field("baseline", description="Scenario name for simulation")


class ExchangeRiskResponse(BaseModel):
    """Exchange risk mapping response"""
    success: bool = True
    exchange_id: Optional[str]
    signal_date: datetime = Field(default_factory=datetime.now)
    risk_concentration_score: float = Field(..., ge=0.0, le=1.0)
    dependency_hotspots: List[Dict[str, Any]] = Field(..., description="High-dependency relationships")
    systemic_exposure_indicator: float = Field(..., ge=0.0, le=1.0)
    stress_propagation_risk: float = Field(..., ge=0.0, le=1.0)
    explanation: MarketIntelligenceExplanation  # MANDATORY
    scenario_applied: str
    metadata: Optional[Dict[str, Any]] = None

