"""
Travel AI Models
Decision-intelligence models for travel operations, pricing, and personalization
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


# ==================== PILLAR 1: PRICING & REVENUE INTELLIGENCE ====================

# Use Case 1: Dynamic Pricing Engine
class PricingEvent(Base):
    """Historical pricing events and demand signals"""
    __tablename__ = "pricing_events"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String(100), nullable=False, index=True)  # Hotel, flight route, etc.
    event_date = Column(DateTime(timezone=True), nullable=False, index=True)
    base_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=False)
    demand_level = Column(Float, nullable=False)  # 0.0 to 1.0
    booking_velocity = Column(Float, nullable=False)  # Bookings per day
    seasonality_factor = Column(Float)  # Seasonal adjustment
    event_impact = Column(Float)  # External event impact
    lead_time_days = Column(Integer)  # Days before travel
    occupancy_rate = Column(Float)  # Current occupancy
    competitor_price_avg = Column(Float)  # Average competitor price
    price_elasticity = Column(Float)  # Estimated price sensitivity
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_pricing_property_date', 'property_id', 'event_date'),
    )


class PricingRecommendation(Base):
    """Dynamic pricing recommendations"""
    __tablename__ = "pricing_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String(100), nullable=False, index=True)
    recommendation_date = Column(DateTime(timezone=True), nullable=False, index=True)
    recommended_price_min = Column(Float, nullable=False)
    recommended_price_max = Column(Float, nullable=False)
    recommended_price_optimal = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    top_drivers = Column(JSON)  # Top factors influencing price
    demand_surge_indicator = Column(Float)  # 0.0 to 1.0
    seasonality_impact = Column(Float)  # Seasonal adjustment factor
    lead_time_factor = Column(Float)  # Lead time impact
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_pricing_rec_property_date', 'property_id', 'recommendation_date'),
    )


# Use Case 2: Demand Forecasting
class BookingHistory(Base):
    """Historical booking patterns"""
    __tablename__ = "booking_history"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String(100), nullable=False, index=True)
    booking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    travel_date = Column(DateTime(timezone=True), nullable=False, index=True)
    booking_count = Column(Integer, nullable=False)
    cancellation_count = Column(Integer, default=0)
    lead_time_days = Column(Integer)  # Days between booking and travel
    season = Column(String(20))  # 'peak', 'shoulder', 'off'
    holiday_flag = Column(Boolean, default=False)
    event_flag = Column(Boolean, default=False)
    weather_impact = Column(Float)  # Weather impact on bookings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_booking_property_travel_date', 'property_id', 'travel_date'),
    )


class DemandForecast(Base):
    """Demand forecasting predictions"""
    __tablename__ = "demand_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String(100), nullable=False, index=True)
    forecast_date = Column(DateTime(timezone=True), nullable=False, index=True)
    target_date = Column(DateTime(timezone=True), nullable=False, index=True)
    forecasted_demand = Column(Float, nullable=False)
    confidence_band_lower = Column(Float, nullable=False)
    confidence_band_upper = Column(Float, nullable=False)
    trend_direction = Column(String(20))  # 'increasing', 'decreasing', 'stable'
    risk_zones = Column(JSON)  # High/medium/low risk periods
    holiday_impact = Column(Float)  # Holiday impact on demand
    event_impact = Column(Float)  # Event impact on demand
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_forecast_property_target', 'property_id', 'target_date'),
    )


# ==================== PILLAR 2: PERSONALIZED TRAVEL INTELLIGENCE ====================

# Use Case 3: Personalized Recommendations
class TravelerProfile(Base):
    """Traveler preferences and behavior"""
    __tablename__ = "traveler_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    traveler_id = Column(String(100), unique=True, index=True, nullable=False)
    preference_embeddings = Column(JSON)  # Vector embeddings of preferences
    travel_history_count = Column(Integer, default=0)
    preferred_destinations = Column(JSON)  # List of preferred destinations
    budget_range_min = Column(Float)
    budget_range_max = Column(Float)
    travel_style = Column(String(50))  # 'budget', 'luxury', 'business', 'adventure'
    accommodation_preferences = Column(JSON)  # Hotel preferences
    activity_preferences = Column(JSON)  # Activity interests
    season_preferences = Column(JSON)  # Preferred travel seasons
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TravelerIntent(Base):
    """Traveler intent signals"""
    __tablename__ = "traveler_intents"
    
    id = Column(Integer, primary_key=True, index=True)
    traveler_id = Column(String(100), ForeignKey("traveler_profiles.traveler_id"), nullable=False, index=True)
    intent_date = Column(DateTime(timezone=True), nullable=False, index=True)
    intent_type = Column(String(50))  # 'leisure', 'business', 'family', 'romantic'
    destination_preference = Column(String(200))
    travel_date_preference = Column(DateTime(timezone=True))
    duration_days = Column(Integer)
    group_size = Column(Integer)
    budget_constraint = Column(Float)
    intent_confidence = Column(Float)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    traveler = relationship("TravelerProfile", backref="intents")


class RecommendationResult(Base):
    """Personalized recommendation results"""
    __tablename__ = "recommendation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    traveler_id = Column(String(100), nullable=False, index=True)
    recommendation_date = Column(DateTime(timezone=True), nullable=False, index=True)
    recommended_items = Column(JSON)  # Ranked list of recommendations
    recommendation_reasons = Column(JSON)  # Why each item was recommended
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    intent_match_score = Column(Float)  # How well recommendations match intent
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_rec_traveler_date', 'traveler_id', 'recommendation_date'),
    )


# Use Case 4: AI Concierge
class ConversationContext(Base):
    """AI Concierge conversation context"""
    __tablename__ = "conversation_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(100), unique=True, index=True, nullable=False)
    traveler_id = Column(String(100), nullable=False, index=True)
    travel_state = Column(String(50))  # 'planning', 'booked', 'in_travel', 'post_travel'
    conversation_history = Column(JSON)  # Message history
    current_intent = Column(String(100))  # Current user intent
    suggested_actions = Column(JSON)  # AI-suggested next actions
    escalation_required = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ==================== PILLAR 3: OPERATIONAL INTELLIGENCE ====================

# Use Case 5: Route Optimization
class RouteSegment(Base):
    """Route segments and connections"""
    __tablename__ = "route_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String(100), nullable=False, index=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    segment_date = Column(DateTime(timezone=True), nullable=False, index=True)
    distance_km = Column(Float, nullable=False)
    estimated_duration_minutes = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    capacity = Column(Integer)  # Available capacity
    disruption_risk = Column(Float)  # 0.0 to 1.0
    weather_impact = Column(Float)  # Weather impact on route
    traffic_conditions = Column(String(50))  # 'normal', 'heavy', 'light'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_route_segment_date', 'route_id', 'segment_date'),
    )


class RouteOptimization(Base):
    """Route optimization results"""
    __tablename__ = "route_optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String(100), nullable=False, index=True)
    optimization_date = Column(DateTime(timezone=True), nullable=False, index=True)
    optimal_route = Column(JSON)  # Optimal route segments
    total_distance_km = Column(Float, nullable=False)
    total_duration_minutes = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    delay_risk_score = Column(Float, nullable=False)  # 0.0 to 1.0
    savings_estimate = Column(Float)  # Savings vs baseline
    constraint_violations = Column(JSON)  # Any constraint violations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_route_opt_route_date', 'route_id', 'optimization_date'),
    )


# Use Case 6: Hotel Matching AI
class HotelProfile(Base):
    """Hotel attributes and characteristics"""
    __tablename__ = "hotel_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(String(100), unique=True, index=True, nullable=False)
    hotel_name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    location_embedding = Column(JSON)  # Vector embedding of location
    price_range_min = Column(Float, nullable=False)
    price_range_max = Column(Float, nullable=False)
    star_rating = Column(Integer)  # 1-5 stars
    amenities = Column(JSON)  # List of amenities
    hotel_type = Column(String(50))  # 'luxury', 'budget', 'boutique', 'resort'
    guest_rating_avg = Column(Float)  # Average guest rating
    attribute_embeddings = Column(JSON)  # Vector embeddings of all attributes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class HotelMatch(Base):
    """Hotel matching results"""
    __tablename__ = "hotel_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    traveler_id = Column(String(100), nullable=False, index=True)
    match_date = Column(DateTime(timezone=True), nullable=False, index=True)
    matched_hotels = Column(JSON)  # Ranked list of matched hotels
    match_scores = Column(JSON)  # Similarity scores for each hotel
    tradeoff_explanations = Column(JSON)  # Tradeoffs for each match
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    intent_match_score = Column(Float)  # How well hotels match traveler intent
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_hotel_match_traveler_date', 'traveler_id', 'match_date'),
    )

