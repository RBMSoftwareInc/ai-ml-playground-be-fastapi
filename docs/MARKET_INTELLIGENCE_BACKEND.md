# Market & Digital Asset Intelligence Backend

## Overview

The Market & Digital Asset Intelligence backend is a signal-based, explainable market behavior intelligence system. It provides decision-support intelligence, not trading recommendations or predictions.

## Core Design Principles

1. **Signal, not prediction**: Focus on identifying signals and patterns, not exact price forecasts
2. **Confidence & uncertainty first**: Every output includes confidence assessment and uncertainty factors
3. **Explainability is mandatory**: All APIs return plain English explanations with no jargon
4. **Historical analogy over raw forecasting**: Emphasize similar historical periods over pure predictions
5. **Every output must be traceable to data**: All signals must be explainable from underlying data

## Modules

### 1. Commodity Trend Intelligence

**Purpose**: Signal-based trend analysis for commodities (gold, silver, oil, etc.)

**Database Schema**:
- `CommodityMarketData`: OHLC price data, volume, volatility, macro proxies
- `CommodityTrendSignal`: Directional bias, confidence bands, trend strength

**API Endpoint**: `POST /api/v1/market-intelligence/commodity-trend`

**Request**:
```json
{
  "asset_id": "gold",
  "lookback_days": 90,
  "scenario": "baseline"
}
```

**Response**:
- `directional_bias`: "up", "down", or "sideways"
- `confidence_band_lower` / `confidence_band_upper`: Confidence range
- `trend_strength`: 0.0 to 1.0
- `volatility_estimate`: Volatility measure
- `similar_periods`: Top 3 historical analogs
- `explanation`: Mandatory explanation object

### 2. Market Regime Signals

**Purpose**: Identify current market regime and transition probabilities

**Database Schema**:
- `MarketRegimeFeature`: Derived features (volatility, trend, drawdown, liquidity)
- `MarketRegimeState`: Regime labels (soft, not hard), stability, transition probabilities

**API Endpoint**: `POST /api/v1/market-intelligence/market-regime`

**Request**:
```json
{
  "market_id": "MARKET_US",
  "lookback_days": 90,
  "scenario": "volatility_spike"
}
```

**Response**:
- `current_regime`: "calm", "volatile", "stress", "recovery"
- `regime_probability`: 0.0 to 1.0 (soft label probability)
- `stability_score`: 0.0 to 1.0
- `transition_probability`: 0.0 to 1.0
- `transition_likelihoods`: Probabilities to other regimes
- `explanation`: Mandatory explanation object

### 3. Digital Asset Adoption Intelligence

**Purpose**: Analyze digital asset adoption phases and momentum by country/region

**Database Schema**:
- `DigitalAssetAdoptionData`: Wallet activity, transaction volume, exchange activity, regulatory signals
- `DigitalAssetAdoptionSignal`: Adoption phase, momentum, growth rate, acceleration

**API Endpoint**: `POST /api/v1/market-intelligence/digital-asset-adoption`

**Request**:
```json
{
  "country_code": "US",
  "lookback_days": 180,
  "scenario": "baseline"
}
```

**Response**:
- `adoption_phase`: "early", "growth", "maturation", "saturation"
- `momentum_score`: -1.0 to 1.0
- `growth_rate`: Percentage growth rate
- `acceleration_indicator`: -1.0 to 1.0
- `explanation`: Mandatory explanation object

### 4. Exchange & Market Risk Mapping

**Purpose**: Map risk concentration and dependency hotspots across exchanges

**Database Schema**:
- `ExchangeProfile`: Exchange characteristics (asset coverage, volume concentration, liquidity)
- `ExchangeRiskSignal`: Risk concentration, dependency hotspots, systemic exposure

**API Endpoint**: `POST /api/v1/market-intelligence/exchange-risk`

**Request**:
```json
{
  "exchange_id": "EXCHANGE_1",
  "scenario": "liquidity_drop"
}
```

**Response**:
- `risk_concentration_score`: 0.0 to 1.0
- `dependency_hotspots`: List of high-dependency relationships
- `systemic_exposure_indicator`: 0.0 to 1.0
- `stress_propagation_risk`: 0.0 to 1.0
- `explanation`: Mandatory explanation object

## Explanation Contract (Mandatory)

Every API response includes a `MarketIntelligenceExplanation` object with:

```json
{
  "signal_summary": {
    "signal_type": "commodity_trend",
    "signal_direction": "up",
    "signal_strength": 0.75,
    "time_horizon": "30-90 days"
  },
  "confidence": {
    "confidence_level": "high",
    "confidence_score": 0.85,
    "confidence_reason": "Strong historical patterns...",
    "data_quality": "high"
  },
  "key_drivers": [
    {
      "driver_name": "Market Volatility",
      "impact_direction": "positive",
      "impact_magnitude": 0.3,
      "explanation": "Elevated volatility indicates..."
    }
  ],
  "historical_analogs": [
    {
      "period_start": "2020-03-01",
      "period_end": "2020-06-30",
      "similarity_score": 0.75,
      "outcome_summary": "Similar volatility pattern..."
    }
  ],
  "uncertainty_factors": [
    {
      "factor_name": "High Volatility",
      "uncertainty_level": "high",
      "explanation": "Elevated volatility makes..."
    }
  ],
  "what_this_means": "Plain English explanation with no jargon, no model names, no equations"
}
```

## Scenario Simulation

The system supports scenario simulation with controlled perturbations:

### Available Scenarios

- `baseline`: Normal market conditions
- `volatility_spike`: 2.5x volatility, reduced liquidity
- `demand_shock`: 30% demand increase, elevated volatility
- `liquidity_drop`: 50% liquidity reduction, increased volatility
- `stress_scenario`: Combined stress (3x volatility, 20% demand decrease, 40% liquidity)

### Scenario Application

Scenarios are applied to feature vectors before inference:
- Volatility multipliers affect volatility features
- Demand shocks affect price/growth features
- Liquidity multipliers affect liquidity features

## Synthetic Data Generation

All modules use synthetic data generators that:
- Preserve real-world distributions
- Preserve correlations
- Allow regime switching
- Support stress scenarios

Data is used for:
- Model training
- Demo stability
- Reproducibility
- Safety (no real market data exposure)

## Modeling Approach

### Commodity Trend Intelligence
- **Ensemble logic**: Time-series trend extractor + volatility estimator + pattern similarity matcher
- **Output**: Directional bias, confidence bands, historical analogs

### Market Regime Signals
- **Regime clustering**: Unsupervised clustering for regime identification
- **Transition probability**: Estimation of regime change likelihood
- **Output**: Soft regime labels, stability scores, transition probabilities

### Digital Asset Adoption Intelligence
- **Index modeling**: Adoption index construction
- **Trend decomposition**: Growth vs saturation analysis
- **Output**: Adoption phase, momentum, acceleration indicators

### Exchange Risk Mapping
- **Network graph modeling**: Dependency relationship analysis
- **Concentration metrics**: Risk concentration calculation
- **Output**: Risk scores, dependency hotspots, systemic exposure

## Training & Retraining Strategy

- **Offline batch training**: Models trained on synthetic + real data
- **Periodic retraining**: Scheduled retraining with updated data
- **Version control**: Every model versioned and stored
- **Feature distributions**: Stored per version for consistency
- **No online learning**: No continuous online learning (for now)

## API Design

### Input Requirements
- **Structured inputs only**: No free text accepted
- **Scenario parameters**: Optional scenario selection
- **Lookback periods**: Configurable historical data windows

### Output Structure
- **Structured intelligence**: Signal data + explanation
- **Decision-support**: Not execution recommendations
- **Explainable**: Every output includes plain English explanation

## Usage Examples

### Commodity Trend Analysis

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/market-intelligence/commodity-trend",
    json={
        "asset_id": "gold",
        "lookback_days": 90,
        "scenario": "volatility_spike"
    }
)

result = response.json()
print(f"Direction: {result['directional_bias']}")
print(f"Trend Strength: {result['trend_strength']:.2f}")
print(f"What This Means: {result['explanation']['what_this_means']}")
```

### Market Regime Analysis

```python
response = requests.post(
    "http://localhost:8000/api/v1/market-intelligence/market-regime",
    json={
        "market_id": "MARKET_US",
        "lookback_days": 90,
        "scenario": "baseline"
    }
)

result = response.json()
print(f"Current Regime: {result['current_regime']}")
print(f"Stability: {result['stability_score']:.2f}")
print(f"Transition Probability: {result['transition_probability']:.2f}")
```

## Design Philosophy

This backend is designed to feel:
- **Calm**: Conservative, measured approach
- **Intelligent**: Explainable, defensible signals
- **Serious**: Boardroom-grade, not toy-like
- **Trustworthy**: Every output traceable to data

## Success Metrics

After implementing this backend:
- ✅ UI teams can build rich walkthroughs
- ✅ Stakeholders can trust outputs
- ✅ Demos feel real, not toy-like
- ✅ Models are explainable and defensible
- ✅ Every signal has a clear explanation

