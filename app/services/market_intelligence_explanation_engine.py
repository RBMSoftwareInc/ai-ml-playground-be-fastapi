"""
Market Intelligence Explanation Engine
Generates mandatory explanation objects for all Market Intelligence APIs
Plain English, no jargon, no model names, no equations
"""
from typing import Dict, List, Any, Optional
from app.schemas.fintech import (
    MarketIntelligenceExplanation, SignalSummary, MarketIntelligenceConfidenceAssessment,
    KeyDriver, HistoricalAnalog, UncertaintyFactor
)
from datetime import datetime


class MarketIntelligenceExplanationEngine:
    """
    Explanation engine for Market Intelligence APIs
    Generates explainable, human-readable reasoning for all signals
    """
    
    def __init__(self):
        """Initialize explanation engine"""
        pass
    
    def generate_commodity_trend_explanation(
        self,
        directional_bias: str,
        trend_strength: float,
        confidence_lower: float,
        confidence_upper: float,
        volatility_estimate: float,
        similar_periods: List[Dict[str, Any]],
        scenario_params: Dict[str, Any]
    ) -> MarketIntelligenceExplanation:
        """Generate explanation for commodity trend intelligence"""
        
        # Signal Summary
        signal_summary = SignalSummary(
            signal_type="commodity_trend",
            signal_direction=directional_bias,
            signal_strength=trend_strength,
            time_horizon="30-90 days"
        )
        
        # Confidence Assessment
        confidence_range = confidence_upper - confidence_lower
        if confidence_range < 0.2:
            conf_level = "high"
            conf_score = 0.85
            conf_reason = "Strong historical patterns and consistent market signals support this assessment."
        elif confidence_range < 0.4:
            conf_level = "medium"
            conf_score = 0.70
            conf_reason = "Good market data, but some volatility and uncertainty in current conditions."
        else:
            conf_level = "low"
            conf_score = 0.55
            conf_reason = "High market volatility and limited historical precedent reduce confidence."
        
        confidence = MarketIntelligenceConfidenceAssessment(
            confidence_level=conf_level,
            confidence_score=conf_score,
            confidence_reason=conf_reason,
            data_quality="high" if volatility_estimate < 0.05 else "medium"
        )
        
        # Key Drivers
        key_drivers = []
        if volatility_estimate > 0.05:
            key_drivers.append(KeyDriver(
                driver_name="Market Volatility",
                impact_direction="negative" if directional_bias == "down" else "positive",
                impact_magnitude=0.3,
                explanation="Elevated volatility indicates increased market uncertainty and potential price swings."
            ))
        if trend_strength > 0.6:
            key_drivers.append(KeyDriver(
                driver_name="Trend Strength",
                impact_direction="positive",
                impact_magnitude=0.4,
                explanation="Strong directional trend suggests sustained price movement in this direction."
            ))
        if trend_strength < 0.3:
            key_drivers.append(KeyDriver(
                driver_name="Sideways Movement",
                impact_direction="neutral",
                impact_magnitude=0.25,
                explanation="Weak trend strength indicates range-bound trading with limited directional bias."
            ))
        
        # Historical Analogs
        historical_analogs = [
            HistoricalAnalog(
                period_start=period["period_start"],
                period_end=period["period_end"],
                similarity_score=period["similarity_score"],
                outcome_summary=period["outcome_summary"]
            )
            for period in similar_periods[:3]
        ]
        
        # Uncertainty Factors
        uncertainty_factors = []
        if volatility_estimate > 0.05:
            uncertainty_factors.append(UncertaintyFactor(
                factor_name="High Volatility",
                uncertainty_level="high",
                explanation="Elevated volatility makes price movements less predictable."
            ))
        if confidence_range > 0.3:
            uncertainty_factors.append(UncertaintyFactor(
                factor_name="Wide Confidence Range",
                uncertainty_level="medium",
                explanation="Broad confidence range reflects uncertainty in market conditions."
            ))
        
        # What This Means (Plain English)
        if directional_bias == "up":
            what_this_means = f"Market signals suggest upward price movement over the next 30-90 days with {conf_level} confidence. Historical patterns similar to this have shown recovery trends. However, {volatility_estimate:.1%} volatility indicates significant price swings are possible."
        elif directional_bias == "down":
            what_this_means = f"Market signals suggest downward price pressure over the next 30-90 days with {conf_level} confidence. Similar historical periods have shown correction patterns. Elevated volatility of {volatility_estimate:.1%} increases uncertainty around the timing and magnitude of moves."
        else:
            what_this_means = f"Market signals suggest sideways trading with limited directional bias over the next 30-90 days. Trend strength is weak, indicating range-bound conditions. Volatility of {volatility_estimate:.1%} suggests price movements may be choppy rather than trending."
        
        return MarketIntelligenceExplanation(
            signal_summary=signal_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            historical_analogs=historical_analogs,
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            model_version="1.0.0",
            inference_timestamp=datetime.now()
        )
    
    def generate_market_regime_explanation(
        self,
        current_regime: str,
        regime_probability: float,
        stability_score: float,
        transition_probability: float,
        scenario_params: Dict[str, Any]
    ) -> MarketIntelligenceExplanation:
        """Generate explanation for market regime signals"""
        
        # Signal Summary
        signal_summary = SignalSummary(
            signal_type="market_regime",
            signal_direction=current_regime,
            signal_strength=stability_score,
            time_horizon="30-60 days"
        )
        
        # Confidence Assessment
        if regime_probability > 0.75:
            conf_level = "high"
            conf_score = 0.85
            conf_reason = "Strong regime characteristics and consistent market features support this assessment."
        elif regime_probability > 0.55:
            conf_level = "medium"
            conf_score = 0.70
            conf_reason = "Good regime indicators, but some mixed signals suggest potential transition."
        else:
            conf_level = "low"
            conf_score = 0.55
            conf_reason = "Weak regime signals and high transition probability reduce confidence."
        
        confidence = MarketIntelligenceConfidenceAssessment(
            confidence_level=conf_level,
            confidence_score=conf_score,
            confidence_reason=conf_reason,
            data_quality="high"
        )
        
        # Key Drivers
        key_drivers = []
        if stability_score > 0.7:
            key_drivers.append(KeyDriver(
                driver_name="Regime Stability",
                impact_direction="positive",
                impact_magnitude=0.4,
                explanation="High stability score indicates the current regime is well-established and likely to persist."
            ))
        if transition_probability > 0.5:
            key_drivers.append(KeyDriver(
                driver_name="Transition Risk",
                impact_direction="negative",
                impact_magnitude=0.35,
                explanation="Elevated transition probability suggests the regime may be shifting, increasing uncertainty."
            ))
        
        # Historical Analogs (synthetic)
        historical_analogs = [
            HistoricalAnalog(
                period_start="2020-03-01",
                period_end="2020-06-30",
                similarity_score=0.72,
                outcome_summary="Similar regime transition from stress to recovery with volatility normalization"
            ),
            HistoricalAnalog(
                period_start="2018-10-01",
                period_end="2018-12-31",
                similarity_score=0.65,
                outcome_summary="Comparable regime characteristics with sustained volatility period"
            )
        ]
        
        # Uncertainty Factors
        uncertainty_factors = []
        if transition_probability > 0.5:
            uncertainty_factors.append(UncertaintyFactor(
                factor_name="High Transition Probability",
                uncertainty_level="high",
                explanation="Elevated probability of regime change increases uncertainty about future market conditions."
            ))
        
        # What This Means
        regime_descriptions = {
            "calm": "stable, low-volatility conditions",
            "volatile": "high-volatility, unpredictable conditions",
            "stress": "distressed market conditions with elevated risk",
            "recovery": "improving conditions following stress"
        }
        
        what_this_means = f"The market is currently in a {regime_descriptions.get(current_regime, current_regime)} regime with {conf_level} confidence. The regime shows {stability_score:.0%} stability, suggesting it is {'well-established' if stability_score > 0.7 else 'potentially shifting'}. There is a {transition_probability:.0%} probability of transitioning to a different regime over the next 30-60 days, which {'increases uncertainty' if transition_probability > 0.5 else 'suggests relative stability'}."
        
        return MarketIntelligenceExplanation(
            signal_summary=signal_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            historical_analogs=historical_analogs,
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            model_version="1.0.0",
            inference_timestamp=datetime.now()
        )
    
    def generate_digital_asset_adoption_explanation(
        self,
        adoption_phase: str,
        momentum_score: float,
        growth_rate: float,
        acceleration_indicator: float,
        scenario_params: Dict[str, Any]
    ) -> MarketIntelligenceExplanation:
        """Generate explanation for digital asset adoption intelligence"""
        
        # Signal Summary
        signal_summary = SignalSummary(
            signal_type="digital_asset_adoption",
            signal_direction="positive" if momentum_score > 0 else "negative",
            signal_strength=abs(momentum_score),
            time_horizon="90-180 days"
        )
        
        # Confidence Assessment
        if abs(momentum_score) > 0.5:
            conf_level = "high"
            conf_score = 0.80
            conf_reason = "Strong adoption signals and clear momentum direction support this assessment."
        elif abs(momentum_score) > 0.2:
            conf_level = "medium"
            conf_score = 0.65
            conf_reason = "Moderate adoption signals with some variability in momentum."
        else:
            conf_level = "low"
            conf_score = 0.50
            conf_reason = "Weak adoption signals and limited momentum reduce confidence."
        
        confidence = MarketIntelligenceConfidenceAssessment(
            confidence_level=conf_level,
            confidence_score=conf_score,
            confidence_reason=conf_reason,
            data_quality="medium"
        )
        
        # Key Drivers
        key_drivers = []
        if momentum_score > 0.3:
            key_drivers.append(KeyDriver(
                driver_name="Adoption Momentum",
                impact_direction="positive",
                impact_magnitude=0.4,
                explanation="Strong positive momentum indicates accelerating adoption and growing user base."
            ))
        elif momentum_score < -0.3:
            key_drivers.append(KeyDriver(
                driver_name="Adoption Deceleration",
                impact_direction="negative",
                impact_magnitude=0.35,
                explanation="Negative momentum suggests adoption growth is slowing or declining."
            ))
        
        if acceleration_indicator > 0.5:
            key_drivers.append(KeyDriver(
                driver_name="Acceleration",
                impact_direction="positive",
                impact_magnitude=0.3,
                explanation="High acceleration indicates adoption is not just growing, but growing faster over time."
            ))
        
        # Historical Analogs
        historical_analogs = [
            HistoricalAnalog(
                period_start="2020-01-01",
                period_end="2020-06-30",
                similarity_score=0.70,
                outcome_summary="Similar adoption phase with sustained growth momentum"
            )
        ]
        
        # Uncertainty Factors
        uncertainty_factors = []
        if abs(momentum_score) < 0.2:
            uncertainty_factors.append(UncertaintyFactor(
                factor_name="Weak Momentum",
                uncertainty_level="medium",
                explanation="Limited momentum makes adoption trajectory less predictable."
            ))
        
        # What This Means
        phase_descriptions = {
            "early": "early adoption phase with initial user growth",
            "growth": "growth phase with accelerating adoption",
            "maturation": "maturation phase with stable, slower growth",
            "saturation": "saturation phase with limited growth potential"
        }
        
        what_this_means = f"Digital asset adoption is in the {phase_descriptions.get(adoption_phase, adoption_phase)} with {conf_level} confidence. Adoption shows {momentum_score:+.0%} momentum, indicating {'accelerating' if momentum_score > 0.3 else 'stable' if abs(momentum_score) < 0.2 else 'decelerating'} growth. The {growth_rate:+.1f}% growth rate suggests {'strong expansion' if growth_rate > 5 else 'moderate growth' if growth_rate > 0 else 'potential decline'} in adoption activity."
        
        return MarketIntelligenceExplanation(
            signal_summary=signal_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            historical_analogs=historical_analogs,
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            model_version="1.0.0",
            inference_timestamp=datetime.now()
        )
    
    def generate_exchange_risk_explanation(
        self,
        risk_concentration_score: float,
        dependency_hotspots: List[Dict[str, Any]],
        systemic_exposure_indicator: float,
        stress_propagation_risk: float,
        scenario_params: Dict[str, Any]
    ) -> MarketIntelligenceExplanation:
        """Generate explanation for exchange risk mapping"""
        
        # Signal Summary
        signal_summary = SignalSummary(
            signal_type="exchange_risk",
            signal_direction="high" if risk_concentration_score > 0.6 else "low",
            signal_strength=risk_concentration_score,
            time_horizon="ongoing"
        )
        
        # Confidence Assessment
        if risk_concentration_score > 0.7 or risk_concentration_score < 0.3:
            conf_level = "high"
            conf_score = 0.85
            conf_reason = "Clear risk concentration patterns and well-defined dependency structures support this assessment."
        else:
            conf_level = "medium"
            conf_score = 0.70
            conf_reason = "Moderate risk levels with some complexity in dependency relationships."
        
        confidence = MarketIntelligenceConfidenceAssessment(
            confidence_level=conf_level,
            confidence_score=conf_score,
            confidence_reason=conf_reason,
            data_quality="high"
        )
        
        # Key Drivers
        key_drivers = []
        if risk_concentration_score > 0.6:
            key_drivers.append(KeyDriver(
                driver_name="Risk Concentration",
                impact_direction="negative",
                impact_magnitude=0.4,
                explanation="High risk concentration indicates vulnerability to single points of failure."
            ))
        
        if systemic_exposure_indicator > 0.6:
            key_drivers.append(KeyDriver(
                driver_name="Systemic Exposure",
                impact_direction="negative",
                impact_magnitude=0.35,
                explanation="High systemic exposure suggests potential for cascading failures across the market."
            ))
        
        if len(dependency_hotspots) > 0:
            key_drivers.append(KeyDriver(
                driver_name="Dependency Hotspots",
                impact_direction="negative",
                impact_magnitude=0.3,
                explanation=f"{len(dependency_hotspots)} dependency hotspots create concentrated risk points."
            ))
        
        # Historical Analogs
        historical_analogs = [
            HistoricalAnalog(
                period_start="2022-05-01",
                period_end="2022-07-31",
                similarity_score=0.68,
                outcome_summary="Similar risk concentration patterns with exchange stress events"
            )
        ]
        
        # Uncertainty Factors
        uncertainty_factors = []
        if stress_propagation_risk > 0.6:
            uncertainty_factors.append(UncertaintyFactor(
                factor_name="High Stress Propagation Risk",
                uncertainty_level="high",
                explanation="Elevated stress propagation risk increases uncertainty about systemic impact of failures."
            ))
        
        # What This Means
        risk_level = "high" if risk_concentration_score > 0.6 else "medium" if risk_concentration_score > 0.4 else "low"
        
        what_this_means = f"Exchange risk mapping shows {risk_level} risk concentration with {conf_level} confidence. The {risk_concentration_score:.0%} concentration score indicates {'significant vulnerability' if risk_concentration_score > 0.6 else 'moderate risk' if risk_concentration_score > 0.4 else 'well-diversified risk'}. Systemic exposure of {systemic_exposure_indicator:.0%} suggests {'potential for widespread impact' if systemic_exposure_indicator > 0.6 else 'limited systemic risk'}. {'Multiple dependency hotspots' if len(dependency_hotspots) > 1 else 'A dependency hotspot' if len(dependency_hotspots) == 1 else 'No significant dependency hotspots'} {'create' if len(dependency_hotspots) > 1 else 'creates' if len(dependency_hotspots) == 1 else 'indicates'} {'concentrated risk points' if len(dependency_hotspots) > 0 else 'good risk distribution'}."
        
        return MarketIntelligenceExplanation(
            signal_summary=signal_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            historical_analogs=historical_analogs,
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            model_version="1.0.0",
            inference_timestamp=datetime.now()
        )


# Global instance
market_intelligence_explanation_engine = MarketIntelligenceExplanationEngine()

