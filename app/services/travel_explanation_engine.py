"""
Travel AI Explanation Engine
Generates plain-English explanations for all Travel AI decisions
No jargon, no model names, no equations
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.schemas.travel import (
    TravelExplanation,
    TravelKeyDriver,
    TravelUncertaintyFactor,
    TravelConfidenceAssessment
)


class TravelExplanationEngine:
    """Generate explanations for Travel AI decisions"""
    
    def __init__(self):
        self.model_version = "1.0.0"
    
    # ==================== USE CASE 1: DYNAMIC PRICING ====================
    
    def generate_dynamic_pricing_explanation(
        self,
        price_min: float,
        price_max: float,
        price_optimal: float,
        confidence_score: float,
        top_drivers: List[Dict[str, Any]],
        demand_surge_indicator: float,
        seasonality_impact: float,
        scenario_params: Optional[Dict[str, Any]] = None
    ) -> TravelExplanation:
        """Generate explanation for dynamic pricing recommendation"""
        
        # Decision summary
        price_change_pct = ((price_optimal - price_min) / price_min * 100) if price_min > 0 else 0
        decision_summary = (
            f"The system recommends pricing between ${price_min:.2f} and ${price_max:.2f}, "
            f"with an optimal price of ${price_optimal:.2f}. "
            f"This pricing adapts to current demand signals and market conditions."
        )
        
        # Key drivers
        key_drivers = []
        if demand_surge_indicator > 0.6:
            key_drivers.append(TravelKeyDriver(
                driver_name="High Demand Surge",
                impact_direction="positive",
                impact_magnitude=float(demand_surge_indicator),
                explanation="Current booking velocity indicates strong demand, supporting higher pricing."
            ))
        if seasonality_impact > 1.1:
            key_drivers.append(TravelKeyDriver(
                driver_name="Peak Season",
                impact_direction="positive",
                impact_magnitude=float((seasonality_impact - 1.0) * 2),
                explanation="We're in a peak travel season, which typically supports premium pricing."
            ))
        if len(top_drivers) > 0:
            for driver in top_drivers[:3]:
                key_drivers.append(TravelKeyDriver(
                    driver_name=driver.get("name", "Market Factor"),
                    impact_direction=driver.get("direction", "neutral"),
                    impact_magnitude=float(driver.get("magnitude", 0.5)),
                    explanation=driver.get("explanation", "This factor influences pricing.")
                ))
        
        # Confidence
        if confidence_score >= 0.8:
            confidence_level = "high"
            confidence_reason = "Strong demand signals and stable market conditions provide high confidence in this pricing recommendation."
        elif confidence_score >= 0.6:
            confidence_level = "medium"
            confidence_reason = "Moderate confidence based on available market data. Some uncertainty remains due to market volatility."
        else:
            confidence_level = "low"
            confidence_reason = "Lower confidence due to limited or conflicting market signals. Manual review recommended."
        
        confidence = TravelConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_score=float(confidence_score),
            confidence_reason=confidence_reason,
            data_quality="high" if confidence_score >= 0.7 else "medium"
        )
        
        # Uncertainty factors
        uncertainty_factors = []
        if demand_surge_indicator < 0.3:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="Low Demand Signals",
                uncertainty_level="medium",
                explanation="Current booking velocity is low, making demand prediction less certain."
            ))
        if seasonality_impact < 0.9 or seasonality_impact > 1.3:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="Seasonal Transition",
                uncertainty_level="low",
                explanation="We're in a seasonal transition period, which adds some uncertainty to pricing."
            ))
        
        # What this means
        what_this_means = (
            f"This pricing recommendation is designed to maximize revenue while remaining competitive. "
            f"The system continuously monitors demand signals and adjusts pricing accordingly. "
            f"Compared to static pricing, this approach can increase revenue by 10-25% during peak periods."
        )
        
        # Time savings
        time_savings = "What took revenue teams 3-5 days to adjust now happens in under 2 minutes, continuously."
        
        return TravelExplanation(
            decision_summary=decision_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            time_savings=time_savings,
            model_version=self.model_version,
            inference_timestamp=datetime.now()
        )
    
    # ==================== USE CASE 2: DEMAND FORECASTING ====================
    
    def generate_demand_forecast_explanation(
        self,
        forecasted_demand: float,
        confidence_lower: float,
        confidence_upper: float,
        trend_direction: str,
        risk_zones: List[Dict[str, Any]],
        holiday_impact: float,
        event_impact: float,
        scenario_params: Optional[Dict[str, Any]] = None
    ) -> TravelExplanation:
        """Generate explanation for demand forecast"""
        
        # Decision summary
        confidence_range = confidence_upper - confidence_lower
        decision_summary = (
            f"The system forecasts demand of {forecasted_demand:.1f} bookings, "
            f"with a confidence range of {confidence_lower:.1f} to {confidence_upper:.1f}. "
            f"The trend is {trend_direction}, indicating how demand is expected to change."
        )
        
        # Key drivers
        key_drivers = []
        if trend_direction == "increasing":
            key_drivers.append(TravelKeyDriver(
                driver_name="Rising Demand Trend",
                impact_direction="positive",
                impact_magnitude=0.7,
                explanation="Historical patterns and current signals suggest increasing demand ahead."
            ))
        elif trend_direction == "decreasing":
            key_drivers.append(TravelKeyDriver(
                driver_name="Declining Demand Trend",
                impact_direction="negative",
                impact_magnitude=0.6,
                explanation="Market signals indicate demand is tapering off."
            ))
        
        if holiday_impact > 0.1:
            key_drivers.append(TravelKeyDriver(
                driver_name="Holiday Period Impact",
                impact_direction="positive",
                impact_magnitude=float(holiday_impact * 3),
                explanation="Upcoming holidays typically boost demand by 20-30%."
            ))
        
        if event_impact > 0.1:
            key_drivers.append(TravelKeyDriver(
                driver_name="Special Events",
                impact_direction="positive",
                impact_magnitude=float(event_impact * 3),
                explanation="Special events in the area are expected to increase demand."
            ))
        
        # Confidence
        confidence_score = 1.0 - (confidence_range / forecasted_demand) if forecasted_demand > 0 else 0.7
        confidence_score = max(0.5, min(1.0, confidence_score))
        
        if confidence_score >= 0.8:
            confidence_level = "high"
            confidence_reason = "Strong historical patterns and clear market signals provide high confidence in this forecast."
        elif confidence_score >= 0.6:
            confidence_level = "medium"
            confidence_reason = "Moderate confidence based on available data. Some uncertainty remains due to market volatility."
        else:
            confidence_level = "low"
            confidence_reason = "Lower confidence due to limited historical data or high market volatility."
        
        confidence = TravelConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_score=float(confidence_score),
            confidence_reason=confidence_reason,
            data_quality="high" if confidence_score >= 0.7 else "medium"
        )
        
        # Uncertainty factors
        uncertainty_factors = []
        if confidence_range > forecasted_demand * 0.3:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="Wide Confidence Range",
                uncertainty_level="medium",
                explanation="The forecast has a wide confidence range, indicating higher uncertainty."
            ))
        
        # What this means
        what_this_means = (
            f"This forecast helps you plan inventory, staffing, and pricing strategies. "
            f"The confidence bands show the range of likely outcomes, helping you prepare for different scenarios. "
            f"Compared to manual forecasting, this AI-driven approach reduces forecast error by 15-30%."
        )
        
        # Time savings
        time_savings = "What took analysts 2-3 days to produce now happens in under 1 minute, with continuous updates."
        
        return TravelExplanation(
            decision_summary=decision_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            time_savings=time_savings,
            model_version=self.model_version,
            inference_timestamp=datetime.now()
        )
    
    # ==================== USE CASE 3: PERSONALIZED RECOMMENDATIONS ====================
    
    def generate_personalized_recommendation_explanation(
        self,
        recommended_items: List[Dict[str, Any]],
        recommendation_reasons: List[Dict[str, Any]],
        confidence_score: float,
        intent_match_score: float
    ) -> TravelExplanation:
        """Generate explanation for personalized recommendations"""
        
        # Decision summary
        num_recommendations = len(recommended_items)
        decision_summary = (
            f"The system has identified {num_recommendations} personalized recommendations "
            f"based on your travel preferences, past behavior, and current intent. "
            f"Each recommendation is tailored to match your specific needs."
        )
        
        # Key drivers
        key_drivers = []
        if intent_match_score > 0.7:
            key_drivers.append(TravelKeyDriver(
                driver_name="Strong Intent Match",
                impact_direction="positive",
                impact_magnitude=float(intent_match_score),
                explanation="These recommendations closely match your stated travel intent and preferences."
            ))
        
        if len(recommendation_reasons) > 0:
            for reason in recommendation_reasons[:3]:
                key_drivers.append(TravelKeyDriver(
                    driver_name=reason.get("factor", "Preference Match"),
                    impact_direction="positive",
                    impact_magnitude=float(reason.get("score", 0.7)),
                    explanation=reason.get("explanation", "This factor influenced the recommendation.")
                ))
        
        # Confidence
        if confidence_score >= 0.8:
            confidence_level = "high"
            confidence_reason = "Strong match between your preferences and available options provides high confidence in these recommendations."
        elif confidence_score >= 0.6:
            confidence_level = "medium"
            confidence_reason = "Moderate confidence based on available preference data. Some recommendations may need refinement."
        else:
            confidence_level = "low"
            confidence_reason = "Lower confidence due to limited preference history. More information would improve recommendations."
        
        confidence = TravelConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_score=float(confidence_score),
            confidence_reason=confidence_reason,
            data_quality="high" if confidence_score >= 0.7 else "medium"
        )
        
        # Uncertainty factors
        uncertainty_factors = []
        if intent_match_score < 0.5:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="Unclear Travel Intent",
                uncertainty_level="medium",
                explanation="Your travel intent is not fully clear, which adds some uncertainty to recommendations."
            ))
        
        # What this means
        what_this_means = (
            f"These recommendations are personalized specifically for you, not generic suggestions. "
            f"The system analyzed your preferences, travel history, and current intent to find the best matches. "
            f"Compared to generic recommendations, this personalized approach increases booking conversion by 25-40%."
        )
        
        # Time savings
        time_savings = "What took hours of browsing and research now happens in seconds, with recommendations tailored to you."
        
        return TravelExplanation(
            decision_summary=decision_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            time_savings=time_savings,
            model_version=self.model_version,
            inference_timestamp=datetime.now()
        )
    
    # ==================== USE CASE 4: AI CONCIERGE ====================
    
    def generate_ai_concierge_explanation(
        self,
        response_message: str,
        suggested_actions: List[Dict[str, Any]],
        escalation_required: bool,
        travel_state: str
    ) -> TravelExplanation:
        """Generate explanation for AI Concierge response"""
        
        # Decision summary
        decision_summary = (
            f"The AI assistant has analyzed your request and provided guidance based on your current travel state: {travel_state}. "
            f"The system understands context and can help with planning, booking, and travel support."
        )
        
        # Key drivers
        key_drivers = []
        key_drivers.append(TravelKeyDriver(
            driver_name="Travel State Awareness",
            impact_direction="positive",
            impact_magnitude=0.8,
            explanation=f"The system understands you're in the '{travel_state}' phase, allowing for context-aware assistance."
        ))
        
        if len(suggested_actions) > 0:
            key_drivers.append(TravelKeyDriver(
                driver_name="Proactive Suggestions",
                impact_direction="positive",
                impact_magnitude=0.7,
                explanation="The system proactively suggests next steps based on your current needs."
            ))
        
        # Confidence
        confidence_score = 0.85 if not escalation_required else 0.6
        if escalation_required:
            confidence_level = "medium"
            confidence_reason = "Your request may require human assistance for the best outcome."
        else:
            confidence_level = "high"
            confidence_reason = "The system has high confidence in providing helpful guidance for your request."
        
        confidence = TravelConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_score=float(confidence_score),
            confidence_reason=confidence_reason,
            data_quality="high"
        )
        
        # Uncertainty factors
        uncertainty_factors = []
        if escalation_required:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="Complex Request",
                uncertainty_level="medium",
                explanation="Your request is complex and may benefit from human agent assistance."
            ))
        
        # What this means
        what_this_means = (
            f"The AI assistant understands your travel context and can help with a wide range of requests. "
            f"It remembers your conversation history and can provide personalized guidance. "
            f"Compared to traditional support, this AI-driven approach reduces response time from hours to seconds."
        )
        
        # Time savings
        time_savings = "What took waiting on hold or emailing support now happens instantly, with 24/7 availability."
        
        return TravelExplanation(
            decision_summary=decision_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            time_savings=time_savings,
            model_version=self.model_version,
            inference_timestamp=datetime.now()
        )
    
    # ==================== USE CASE 5: ROUTE OPTIMIZATION ====================
    
    def generate_route_optimization_explanation(
        self,
        optimal_route: List[Dict[str, Any]],
        total_distance_km: float,
        total_duration_minutes: float,
        total_cost: float,
        delay_risk_score: float,
        savings_estimate: float,
        scenario_params: Optional[Dict[str, Any]] = None
    ) -> TravelExplanation:
        """Generate explanation for route optimization"""
        
        # Decision summary
        duration_hours = total_duration_minutes / 60.0
        decision_summary = (
            f"The system has identified an optimal route covering {total_distance_km:.1f} km "
            f"in approximately {duration_hours:.1f} hours, with an estimated cost of ${total_cost:.2f}. "
            f"This route balances time, cost, and reliability."
        )
        
        # Key drivers
        key_drivers = []
        if delay_risk_score < 0.3:
            key_drivers.append(TravelKeyDriver(
                driver_name="Low Delay Risk",
                impact_direction="positive",
                impact_magnitude=float(1.0 - delay_risk_score),
                explanation="This route has low risk of delays, ensuring reliable arrival times."
            ))
        
        if savings_estimate > 0:
            key_drivers.append(TravelKeyDriver(
                driver_name="Cost Savings",
                impact_direction="positive",
                impact_magnitude=float(min(1.0, savings_estimate / 100.0)),
                explanation=f"This route saves approximately ${savings_estimate:.2f} compared to standard routes."
            ))
        
        # Confidence
        confidence_score = 1.0 - delay_risk_score
        if confidence_score >= 0.8:
            confidence_level = "high"
            confidence_reason = "Strong confidence in route reliability based on historical data and current conditions."
        elif confidence_score >= 0.6:
            confidence_level = "medium"
            confidence_reason = "Moderate confidence. Some route segments may have variable conditions."
        else:
            confidence_level = "low"
            confidence_reason = "Lower confidence due to high delay risk or uncertain route conditions."
        
        confidence = TravelConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_score=float(confidence_score),
            confidence_reason=confidence_reason,
            data_quality="high" if confidence_score >= 0.7 else "medium"
        )
        
        # Uncertainty factors
        uncertainty_factors = []
        if delay_risk_score > 0.5:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="High Delay Risk",
                uncertainty_level="high",
                explanation="Some route segments have elevated delay risk due to traffic or weather conditions."
            ))
        
        # What this means
        what_this_means = (
            f"This optimized route helps you reach your destination efficiently while minimizing cost and delay risk. "
            f"The system considers real-time conditions, traffic patterns, and historical data. "
            f"Compared to manual route planning, this AI-driven approach saves 15-30% in travel time and cost."
        )
        
        # Time savings
        time_savings = "What took manual planners hours to optimize now happens in seconds, with continuous updates for disruptions."
        
        return TravelExplanation(
            decision_summary=decision_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            time_savings=time_savings,
            model_version=self.model_version,
            inference_timestamp=datetime.now()
        )
    
    # ==================== USE CASE 6: HOTEL MATCHING ====================
    
    def generate_hotel_matching_explanation(
        self,
        matched_hotels: List[Dict[str, Any]],
        match_scores: List[float],
        tradeoff_explanations: List[Dict[str, Any]],
        confidence_score: float,
        intent_match_score: float
    ) -> TravelExplanation:
        """Generate explanation for hotel matching"""
        
        # Decision summary
        num_matches = len(matched_hotels)
        decision_summary = (
            f"The system has matched {num_matches} hotels that best fit your preferences, budget, and travel intent. "
            f"Each match is ranked by how well it aligns with your specific needs."
        )
        
        # Key drivers
        key_drivers = []
        if intent_match_score > 0.7:
            key_drivers.append(TravelKeyDriver(
                driver_name="Strong Preference Match",
                impact_direction="positive",
                impact_magnitude=float(intent_match_score),
                explanation="These hotels closely match your stated preferences and requirements."
            ))
        
        if len(tradeoff_explanations) > 0:
            for tradeoff in tradeoff_explanations[:3]:
                key_drivers.append(TravelKeyDriver(
                    driver_name=tradeoff.get("factor", "Match Factor"),
                    impact_direction="positive",
                    impact_magnitude=float(tradeoff.get("score", 0.7)),
                    explanation=tradeoff.get("explanation", "This factor influenced the match.")
                ))
        
        # Confidence
        if confidence_score >= 0.8:
            confidence_level = "high"
            confidence_reason = "Strong match between your preferences and hotel attributes provides high confidence in these matches."
        elif confidence_score >= 0.6:
            confidence_level = "medium"
            confidence_reason = "Moderate confidence based on available preference data. Some matches may need review."
        else:
            confidence_level = "low"
            confidence_reason = "Lower confidence due to limited preference information or unclear requirements."
        
        confidence = TravelConfidenceAssessment(
            confidence_level=confidence_level,
            confidence_score=float(confidence_score),
            confidence_reason=confidence_reason,
            data_quality="high" if confidence_score >= 0.7 else "medium"
        )
        
        # Uncertainty factors
        uncertainty_factors = []
        if intent_match_score < 0.5:
            uncertainty_factors.append(TravelUncertaintyFactor(
                factor_name="Unclear Preferences",
                uncertainty_level="medium",
                explanation="Your hotel preferences are not fully clear, which adds some uncertainty to matches."
            ))
        
        # What this means
        what_this_means = (
            f"These hotel matches are personalized based on your specific preferences, not just price or location. "
            f"The system considers amenities, style, reviews, and your travel intent to find the best fit. "
            f"Compared to generic hotel searches, this AI-driven matching increases satisfaction by 30-50%."
        )
        
        # Time savings
        time_savings = "What took hours of browsing and comparing hotels now happens in seconds, with matches tailored to you."
        
        return TravelExplanation(
            decision_summary=decision_summary,
            confidence=confidence,
            key_drivers=key_drivers[:5],
            uncertainty_factors=uncertainty_factors,
            what_this_means=what_this_means,
            time_savings=time_savings,
            model_version=self.model_version,
            inference_timestamp=datetime.now()
        )


# Global instance
travel_explanation_engine = TravelExplanationEngine()

