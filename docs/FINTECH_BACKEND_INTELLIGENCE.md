# Fintech Backend Intelligence Layer

## Overview

The Fintech backend intelligence layer is a boardroom-grade system designed for decision intelligence, not toy demos. It provides explainable AI decisions with mandatory explanation contracts for all API responses.

## Architecture

### Core Principles

1. **Canonical Data Schemas**: Database-level, stable, versioned schemas
2. **Synthetic Data Generation**: Statistically realistic training data with preserved correlations
3. **Scenario Catalogs**: User-driven scenarios that adjust model behavior
4. **Explanation Contracts**: Mandatory explanation objects for all API responses
5. **Model Training**: Models trained offline, APIs perform inference only
6. **No Random Outputs**: All decisions are explainable and contextually dynamic

## Modules

### 1. Credit Risk Intelligence

**Purpose**: Boardroom-grade credit risk assessment with scenario-driven sensitivity analysis.

**Database Schema**:
- `BorrowerProfile`: Borrower demographics and employment
- `CreditHistorySummary`: Credit score, loans, delinquency history
- `FinancialBehavior`: Debt-to-income, utilization, payment patterns
- `MacroEconomicContext`: Regional economic indicators
- `CreditOutcome`: Training labels (not used in production)

**Scenarios**:
- `stable_economy`: Normal economic conditions
- `rising_interest_rates`: Rising rates increase default risk (40% sensitivity increase)
- `economic_downturn`: Recession with high unemployment (100% sensitivity increase)
- `high_inflation`: High inflation erodes purchasing power (60% sensitivity increase)

**API Endpoint**: `POST /api/v1/fintech/credit-risk`

**Request**:
```json
{
  "borrower_id": "BORROWER_123",
  "scenario": "rising_interest_rates",
  "borrower_data": {
    "age": 35,
    "employment_stability_score": 0.7,
    "annual_income": 75000,
    "credit_score_band": "good"
  }
}
```

**Response**:
- `risk_score`: 0.0-1.0 (higher = lower risk)
- `risk_level`: "low", "medium", "high", "very_high"
- `default_probability`: 0.0-1.0
- `loss_given_default_estimate`: 0.0-1.0
- `explanation`: Mandatory explanation object

### 2. Fraud Detection Control Room

**Purpose**: Real-time transaction fraud detection with behavioral pattern analysis.

**Database Schema**:
- `TransactionEvent`: Transaction details (amount, channel, location, timestamp)
- `AccountProfile`: Account history and typical behavior
- `DeviceContext`: Device trust and change frequency
- `BehavioralPattern`: Velocity, geo deviation, consistency scores
- `FraudLabel`: Training labels (not used in production)

**Scenarios**:
- `normal_behavior`: Standard transaction patterns
- `velocity_spike`: Unusual transaction velocity (lower threshold, +20% fraud bias)
- `geo_shift`: Transaction from unusual location (2x geo weight, +30% fraud bias)
- `coordinated_fraud`: Coordinated attack pattern (0.3x velocity threshold, +40% fraud bias)

**API Endpoint**: `POST /api/v1/fintech/fraud-detection`

**Request**:
```json
{
  "transaction_id": "TXN_456",
  "scenario": "geo_shift",
  "transaction_data": {
    "amount": 5000.00,
    "channel_type": "online",
    "geo_location": "BR",
    "account_id": "ACC_789",
    "timestamp": "2024-01-15T14:30:00Z"
  }
}
```

**Response**:
- `fraud_probability`: 0.0-1.0
- `fraud_flag`: boolean
- `fraud_type`: "card_testing", "account_takeover", "identity_theft", etc.
- `risk_level`: "low", "medium", "high", "critical"
- `explanation`: Mandatory explanation object

### 3. KYC / AML Risk Engine

**Purpose**: Customer risk assessment for compliance and regulatory requirements.

**Database Schema**:
- `CustomerIdentity`: Nationality, residency, occupation risk
- `IdentityVerificationSignals`: Document, biometric, name similarity scores
- `JurisdictionRisk`: Country-level AML risk ratings
- `RelationshipNetwork`: Linked entities, high-risk links, complexity
- `ComplianceOutcome`: Training labels (not used in production)

**Scenarios**:
- `low_risk_retail`: Standard retail customer (-20% risk bias)
- `high_risk_jurisdiction`: High-risk jurisdiction (2x jurisdiction risk, +30% bias)
- `pep_profile`: Politically Exposed Person (2x occupation weight, +40% bias)
- `networked_entity`: Complex relationship network (3x network weight, +35% bias)

**API Endpoint**: `POST /api/v1/fintech/kyc-aml`

**Request**:
```json
{
  "customer_id": "CUST_101",
  "scenario": "pep_profile",
  "customer_data": {
    "country_code": "US",
    "occupation_risk_level": "high",
    "network_complexity_score": 0.7
  }
}
```

**Response**:
- `aml_risk_score`: 0.0-1.0
- `aml_risk_level`: "low", "medium", "high", "very_high"
- `escalation_required`: boolean
- `kyc_status`: "approved", "pending_review", "rejected", "escalated"
- `explanation`: Mandatory explanation object

### 4. Market Signal Intelligence

**Purpose**: Market stress and sentiment analysis for trading and risk management.

**Database Schema**:
- `MarketEnvironment`: Volatility, liquidity, macro uncertainty
- `NewsSignal`: Sentiment scores, topic clusters, relevance weights
- `SentimentAggregate`: Rolling sentiment index, divergence scores
- `MarketContextLabel`: Training labels (not used in production)

**Scenarios**:
- `calm_market`: Stable conditions (-20% volatility bias)
- `news_uncertainty`: News-driven uncertainty (+30% volatility, -40% sentiment)
- `liquidity_stress`: Liquidity constraints (+40% volatility, -50% liquidity)
- `macro_shock`: Major macroeconomic shock (+60% volatility, -60% sentiment)

**API Endpoint**: `POST /api/v1/fintech/market-signal`

**Request**:
```json
{
  "market_id": "MARKET_US",
  "scenario": "liquidity_stress",
  "time_horizon_days": 30
}
```

**Response**:
- `market_stress_state`: "calm", "stressed", "volatile"
- `stress_score`: 0.0-1.0
- `sentiment_index`: -1.0 to 1.0
- `volatility_forecast`: 0.0+
- `explanation`: Mandatory explanation object

### 5. Market Regime Simulation Engine

**Purpose**: Regime transition and stress scenario analysis for portfolio risk.

**Database Schema**:
- `MarketTimeSeries`: Return volatility, drawdown, liquidity shifts
- `RegimeState`: Regime labels, confidence, transition probabilities
- `StressScenarioProfile`: Volatility shock, correlation breakdown, liquidity crisis levels

**Scenarios**:
- `volatility_expansion`: Expanding volatility (0.7 shock level, 0.6 transition prob)
- `correlation_breakdown`: Asset correlation breakdown (0.8 breakdown score, 0.7 transition prob)
- `liquidity_freeze`: Severe liquidity crisis (0.9 crisis level, 0.8 transition prob)

**API Endpoint**: `POST /api/v1/fintech/regime-simulation`

**Request**:
```json
{
  "market_id": "MARKET_US",
  "scenario": "correlation_breakdown",
  "simulation_horizon_days": 90,
  "stress_level": 0.75
}
```

**Response**:
- `current_regime`: "bull", "bear", "volatile", "calm", "stress"
- `regime_confidence`: 0.0-1.0
- `projected_regime`: Projected regime label
- `transition_probability`: 0.0-1.0
- `stress_indicators`: Dict of stress metrics
- `explanation`: Mandatory explanation object

## Explanation Contract

Every API response includes a mandatory `ExplanationObject` with:

1. **decision_summary**: Human-readable decision summary
2. **confidence_score**: 0.0-1.0 confidence in decision
3. **top_contributing_factors**: Ranked list of top 5 factors with:
   - `factor_name`: Name of factor
   - `impact_score`: 0.0-1.0 impact weight
   - `direction`: "increases" or "decreases" risk/score
   - `explanation`: Human-readable explanation
4. **sensitivity_analysis**: Parameter sensitivity analysis
5. **scenario_impact**: Impact of selected scenario on decision
6. **uncertainty_notes**: Notes on uncertainty and limitations
7. **human_review_recommended**: Boolean flag for human review
8. **model_version**: Model version used
9. **inference_timestamp**: Timestamp of inference

## Synthetic Data Generation

Synthetic data generators produce statistically realistic data with:

- **Preserved Correlations**: Features maintain realistic relationships
- **Preserved Rarity**: Fraud/defaults are rare (1-10% base rates)
- **Preserved Nonlinear Risk Spikes**: Risk increases non-linearly
- **Preserved Regime Shifts**: Market regimes transition realistically

Data is used only for training, never shown raw to users.

## Model Training

- Models are trained offline on synthetic data
- Models are never retrained per request
- APIs perform inference only
- Predictions are ephemeral, not stored as truth
- Explainability layer runs after inference

## Design Constraints

- ✅ No random outputs
- ✅ No magic confidence numbers
- ✅ No black-box decisions
- ✅ No UI-dependent logic
- ✅ No regulatory claims
- ✅ Always explainable
- ✅ Always scenario-driven
- ✅ Always contextually dynamic

## Usage Examples

### Credit Risk Assessment

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/fintech/credit-risk",
    json={
        "borrower_id": "BORROWER_123",
        "scenario": "rising_interest_rates",
        "borrower_data": {
            "age": 35,
            "employment_stability_score": 0.7,
            "annual_income": 75000,
            "credit_score_band": "good",
            "debt_to_income_ratio": 0.35
        }
    }
)

result = response.json()
print(f"Risk Score: {result['risk_score']:.2f}")
print(f"Risk Level: {result['risk_level']}")
print(f"Default Probability: {result['default_probability']:.2%}")
print(f"Decision: {result['explanation']['decision_summary']}")
print(f"Top Factor: {result['explanation']['top_contributing_factors'][0]['factor_name']}")
```

### Fraud Detection

```python
response = requests.post(
    "http://localhost:8000/api/v1/fintech/fraud-detection",
    json={
        "transaction_id": "TXN_456",
        "scenario": "velocity_spike",
        "transaction_data": {
            "amount": 5000.00,
            "channel_type": "online",
            "geo_location": "BR",
            "account_id": "ACC_789",
            "timestamp": "2024-01-15T14:30:00Z"
        }
    }
)

result = response.json()
print(f"Fraud Probability: {result['fraud_probability']:.2%}")
print(f"Fraud Flag: {result['fraud_flag']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendation: {result['recommendation']}")
```

## Database Migration

To create the Fintech tables, run:

```bash
alembic revision --autogenerate -m "Add fintech tables"
alembic upgrade head
```

## Testing

All endpoints can be tested via:

1. **Swagger UI**: `http://localhost:8000/docs`
2. **ReDoc**: `http://localhost:8000/redoc`
3. **Direct API calls**: Use the examples above

## Future Enhancements

- Real ML model integration (currently uses RandomForest)
- RAG over medical/financial literature
- MCP-powered AI tools
- Multi-industry orchestration pattern
- Real-time streaming updates
- Advanced ensemble methods

## Success Metric

The backend should make the UI feel:
- **Alive**: Dynamic, contextually responsive
- **Intelligent**: Explainable, not random
- **Explainable**: Every decision has reasoning
- **Different every time**: Scenario-driven variability

Not random — contextually dynamic.

