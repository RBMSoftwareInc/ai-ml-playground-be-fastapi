# Travel AI Backend Implementation

## Overview

Travel AI backend provides decision-intelligence APIs for travel operations, pricing, and personalization. This is a boardroom-grade demo system, not a booking engine or toy demo.

## Architecture

### 3 Pillars, 6 Use Cases

**Pillar 1: Pricing & Revenue Intelligence**
- Use Case 1: Dynamic Pricing Engine
- Use Case 2: Demand Forecasting

**Pillar 2: Personalized Travel Intelligence**
- Use Case 3: Personalized Recommendations
- Use Case 4: AI Concierge

**Pillar 3: Operational Intelligence**
- Use Case 5: Route Optimization
- Use Case 6: Hotel Matching AI

## API Endpoints

All endpoints are under `/api/v1/travel`:

1. `POST /dynamic-pricing` - Dynamic pricing engine
2. `POST /demand-forecast` - Demand forecasting
3. `POST /personalized-recommendations` - Personalized recommendations
4. `POST /ai-concierge` - AI concierge assistant
5. `POST /route-optimization` - Route optimization
6. `POST /hotel-matching` - Hotel matching AI
7. `GET /scenarios` - Get available scenarios for all modules

## Data Models

### Pricing & Revenue Intelligence

- `PricingEvent` - Historical pricing events and demand signals
- `PricingRecommendation` - Dynamic pricing recommendations
- `BookingHistory` - Historical booking patterns
- `DemandForecast` - Demand forecasting predictions

### Personalized Travel Intelligence

- `TravelerProfile` - Traveler preferences and behavior
- `TravelerIntent` - Traveler intent signals
- `RecommendationResult` - Personalized recommendation results
- `ConversationContext` - AI Concierge conversation context

### Operational Intelligence

- `RouteSegment` - Route segments and connections
- `RouteOptimization` - Route optimization results
- `HotelProfile` - Hotel attributes and characteristics
- `HotelMatch` - Hotel matching results

## ML Models

### Use Case 1: Dynamic Pricing
- **Model**: `RandomForestRegressor`
- **Training**: 5,000 synthetic pricing events
- **Features**: Demand level, booking velocity, seasonality, event impact, lead time, occupancy, competitor price ratio
- **Output**: Optimal price range (min, max, optimal)

### Use Case 2: Demand Forecasting
- **Model**: `RandomForestRegressor`
- **Training**: 3,000 synthetic booking history entries
- **Features**: Lead time, season, holiday flag, event flag, weather impact
- **Output**: Forecasted demand with confidence bands

### Use Case 3: Personalized Recommendations
- **Approach**: Embedding-based similarity (no traditional ML model)
- **Data**: Traveler profiles, preferences, intent signals
- **Output**: Ranked recommendations with match scores

### Use Case 4: AI Concierge
- **Approach**: NLP/LLM-based (no traditional ML model)
- **Data**: Conversation context, travel state, intent
- **Output**: Response message, suggested actions, escalation flags

### Use Case 5: Route Optimization
- **Model**: `RandomForestRegressor` (for delay risk)
- **Training**: 2,000 synthetic route segments
- **Features**: Distance, disruption risk, weather impact, traffic conditions
- **Output**: Optimal route with delay risk score

### Use Case 6: Hotel Matching
- **Approach**: Embedding-based similarity (no traditional ML model)
- **Data**: Hotel profiles, traveler preferences
- **Output**: Ranked hotel matches with tradeoff explanations

## Explanation Contract

Every API response includes a mandatory `TravelExplanation` object with:

- `decision_summary` - Plain English decision summary
- `confidence` - Confidence assessment (level, score, reason, data quality)
- `key_drivers` - Top 3-5 key drivers of the decision
- `uncertainty_factors` - Factors contributing to uncertainty
- `what_this_means` - Plain English explanation
- `time_savings` - Time savings vs conventional approach

**Rules**:
- No ML jargon
- No model names
- No equations
- Plain English only

## Scenarios

### Dynamic Pricing Scenarios
- `baseline` - Normal market conditions
- `peak_season` - High-demand peak travel season
- `low_season` - Low-demand off-peak season
- `event_surge` - Major event causing demand spike
- `last_minute` - Short lead time with high urgency

### Demand Forecasting Scenarios
- `baseline` - Standard demand forecast
- `holiday_boost` - Upcoming holiday period
- `event_boost` - Special event in the area
- `economic_downturn` - Economic conditions reducing demand
- `seasonal_transition` - Transition between peak and off-peak

### Route Optimization Scenarios
- `baseline` - Normal traffic and weather conditions
- `heavy_traffic` - Heavy traffic conditions expected
- `weather_disruption` - Adverse weather conditions
- `peak_travel` - High-traffic peak travel period
- `optimal_conditions` - Ideal travel conditions

## Synthetic Data Generation

All training data is generated using `TravelDataGenerator`:

- **Statistically realistic** - Preserves real-world distributions
- **Preserves correlations** - Maintains relationships between features
- **Seasonality** - Models seasonal patterns
- **Edge cases** - Includes rare but realistic scenarios
- **Reproducible** - Uses seed for consistency

## Training Strategy

- **Offline training** - Models trained during service initialization
- **Synthetic data** - All training data is synthetic (no real customer data)
- **Inference only** - APIs perform inference, not training
- **Model persistence** - Models can be saved to `trained_models/` (future enhancement)

## Example Requests

### Dynamic Pricing
```json
{
  "property_id": "HOTEL_123",
  "target_date": "2024-06-15T00:00:00Z",
  "current_price": 150.0,
  "lead_time_days": 30,
  "scenario": "peak_season"
}
```

### Demand Forecasting
```json
{
  "property_id": "HOTEL_123",
  "forecast_horizon_days": 90,
  "scenario": "holiday_boost"
}
```

### Personalized Recommendations
```json
{
  "traveler_id": "TRAVELER_456",
  "destination": "Paris",
  "travel_date": "2024-07-01T00:00:00Z",
  "duration_days": 7,
  "budget": 2000.0,
  "travel_style": "luxury"
}
```

### AI Concierge
```json
{
  "traveler_id": "TRAVELER_456",
  "message": "I need help planning my trip to Paris",
  "travel_state": "planning"
}
```

### Route Optimization
```json
{
  "origin": "New York",
  "destination": "Los Angeles",
  "travel_date": "2024-06-15T00:00:00Z",
  "scenario": "baseline"
}
```

### Hotel Matching
```json
{
  "traveler_id": "TRAVELER_456",
  "destination": "Paris",
  "check_in_date": "2024-07-01T00:00:00Z",
  "check_out_date": "2024-07-08T00:00:00Z",
  "budget": 2000.0
}
```

## Response Structure

All responses follow this structure:

```json
{
  "success": true,
  "...": "...",  // Use-case specific fields
  "explanation": {
    "decision_summary": "...",
    "confidence": {
      "confidence_level": "high|medium|low",
      "confidence_score": 0.0-1.0,
      "confidence_reason": "...",
      "data_quality": "high|medium|low"
    },
    "key_drivers": [...],
    "uncertainty_factors": [...],
    "what_this_means": "...",
    "time_savings": "...",
    "model_version": "1.0.0",
    "inference_timestamp": "..."
  },
  "scenario_applied": "...",
  "metadata": {...}
}
```

## Design Principles

1. **Decision Intelligence** - Focus on decision support, not execution
2. **Explainability** - Every decision must be explainable in plain English
3. **Scenario-Driven** - Users select scenarios, not raw data
4. **Synthetic Data** - All training data is synthetic (safety & privacy)
5. **No Overclaiming** - Honest about limitations and uncertainty
6. **Time Savings** - Emphasize time savings vs conventional approaches

## Future Enhancements

1. **Model Persistence** - Save models to disk (like Healthcare)
2. **Real Embeddings** - Use actual embedding models for recommendations/matching
3. **LLM Integration** - Integrate real LLM for AI Concierge
4. **Graph Algorithms** - Use proper graph algorithms for route optimization
5. **Model Versioning** - Track model versions and performance
6. **A/B Testing** - Support multiple model versions for comparison

## Files Structure

```
app/
├── models/
│   └── travel.py              # Database models
├── schemas/
│   └── travel.py              # Pydantic schemas
├── services/
│   ├── travel_data_generator.py      # Synthetic data generation
│   ├── travel_ml_service.py          # ML models and inference
│   ├── travel_explanation_engine.py  # Explanation generation
│   └── travel_scenarios.py           # Scenario catalog
└── api/
    └── v1/
        └── travel.py          # API endpoints
```

## Testing

To test the implementation:

```bash
# Start the server
uvicorn app.main:app --reload

# Test dynamic pricing
curl -X POST "http://localhost:5000/api/v1/travel/dynamic-pricing" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "HOTEL_123",
    "target_date": "2024-06-15T00:00:00Z",
    "current_price": 150.0,
    "scenario": "peak_season"
  }'
```

## Notes

- All models are trained on synthetic data during service initialization
- Models are not persisted to disk yet (future enhancement)
- Embedding-based use cases (recommendations, hotel matching) use simplified similarity (would use real embeddings in production)
- AI Concierge uses simplified response generation (would use LLM in production)
- Route optimization uses simplified route generation (would use graph algorithms in production)

