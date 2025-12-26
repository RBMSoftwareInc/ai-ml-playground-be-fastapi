"""
Travel AI Data Generator
Synthetic data generation for travel use cases
Statistically realistic, preserves correlations, seasonality, and edge cases
"""
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


class TravelDataGenerator:
    """Generate synthetic travel data aligned to real-world distributions"""
    
    def __init__(self, seed: int = 42):
        """Initialize generator with seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
        self.seed = seed
    
    # ==================== USE CASE 1: DYNAMIC PRICING ====================
    
    def generate_pricing_event(
        self,
        property_id: str,
        event_date: datetime,
        base_price: float = 100.0
    ) -> Dict[str, Any]:
        """Generate a pricing event with demand signals"""
        # Seasonality factor (higher in summer, lower in winter)
        month = event_date.month
        seasonality_factor = 0.7 + 0.3 * np.sin(2 * np.pi * (month - 6) / 12)
        
        # Demand level (0.0 to 1.0)
        demand_level = np.clip(
            np.random.beta(2, 3) + seasonality_factor * 0.3 - 0.15,
            0.0, 1.0
        )
        
        # Booking velocity (bookings per day)
        booking_velocity = np.random.exponential(5.0) * (1 + demand_level * 2)
        
        # Event impact (occasional spikes)
        event_impact = 0.0
        if np.random.random() < 0.1:  # 10% chance of event
            event_impact = np.random.uniform(0.2, 0.5)
        
        # Lead time (days before travel)
        lead_time_days = int(np.random.exponential(30))
        
        # Occupancy rate
        occupancy_rate = np.clip(
            demand_level + np.random.normal(0, 0.1),
            0.0, 1.0
        )
        
        # Competitor price (similar to base price with variation)
        competitor_price_avg = base_price * np.random.uniform(0.9, 1.1)
        
        # Price elasticity (how sensitive demand is to price)
        price_elasticity = np.random.uniform(-2.0, -0.5)  # Negative (demand decreases with price)
        
        # Actual price (base price adjusted by demand)
        price_multiplier = 1.0 + (demand_level - 0.5) * 0.4 + event_impact
        actual_price = base_price * price_multiplier
        
        return {
            "property_id": property_id,
            "event_date": event_date,
            "base_price": float(base_price),
            "actual_price": float(actual_price),
            "demand_level": float(demand_level),
            "booking_velocity": float(booking_velocity),
            "seasonality_factor": float(seasonality_factor),
            "event_impact": float(event_impact),
            "lead_time_days": int(lead_time_days),
            "occupancy_rate": float(occupancy_rate),
            "competitor_price_avg": float(competitor_price_avg),
            "price_elasticity": float(price_elasticity)
        }
    
    # ==================== USE CASE 2: DEMAND FORECASTING ====================
    
    def generate_booking_history(
        self,
        property_id: str,
        booking_date: datetime,
        travel_date: datetime
    ) -> Dict[str, Any]:
        """Generate booking history entry"""
        lead_time_days = (travel_date - booking_date).days
        
        # Season classification
        month = travel_date.month
        if month in [6, 7, 8, 12]:  # Summer and December
            season = "peak"
        elif month in [3, 4, 5, 9, 10, 11]:  # Spring and Fall
            season = "shoulder"
        else:  # Winter
            season = "off"
        
        # Holiday flag
        holiday_flag = np.random.random() < 0.15  # 15% chance
        
        # Event flag
        event_flag = np.random.random() < 0.1  # 10% chance
        
        # Booking count (higher in peak season)
        base_count = 10 if season == "peak" else (5 if season == "shoulder" else 3)
        booking_count = int(np.random.poisson(base_count))
        if holiday_flag:
            booking_count = int(booking_count * 1.5)
        if event_flag:
            booking_count = int(booking_count * 1.3)
        
        # Cancellation count (5-10% cancellation rate)
        cancellation_rate = np.random.uniform(0.05, 0.10)
        cancellation_count = int(booking_count * cancellation_rate)
        
        # Weather impact
        weather_impact = np.random.uniform(-0.2, 0.2)
        
        return {
            "property_id": property_id,
            "booking_date": booking_date,
            "travel_date": travel_date,
            "booking_count": int(booking_count),
            "cancellation_count": int(cancellation_count),
            "lead_time_days": int(lead_time_days),
            "season": season,
            "holiday_flag": bool(holiday_flag),
            "event_flag": bool(event_flag),
            "weather_impact": float(weather_impact)
        }
    
    # ==================== USE CASE 3: PERSONALIZED RECOMMENDATIONS ====================
    
    def generate_traveler_profile(
        self,
        traveler_id: str
    ) -> Dict[str, Any]:
        """Generate traveler profile with preferences"""
        travel_styles = ["budget", "luxury", "business", "adventure", "family"]
        travel_style = np.random.choice(travel_styles, p=[0.3, 0.2, 0.2, 0.15, 0.15])
        
        # Budget range based on style
        if travel_style == "budget":
            budget_min = np.random.uniform(50, 150)
            budget_max = budget_min * np.random.uniform(1.5, 2.5)
        elif travel_style == "luxury":
            budget_min = np.random.uniform(300, 800)
            budget_max = budget_min * np.random.uniform(1.5, 2.0)
        else:
            budget_min = np.random.uniform(150, 400)
            budget_max = budget_min * np.random.uniform(1.5, 2.0)
        
        # Preferred destinations (random selection)
        all_destinations = ["Paris", "Tokyo", "New York", "Bali", "London", "Dubai", "Sydney", "Rome"]
        num_preferred = np.random.randint(2, 5)
        preferred_destinations = random.sample(all_destinations, num_preferred)
        
        # Accommodation preferences
        accommodation_preferences = {
            "amenities": random.sample(
                ["wifi", "pool", "gym", "spa", "restaurant", "parking"],
                np.random.randint(2, 5)
            ),
            "room_type": np.random.choice(["standard", "suite", "villa"]),
            "location_preference": np.random.choice(["city_center", "airport", "beach", "mountains"])
        }
        
        # Activity preferences
        all_activities = ["sightseeing", "shopping", "adventure", "culture", "nightlife", "nature", "food"]
        activity_preferences = random.sample(
            all_activities,
            np.random.randint(2, 5)
        )
        
        # Season preferences
        season_preferences = random.sample(
            ["spring", "summer", "fall", "winter"],
            np.random.randint(1, 3)
        )
        
        # Generate preference embeddings (simplified - would use real embeddings in production)
        preference_embeddings = np.random.rand(128).tolist()
        
        return {
            "traveler_id": traveler_id,
            "preference_embeddings": preference_embeddings,
            "travel_history_count": int(np.random.poisson(5)),
            "preferred_destinations": preferred_destinations,
            "budget_range_min": float(budget_min),
            "budget_range_max": float(budget_max),
            "travel_style": travel_style,
            "accommodation_preferences": accommodation_preferences,
            "activity_preferences": activity_preferences,
            "season_preferences": season_preferences
        }
    
    def generate_traveler_intent(
        self,
        traveler_id: str,
        intent_date: datetime
    ) -> Dict[str, Any]:
        """Generate traveler intent signal"""
        intent_types = ["leisure", "business", "family", "romantic", "adventure"]
        intent_type = np.random.choice(intent_types, p=[0.4, 0.25, 0.15, 0.1, 0.1])
        
        destinations = ["Paris", "Tokyo", "New York", "Bali", "London", "Dubai"]
        destination_preference = np.random.choice(destinations)
        
        # Travel date preference (30-180 days ahead)
        travel_date_preference = intent_date + timedelta(days=np.random.randint(30, 180))
        
        duration_days = int(np.random.exponential(7))  # Average 7 days
        duration_days = max(2, min(duration_days, 30))  # Clamp to 2-30 days
        
        group_size = int(np.random.poisson(2)) + 1  # At least 1, average 2
        
        budget_constraint = np.random.uniform(500, 5000)
        
        intent_confidence = np.random.uniform(0.6, 0.95)
        
        return {
            "traveler_id": traveler_id,
            "intent_date": intent_date,
            "intent_type": intent_type,
            "destination_preference": destination_preference,
            "travel_date_preference": travel_date_preference,
            "duration_days": int(duration_days),
            "group_size": int(group_size),
            "budget_constraint": float(budget_constraint),
            "intent_confidence": float(intent_confidence)
        }
    
    # ==================== USE CASE 4: AI CONCIERGE ====================
    
    def generate_conversation_context(
        self,
        conversation_id: str,
        traveler_id: str
    ) -> Dict[str, Any]:
        """Generate conversation context for AI Concierge"""
        travel_states = ["planning", "booked", "in_travel", "post_travel"]
        travel_state = np.random.choice(travel_states, p=[0.4, 0.3, 0.2, 0.1])
        
        # Conversation history (simplified)
        conversation_history = [
            {"role": "user", "message": "I need help planning my trip"},
            {"role": "assistant", "message": "I'd be happy to help! Where are you planning to travel?"}
        ]
        
        current_intent = np.random.choice([
            "find_hotel", "book_activity", "get_recommendations", "change_booking", "ask_question"
        ])
        
        suggested_actions = [
            {"action": "search_hotels", "confidence": 0.8},
            {"action": "view_recommendations", "confidence": 0.7}
        ]
        
        escalation_required = np.random.random() < 0.1  # 10% chance
        
        return {
            "conversation_id": conversation_id,
            "traveler_id": traveler_id,
            "travel_state": travel_state,
            "conversation_history": conversation_history,
            "current_intent": current_intent,
            "suggested_actions": suggested_actions,
            "escalation_required": bool(escalation_required)
        }
    
    # ==================== USE CASE 5: ROUTE OPTIMIZATION ====================
    
    def generate_route_segment(
        self,
        route_id: str,
        origin: str,
        destination: str,
        segment_date: datetime
    ) -> Dict[str, Any]:
        """Generate route segment data"""
        # Distance (km) - random but realistic
        distance_km = np.random.uniform(50, 2000)
        
        # Estimated duration (minutes) - based on distance and speed
        avg_speed_kmh = np.random.uniform(60, 120)  # Varies by route type
        estimated_duration_minutes = (distance_km / avg_speed_kmh) * 60
        
        # Cost (varies by distance and route type)
        cost_per_km = np.random.uniform(0.5, 2.0)
        cost = distance_km * cost_per_km
        
        # Capacity
        capacity = int(np.random.uniform(50, 500))
        
        # Disruption risk (0.0 to 1.0)
        disruption_risk = np.random.beta(2, 8)  # Low risk on average
        
        # Weather impact
        weather_impact = np.random.uniform(-0.1, 0.1)
        
        # Traffic conditions
        traffic_conditions = np.random.choice(
            ["normal", "heavy", "light"],
            p=[0.7, 0.2, 0.1]
        )
        
        return {
            "route_id": route_id,
            "origin": origin,
            "destination": destination,
            "segment_date": segment_date,
            "distance_km": float(distance_km),
            "estimated_duration_minutes": float(estimated_duration_minutes),
            "cost": float(cost),
            "capacity": int(capacity),
            "disruption_risk": float(disruption_risk),
            "weather_impact": float(weather_impact),
            "traffic_conditions": traffic_conditions
        }
    
    # ==================== USE CASE 6: HOTEL MATCHING ====================
    
    def generate_hotel_profile(
        self,
        hotel_id: str,
        location: str
    ) -> Dict[str, Any]:
        """Generate hotel profile with attributes"""
        hotel_names = [
            "Grand Plaza Hotel", "Seaside Resort", "City Center Inn",
            "Mountain View Lodge", "Business Tower Hotel", "Boutique Garden"
        ]
        hotel_name = np.random.choice(hotel_names) + f" {location}"
        
        # Price range
        price_range_min = np.random.uniform(50, 500)
        price_range_max = price_range_min * np.random.uniform(1.5, 3.0)
        
        # Star rating
        star_rating = int(np.random.choice([3, 4, 5], p=[0.3, 0.5, 0.2]))
        
        # Amenities
        all_amenities = ["wifi", "pool", "gym", "spa", "restaurant", "parking", "airport_shuttle", "concierge"]
        num_amenities = np.random.randint(3, 7)
        amenities = random.sample(all_amenities, num_amenities)
        
        # Hotel type
        hotel_types = ["luxury", "budget", "boutique", "resort", "business"]
        hotel_type = np.random.choice(hotel_types, p=[0.2, 0.3, 0.2, 0.15, 0.15])
        
        # Guest rating
        guest_rating_avg = np.random.uniform(3.5, 5.0)
        
        # Generate embeddings (simplified)
        location_embedding = np.random.rand(64).tolist()
        attribute_embeddings = np.random.rand(128).tolist()
        
        return {
            "hotel_id": hotel_id,
            "hotel_name": hotel_name,
            "location": location,
            "location_embedding": location_embedding,
            "price_range_min": float(price_range_min),
            "price_range_max": float(price_range_max),
            "star_rating": int(star_rating),
            "amenities": amenities,
            "hotel_type": hotel_type,
            "guest_rating_avg": float(guest_rating_avg),
            "attribute_embeddings": attribute_embeddings
        }

