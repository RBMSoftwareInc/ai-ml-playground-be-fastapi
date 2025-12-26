"""
Travel AI API Routes
Decision-intelligence APIs for travel operations, pricing, and personalization
6 Use Cases: Dynamic Pricing, Demand Forecasting, Personalized Recommendations,
            AI Concierge, Route Optimization, Hotel Matching
All responses include mandatory explanation contracts
"""
import numpy as np
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.schemas.travel import (
    DynamicPricingRequest, DynamicPricingResponse,
    DemandForecastRequest, DemandForecastResponse,
    PersonalizedRecommendationRequest, PersonalizedRecommendationResponse,
    AIConciergeRequest, AIConciergeResponse,
    RouteOptimizationRequest, RouteOptimizationResponse,
    HotelMatchingRequest, HotelMatchingResponse
)
from app.services.travel_scenarios import travel_scenario_catalog
from app.services.travel_ml_service import TravelMLService
from app.services.travel_explanation_engine import travel_explanation_engine
from app.services.travel_data_generator import TravelDataGenerator

router = APIRouter(tags=["Travel AI"])

# Initialize services
travel_ml_service = TravelMLService()
travel_data_generator = TravelDataGenerator(seed=42)


# ==================== USE CASE 1: DYNAMIC PRICING ENGINE ====================

@router.post("/dynamic-pricing", response_model=DynamicPricingResponse)
async def dynamic_pricing_engine(request: DynamicPricingRequest):
    """
    Dynamic Pricing Engine - Real-time pricing optimization
    
    Adapts prices to demand, seasonality, and market conditions.
    Scenarios: baseline, peak_season, low_season, event_surge, last_minute
    """
    try:
        # Get scenario parameters
        scenario_params = travel_scenario_catalog.get_scenario_params("dynamic_pricing", request.scenario)
        if scenario_params is None:
            scenario_params = {}
        
        # Generate pricing event data
        pricing_event = travel_data_generator.generate_pricing_event(
            request.property_id,
            request.target_date,
            request.current_price or 100.0
        )
        
        # Prepare features for ML model
        base_price = request.current_price or pricing_event["base_price"]
        features = [
            pricing_event["demand_level"],
            pricing_event["booking_velocity"] / 20.0,  # Normalize
            pricing_event["seasonality_factor"],
            pricing_event["event_impact"],
            (request.lead_time_days or pricing_event["lead_time_days"]) / 365.0,
            pricing_event["occupancy_rate"],
            pricing_event["competitor_price_avg"] / base_price
        ]
        
        # Predict optimal price
        price_min, price_max, price_optimal, confidence_score, model_metadata = travel_ml_service.predict_dynamic_pricing(
            features, scenario_params
        )
        
        # Calculate demand surge indicator
        demand_surge_indicator = pricing_event["demand_level"]
        seasonality_impact = pricing_event["seasonality_factor"]
        
        # Top drivers
        top_drivers = [
            {
                "name": "Demand Level",
                "direction": "positive" if demand_surge_indicator > 0.5 else "negative",
                "magnitude": float(demand_surge_indicator),
                "explanation": f"Current demand level is {'high' if demand_surge_indicator > 0.5 else 'low'}, influencing pricing."
            },
            {
                "name": "Seasonality",
                "direction": "positive" if seasonality_impact > 1.0 else "negative",
                "magnitude": float(abs(seasonality_impact - 1.0)),
                "explanation": f"Seasonal factors {'increase' if seasonality_impact > 1.0 else 'decrease'} pricing by {abs(seasonality_impact - 1.0) * 100:.1f}%."
            },
            {
                "name": "Booking Velocity",
                "direction": "positive" if pricing_event["booking_velocity"] > 10 else "negative",
                "magnitude": float(min(1.0, pricing_event["booking_velocity"] / 20.0)),
                "explanation": f"Booking velocity is {pricing_event['booking_velocity']:.1f} bookings/day."
            }
        ]
        
        # Generate explanation
        explanation = travel_explanation_engine.generate_dynamic_pricing_explanation(
            price_min=price_min,
            price_max=price_max,
            price_optimal=price_optimal,
            confidence_score=confidence_score,
            top_drivers=top_drivers,
            demand_surge_indicator=demand_surge_indicator,
            seasonality_impact=seasonality_impact,
            scenario_params=scenario_params
        )
        
        return DynamicPricingResponse(
            success=True,
            property_id=request.property_id,
            recommendation_date=datetime.now(),
            recommended_price_min=price_min,
            recommended_price_max=price_max,
            recommended_price_optimal=price_optimal,
            confidence_score=confidence_score,
            top_drivers=top_drivers,
            demand_surge_indicator=demand_surge_indicator,
            seasonality_impact=seasonality_impact,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "pricing_event": pricing_event,
                "model_metadata": model_metadata
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in dynamic pricing: {str(e)}")


# ==================== USE CASE 2: DEMAND FORECASTING ====================

@router.post("/demand-forecast", response_model=DemandForecastResponse)
async def demand_forecast(request: DemandForecastRequest):
    """
    Demand Forecasting - Predictive demand analysis
    
    Forecasts demand windows and uncertainty bands.
    Scenarios: baseline, holiday_boost, event_boost, economic_downturn, seasonal_transition
    """
    try:
        # Get scenario parameters
        scenario_params = travel_scenario_catalog.get_scenario_params("demand_forecast", request.scenario)
        if scenario_params is None:
            scenario_params = {}
        
        # Generate booking history data
        base_date = datetime.now()
        travel_date = base_date + timedelta(days=request.forecast_horizon_days // 2)
        booking_date = base_date - timedelta(days=30)
        
        booking_history = travel_data_generator.generate_booking_history(
            request.property_id,
            booking_date,
            travel_date
        )
        
        # Prepare features for ML model
        season_encoded = {"peak": 1.0, "shoulder": 0.5, "off": 0.0}.get(booking_history["season"], 0.5)
        features = [
            request.forecast_horizon_days / 180.0,  # Normalize
            season_encoded,
            1.0 if booking_history["holiday_flag"] else 0.0,
            1.0 if booking_history["event_flag"] else 0.0,
            booking_history["weather_impact"]
        ]
        
        # Predict demand
        forecasted_demand, confidence_lower, confidence_upper, trend_direction, risk_zones, holiday_impact, event_impact, model_metadata = travel_ml_service.predict_demand_forecast(
            features, scenario_params
        )
        
        # Generate explanation
        explanation = travel_explanation_engine.generate_demand_forecast_explanation(
            forecasted_demand=forecasted_demand,
            confidence_lower=confidence_lower,
            confidence_upper=confidence_upper,
            trend_direction=trend_direction,
            risk_zones=risk_zones,
            holiday_impact=holiday_impact,
            event_impact=event_impact,
            scenario_params=scenario_params
        )
        
        return DemandForecastResponse(
            success=True,
            property_id=request.property_id,
            forecast_date=datetime.now(),
            forecasted_demand=forecasted_demand,
            confidence_band_lower=confidence_lower,
            confidence_band_upper=confidence_upper,
            trend_direction=trend_direction,
            risk_zones=risk_zones,
            holiday_impact=holiday_impact,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "booking_history": booking_history,
                "model_metadata": model_metadata
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in demand forecasting: {str(e)}")


# ==================== USE CASE 3: PERSONALIZED RECOMMENDATIONS ====================

@router.post("/personalized-recommendations", response_model=PersonalizedRecommendationResponse)
async def personalized_recommendations(request: PersonalizedRecommendationRequest):
    """
    Personalized Recommendations - AI-driven travel recommendations
    
    Adapts recommendations to traveler intent, timing, and behavior.
    """
    try:
        # Generate or retrieve traveler profile
        if request.traveler_id:
            traveler_profile = travel_data_generator.generate_traveler_profile(request.traveler_id)
        else:
            # Use provided traveler data
            traveler_data = request.traveler_data or {}
            traveler_profile = {
                "traveler_id": "GENERATED",
                "travel_style": request.travel_style or traveler_data.get("travel_style", "budget"),
                "preferred_destinations": [request.destination] if request.destination else traveler_data.get("preferred_destinations", []),
                "budget_range_min": request.budget * 0.7 if request.budget else traveler_data.get("budget_range_min", 100),
                "budget_range_max": request.budget * 1.3 if request.budget else traveler_data.get("budget_range_max", 300)
            }
        
        # Generate traveler intent
        traveler_intent = travel_data_generator.generate_traveler_intent(
            traveler_profile["traveler_id"],
            datetime.now()
        )
        
        # Override with request data if provided
        if request.destination:
            traveler_intent["destination_preference"] = request.destination
        if request.travel_date:
            traveler_intent["travel_date_preference"] = request.travel_date
        if request.duration_days:
            traveler_intent["duration_days"] = request.duration_days
        if request.budget:
            traveler_intent["budget_constraint"] = request.budget
        
        # Generate recommendations (simplified - would use embeddings in production)
        recommended_items = [
            {
                "item_id": f"REC_{i}",
                "item_type": "destination",
                "name": traveler_intent["destination_preference"],
                "match_score": float(0.9 - i * 0.1),
                "reason": f"Matches your {traveler_intent['intent_type']} travel style"
            }
            for i in range(5)
        ]
        
        recommendation_reasons = [
            {
                "factor": "Travel Style Match",
                "score": 0.85,
                "explanation": f"Matches your {traveler_profile['travel_style']} travel style"
            },
            {
                "factor": "Budget Fit",
                "score": 0.80,
                "explanation": f"Fits within your budget range of ${traveler_intent['budget_constraint']:.0f}"
            },
            {
                "factor": "Destination Preference",
                "score": 0.75,
                "explanation": f"Matches your preferred destination: {traveler_intent['destination_preference']}"
            }
        ]
        
        confidence_score = float(traveler_intent["intent_confidence"])
        intent_match_score = float(traveler_intent["intent_confidence"] * 0.9)
        
        # Generate explanation
        explanation = travel_explanation_engine.generate_personalized_recommendation_explanation(
            recommended_items=recommended_items,
            recommendation_reasons=recommendation_reasons,
            confidence_score=confidence_score,
            intent_match_score=intent_match_score
        )
        
        return PersonalizedRecommendationResponse(
            success=True,
            traveler_id=traveler_profile["traveler_id"],
            recommendation_date=datetime.now(),
            recommended_items=recommended_items,
            recommendation_reasons=recommendation_reasons,
            confidence_score=confidence_score,
            intent_match_score=intent_match_score,
            explanation=explanation,
            metadata={
                "traveler_profile": traveler_profile,
                "traveler_intent": traveler_intent
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in personalized recommendations: {str(e)}")


# ==================== USE CASE 4: AI CONCIERGE ====================

@router.post("/ai-concierge", response_model=AIConciergeResponse)
async def ai_concierge(request: AIConciergeRequest):
    """
    AI Concierge - Conversational travel assistant
    
    Anticipates needs and reduces friction in travel planning and support.
    """
    try:
        # Generate or retrieve conversation context
        conversation_id = request.conversation_id or f"CONV_{datetime.now().timestamp()}"
        
        conversation_context = travel_data_generator.generate_conversation_context(
            conversation_id,
            request.traveler_id
        )
        
        # Override travel state if provided
        if request.travel_state:
            conversation_context["travel_state"] = request.travel_state
        
        # Generate response (simplified - would use LLM in production)
        response_message = (
            f"I understand you're in the {conversation_context['travel_state']} phase. "
            f"Based on your message, I can help you with {conversation_context['current_intent']}. "
            f"Here are some options I'd recommend."
        )
        
        suggested_actions = conversation_context["suggested_actions"]
        escalation_required = conversation_context["escalation_required"]
        
        # Generate explanation
        explanation = travel_explanation_engine.generate_ai_concierge_explanation(
            response_message=response_message,
            suggested_actions=suggested_actions,
            escalation_required=escalation_required,
            travel_state=conversation_context["travel_state"]
        )
        
        return AIConciergeResponse(
            success=True,
            conversation_id=conversation_id,
            traveler_id=request.traveler_id,
            response_message=response_message,
            suggested_actions=suggested_actions,
            escalation_required=escalation_required,
            travel_state=conversation_context["travel_state"],
            explanation=explanation,
            metadata={
                "conversation_context": conversation_context
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in AI concierge: {str(e)}")


# ==================== USE CASE 5: ROUTE OPTIMIZATION ====================

@router.post("/route-optimization", response_model=RouteOptimizationResponse)
async def route_optimization(request: RouteOptimizationRequest):
    """
    Route Optimization - Adaptive route planning
    
    Routes adapt to constraints and disruptions.
    Scenarios: baseline, heavy_traffic, weather_disruption, peak_travel, optimal_conditions
    """
    try:
        # Get scenario parameters
        scenario_params = travel_scenario_catalog.get_scenario_params("route_optimization", request.scenario)
        if scenario_params is None:
            scenario_params = {}
        
        # Generate route ID if not provided
        route_id = request.route_id or f"ROUTE_{request.origin}_{request.destination}"
        
        # Generate route segments
        segment_date = request.travel_date or datetime.now()
        route_segment = travel_data_generator.generate_route_segment(
            route_id,
            request.origin,
            request.destination,
            segment_date
        )
        
        # Prepare features for ML model
        traffic_encoded = {"normal": 0.0, "heavy": 0.5, "light": -0.2}.get(route_segment["traffic_conditions"], 0.0)
        features = [
            route_segment["distance_km"] / 2000.0,
            route_segment["disruption_risk"],
            route_segment["weather_impact"],
            traffic_encoded
        ]
        
        # Predict delay risk
        delay_risk_score, model_metadata = travel_ml_service.predict_route_delay_risk(
            features, scenario_params
        )
        
        # Generate optimal route (simplified - would use graph algorithms in production)
        optimal_route = [
            {
                "segment_id": f"SEG_1",
                "origin": request.origin,
                "destination": request.destination,
                "distance_km": float(route_segment["distance_km"]),
                "duration_minutes": float(route_segment["estimated_duration_minutes"]),
                "cost": float(route_segment["cost"])
            }
        ]
        
        total_distance_km = route_segment["distance_km"]
        total_duration_minutes = route_segment["estimated_duration_minutes"]
        total_cost = route_segment["cost"]
        
        # Calculate savings estimate (simplified)
        baseline_cost = total_cost * 1.2  # Assume baseline is 20% more expensive
        savings_estimate = baseline_cost - total_cost
        
        # Generate explanation
        explanation = travel_explanation_engine.generate_route_optimization_explanation(
            optimal_route=optimal_route,
            total_distance_km=total_distance_km,
            total_duration_minutes=total_duration_minutes,
            total_cost=total_cost,
            delay_risk_score=delay_risk_score,
            savings_estimate=savings_estimate,
            scenario_params=scenario_params
        )
        
        return RouteOptimizationResponse(
            success=True,
            route_id=route_id,
            optimization_date=datetime.now(),
            optimal_route=optimal_route,
            total_distance_km=total_distance_km,
            total_duration_minutes=total_duration_minutes,
            total_cost=total_cost,
            delay_risk_score=delay_risk_score,
            savings_estimate=savings_estimate,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "route_segment": route_segment,
                "model_metadata": model_metadata
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in route optimization: {str(e)}")


# ==================== USE CASE 6: HOTEL MATCHING AI ====================

@router.post("/hotel-matching", response_model=HotelMatchingResponse)
async def hotel_matching(request: HotelMatchingRequest):
    """
    Hotel Matching AI - Intelligent hotel matching
    
    Matches traveler intent with accommodation attributes.
    """
    try:
        # Generate or retrieve traveler profile
        if request.traveler_id:
            traveler_profile = travel_data_generator.generate_traveler_profile(request.traveler_id)
        else:
            traveler_data = request.traveler_data or {}
            traveler_profile = {
                "traveler_id": "GENERATED",
                "travel_style": traveler_data.get("travel_style", "budget"),
                "budget_range_min": request.budget * 0.7 if request.budget else traveler_data.get("budget_range_min", 100),
                "budget_range_max": request.budget * 1.3 if request.budget else traveler_data.get("budget_range_max", 300)
            }
        
        # Generate hotel profiles (simplified - would use embeddings in production)
        matched_hotels = []
        match_scores = []
        tradeoff_explanations = []
        
        for i in range(5):
            hotel_profile = travel_data_generator.generate_hotel_profile(
                f"HOTEL_{i}",
                request.destination
            )
            
            # Calculate match score (simplified)
            budget_match = 1.0 if (hotel_profile["price_range_min"] >= traveler_profile["budget_range_min"] and
                                   hotel_profile["price_range_max"] <= traveler_profile["budget_range_max"]) else 0.7
            style_match = 0.9 if hotel_profile["hotel_type"] == traveler_profile["travel_style"] else 0.6
            match_score = float((budget_match + style_match) / 2.0 - i * 0.05)
            
            matched_hotels.append({
                "hotel_id": hotel_profile["hotel_id"],
                "hotel_name": hotel_profile["hotel_name"],
                "location": hotel_profile["location"],
                "price_range_min": hotel_profile["price_range_min"],
                "price_range_max": hotel_profile["price_range_max"],
                "star_rating": hotel_profile["star_rating"],
                "amenities": hotel_profile["amenities"],
                "hotel_type": hotel_profile["hotel_type"],
                "guest_rating_avg": hotel_profile["guest_rating_avg"]
            })
            
            match_scores.append(match_score)
            
            tradeoff_explanations.append({
                "hotel_id": hotel_profile["hotel_id"],
                "factor": "Budget vs. Amenities",
                "score": match_score,
                "explanation": f"Balances price range (${hotel_profile['price_range_min']:.0f}-${hotel_profile['price_range_max']:.0f}) with {len(hotel_profile['amenities'])} amenities."
            })
        
        confidence_score = float(np.mean(match_scores))
        intent_match_score = float(np.mean(match_scores) * 0.95)
        
        # Generate explanation
        explanation = travel_explanation_engine.generate_hotel_matching_explanation(
            matched_hotels=matched_hotels,
            match_scores=match_scores,
            tradeoff_explanations=tradeoff_explanations,
            confidence_score=confidence_score,
            intent_match_score=intent_match_score
        )
        
        return HotelMatchingResponse(
            success=True,
            traveler_id=traveler_profile["traveler_id"],
            match_date=datetime.now(),
            matched_hotels=matched_hotels,
            match_scores=match_scores,
            tradeoff_explanations=tradeoff_explanations,
            confidence_score=confidence_score,
            intent_match_score=intent_match_score,
            explanation=explanation,
            metadata={
                "traveler_profile": traveler_profile,
                "destination": request.destination
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in hotel matching: {str(e)}")


# ==================== SCENARIOS ENDPOINT ====================

@router.get("/scenarios")
async def get_scenarios():
    """Get available scenarios for all Travel AI modules"""
    return travel_scenario_catalog.get_all_scenarios()
