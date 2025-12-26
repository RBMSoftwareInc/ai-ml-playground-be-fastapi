# ML Models Matrix: Use Cases to AI/ML Models Mapping

## Overview

This document provides a comprehensive matrix of all use cases in Healthcare and Fintech industries, mapping them to the AI/ML models used, training basis, and data sources.

## Model Training Strategy

### Current Implementation

**Training Approach**: Models are trained **on-the-fly** during service initialization using synthetic data generators.

**Training Data Source**: 
- **Synthetic data generators** create statistically realistic training data
- Data preserves real-world distributions, correlations, and edge cases
- No real patient/financial data is used (safety & privacy)

**Model Storage**:
- **Location**: `./trained_models/` directory (configurable via `MODELS_DIR` in settings)
- **Format**: Pickle files (`.pkl`)
- **Purpose**: 
  - Persist trained models across application restarts
  - Avoid re-training on every startup
  - Enable model versioning (future)

**Training Flow**:
1. Service initialization (`__init__`)
2. Check if pre-trained model exists in `trained_models/` folder
3. If exists → Load model from disk
4. If not exists → Train model on synthetic data → Save to disk
5. Models ready for inference

**Test Data Flow**:
- **No separate test data**: Models are trained and immediately used for inference
- **Inference data**: Comes from API requests (user input)
- **Synthetic training data**: Generated during model initialization, not stored

---

## Healthcare Industry: Use Cases → Models Matrix

| Use Case | Endpoint | ML Model Used | Model Type | Training Basis | Features | Training Data Source |
|----------|----------|---------------|------------|----------------|----------|---------------------|
| **Risk Scoring** | `POST /api/v1/healthcare/risk-scoring` | `RandomForestRegressor` | Regression | Synthetic patient data (1000 samples) | 7 features: BP systolic/diastolic, heart rate, temperature, history count, medication count, lab abnormal count | `HealthcareMLService._create_default_model()` - Synthetic data generator |
| **Diagnostic AI** | `POST /api/v1/healthcare/diagnostic-ai` | **No ML Model** (Simulated) | Simulation | N/A | Image features (would use CNN in production) | Placeholder - would use medical imaging datasets (e.g., ChestX-ray14, MIMIC) |
| **Drug Discovery** | `POST /api/v1/healthcare/drug-discovery` | **No ML Model** (Simulation Engine) | Simulation | Rule-based scoring | Molecular features, QSAR-style logic | Synthetic molecular data generator |
| **Clinical Trials** | `POST /api/v1/healthcare/clinical-trials` | **No ML Model** | Rule-based | N/A | Trial criteria matching | N/A - Rule-based matching |
| **Patient Flow** | `POST /api/v1/healthcare/patient-flow` | **No ML Model** | Rule-based | N/A | Patient data, department capacity | N/A - Rule-based optimization |
| **Resource Allocation** | `POST /api/v1/healthcare/resource-allocation` | **No ML Model** | Rule-based | N/A | Resource data, demand predictions | N/A - Rule-based optimization |
| **Health Report Analysis** | `POST /api/v1/healthcare/health-report-analysis` | **No ML Model** | NLP (spaCy) | Pre-trained spaCy model | Text extraction, entity recognition | Pre-trained spaCy `en_core_web_sm` model |
| **Medical Imaging Analysis** | `POST /api/v1/healthcare/diagnostic-ai` (with images) | **No ML Model** (Simulated) | Simulation | N/A | Image features (would use CNN) | Placeholder - would use medical imaging datasets |

**Healthcare ML Model Summary**:
- ✅ **1 use case uses ML model**: Risk Scoring (`RandomForestRegressor`)
- ❌ **7 use cases use rule-based/simulation**: No ML models

---

## Fintech Industry: Use Cases → Models Matrix

### Original Fintech Modules (5)

| Use Case | Endpoint | ML Model Used | Model Type | Training Basis | Features | Training Data Source |
|----------|----------|---------------|------------|----------------|----------|---------------------|
| **Credit Risk Intelligence** | `POST /api/v1/fintech/credit-risk` | `RandomForestRegressor` | Regression | Synthetic borrower data (10,000 samples) | 12 features: Age, employment stability, income, credit history, financial behavior | `FintechMLService._train_credit_risk_model()` - `FintechDataGenerator` |
| **Fraud Detection** | `POST /api/v1/fintech/fraud-detection` | `RandomForestClassifier` | Classification | Synthetic transaction data (50,000 samples) | 6 features: Amount, channel, geo deviation, hour, account age, amount deviation | `FintechMLService._train_fraud_detection_model()` - `FintechDataGenerator` |
| **KYC / AML Risk Engine** | `POST /api/v1/fintech/kyc-aml` | `RandomForestClassifier` | Classification | Synthetic customer data (5,000 samples) | 8 features: Jurisdiction, occupation, identity verification, network complexity | `FintechMLService._train_kyc_aml_model()` - `FintechDataGenerator` |
| **Market Signal Intelligence** | `POST /api/v1/fintech/market-signal` | `RandomForestRegressor` | Regression | Synthetic market time series (300 samples) | 4 features: Volatility, trend, drawdown, liquidity | `FintechMLService._train_market_signal_model()` - `FintechDataGenerator` |
| **Market Regime Simulation** | `POST /api/v1/fintech/regime-simulation` | `RandomForestClassifier` | Classification | Synthetic market time series (300 samples) | 4 features: Volatility, trend, drawdown, liquidity | `FintechMLService._train_regime_simulation_model()` - `FintechDataGenerator` |

### Market & Digital Asset Intelligence Modules (4)

| Use Case | Endpoint | ML Model Used | Model Type | Training Basis | Features | Training Data Source |
|----------|----------|---------------|------------|----------------|----------|---------------------|
| **Commodity Trend Intelligence** | `POST /api/v1/fintech/commodity-trend` | `RandomForestClassifier` + `RandomForestRegressor` | Classification + Regression | Synthetic commodity data (5,000 samples) | 5 features: Returns, volatility, momentum, price change | `MarketIntelligenceMLService._train_commodity_trend_model()` - `MarketIntelligenceDataGenerator` |
| **Market Regime Intelligence** | `POST /api/v1/fintech/market-regime-intelligence` | `RandomForestClassifier` | Classification | Synthetic regime features (3,000 samples) | 4 features: Volatility, trend strength, drawdown, liquidity | `MarketIntelligenceMLService._train_market_regime_model()` - `MarketIntelligenceDataGenerator` |
| **Digital Asset Adoption** | `POST /api/v1/fintech/digital-asset-adoption` | `RandomForestClassifier` + `RandomForestRegressor` | Classification + Regression | Synthetic adoption data (2,000 samples) | 5 features: Wallet activity, transaction volume, exchange activity, regulatory signals, growth rate | `MarketIntelligenceMLService._train_digital_asset_adoption_model()` - `MarketIntelligenceDataGenerator` |
| **Exchange Risk Mapping** | `POST /api/v1/fintech/exchange-risk` | `RandomForestRegressor` | Regression | Synthetic exchange profiles (1,000 samples) | 6 features: Asset coverage, volume concentration, liquidity, dependencies | `MarketIntelligenceMLService._train_exchange_risk_model()` - `MarketIntelligenceDataGenerator` |

**Fintech ML Model Summary**:
- ✅ **9 use cases use ML models**: All use `RandomForest` variants (Classifier/Regressor)
- ✅ **All models trained on synthetic data**: Generated by data generators

---

## Model Training Details

### Healthcare Models

#### Risk Scoring Model
- **Model**: `RandomForestRegressor`
- **Training Samples**: 1,000 synthetic patients
- **Features**: 7 (BP, heart rate, temperature, history, medications, labs)
- **Target**: Risk score (0.0 to 1.0)
- **Training Method**: `_create_default_model()` in `HealthcareMLService`
- **Storage**: `trained_models/healthcare_risk_model.pkl`
- **Scaler**: `StandardScaler` (fitted during training)

### Fintech Models

#### Credit Risk Model
- **Model**: `RandomForestRegressor`
- **Training Samples**: 10,000 synthetic borrowers
- **Features**: 12 (age, employment, income, credit history, financial behavior)
- **Target**: Default probability (0.0 to 1.0)
- **Training Method**: `_train_credit_risk_model()` in `FintechMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)
- **Scaler**: `StandardScaler` per model

#### Fraud Detection Model
- **Model**: `RandomForestClassifier` (with class_weight="balanced")
- **Training Samples**: 50,000 synthetic transactions
- **Features**: 6 (amount, channel, geo, time, account age, deviation)
- **Target**: Fraud flag (binary)
- **Training Method**: `_train_fraud_detection_model()` in `FintechMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

#### KYC/AML Model
- **Model**: `RandomForestClassifier` (with class_weight="balanced")
- **Training Samples**: 5,000 synthetic customers
- **Features**: 8 (jurisdiction, occupation, identity verification, network)
- **Target**: AML risk level (0=low, 1=medium, 2=high, 3=very_high)
- **Training Method**: `_train_kyc_aml_model()` in `FintechMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

#### Market Signal Model
- **Model**: `RandomForestRegressor`
- **Training Samples**: 300 synthetic market time series points
- **Features**: 4 (volatility, trend, drawdown, liquidity)
- **Target**: Stress state (0=calm, 1=stressed, 2=volatile)
- **Training Method**: `_train_market_signal_model()` in `FintechMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

#### Regime Simulation Model
- **Model**: `RandomForestClassifier`
- **Training Samples**: 300 synthetic market time series points
- **Features**: 4 (volatility, trend, drawdown, liquidity)
- **Target**: Regime label (calm, volatile, stress)
- **Training Method**: `_train_regime_simulation_model()` in `FintechMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

### Market Intelligence Models

#### Commodity Trend Model
- **Model**: `RandomForestClassifier` (direction) + `RandomForestRegressor` (strength)
- **Training Samples**: 5,000 synthetic commodity data points
- **Features**: 5 (returns, volatility, momentum, price change)
- **Target**: Direction (up/down/sideways) + Trend strength (0.0 to 1.0)
- **Training Method**: `_train_commodity_trend_model()` in `MarketIntelligenceMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

#### Market Regime Intelligence Model
- **Model**: `RandomForestClassifier`
- **Training Samples**: 3,000 synthetic regime features
- **Features**: 4 (volatility, trend, drawdown, liquidity)
- **Target**: Regime label (calm, volatile, stress, recovery)
- **Training Method**: `_train_market_regime_model()` in `MarketIntelligenceMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

#### Digital Asset Adoption Model
- **Model**: `RandomForestClassifier` (phase) + `RandomForestRegressor` (momentum)
- **Training Samples**: 2,000 synthetic adoption data points
- **Features**: 5 (wallet, transaction, exchange, regulatory, growth rate)
- **Target**: Adoption phase + Momentum score
- **Training Method**: `_train_digital_asset_adoption_model()` in `MarketIntelligenceMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

#### Exchange Risk Model
- **Model**: `RandomForestRegressor`
- **Training Samples**: 1,000 synthetic exchange profiles
- **Features**: 6 (asset coverage, volume concentration, liquidity, dependencies)
- **Target**: Risk concentration score (0.0 to 1.0)
- **Training Method**: `_train_exchange_risk_model()` in `MarketIntelligenceMLService`
- **Storage**: **Not saved** (trained on-the-fly, in-memory only)

---

## Training Data Flow

### Current Implementation

```
┌─────────────────────────────────────────────────────────┐
│ Service Initialization (__init__)                       │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Check: Does trained model exist in trained_models/ ?    │
└─────────────────────────────────────────────────────────┘
         │                          │
    YES │                          │ NO
         │                          │
         ▼                          ▼
┌──────────────────┐    ┌──────────────────────────────────┐
│ Load from disk   │    │ Generate Synthetic Training Data│
│ (pickle.load)    │    │ (Data Generator)                │
└──────────────────┘    └──────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────────┐
                    │ Train Model              │
                    │ (RandomForest.fit)       │
                    └───────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────────┐
                    │ Save Model to Disk        │
                    │ (pickle.dump)             │
                    │ trained_models/*.pkl      │
                    └───────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────────┐
                    │ Model Ready for Inference │
                    └───────────────────────────┘
```

### Test Data Flow (Inference)

```
┌─────────────────────────────────────────────────────────┐
│ API Request (User Input)                                │
│ POST /api/v1/healthcare/risk-scoring                    │
│ POST /api/v1/fintech/credit-risk                        │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Extract Features from Request                           │
│ (vitals, lab_results, borrower_data, etc.)               │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Transform Features                                       │
│ (StandardScaler.transform)                              │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Model Inference                                          │
│ (model.predict or model.predict_proba)                  │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Generate Explanation                                    │
│ (Explanation Engine)                                    │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Return Response with Prediction + Explanation            │
└─────────────────────────────────────────────────────────┘
```

---

## Trained Models Folder Purpose

### Location
- **Path**: `./trained_models/` (configurable via `MODELS_DIR` in `app/core/config.py`)
- **Default**: `./trained_models/`

### Purpose

1. **Model Persistence**: 
   - Save trained models to disk to avoid re-training on every application restart
   - Models are expensive to train (takes time and computation)

2. **Model Versioning** (Future):
   - Store multiple model versions
   - Track model performance over time
   - Enable A/B testing of models

3. **Production Deployment**:
   - Pre-trained models can be included in deployment packages
   - Models trained offline can be loaded in production
   - No training required in production environment

4. **Model Sharing**:
   - Models can be shared across environments (dev, staging, prod)
   - Models can be version controlled (with Git LFS for large files)

### Current Status

**Healthcare**:
- ✅ **Saves model**: `healthcare_risk_model.pkl` is saved to `trained_models/`
- ✅ **Loads model**: Checks for existing model on startup

**Fintech**:
- ❌ **Does NOT save models**: All models trained on-the-fly, in-memory only
- ❌ **Re-trains on every restart**: Models are recreated each time

**Market Intelligence**:
- ❌ **Does NOT save models**: All models trained on-the-fly, in-memory only
- ❌ **Re-trains on every restart**: Models are recreated each time

### Recommended Improvement

All Fintech and Market Intelligence models should follow the Healthcare pattern:
1. Check for saved model in `trained_models/`
2. If exists → Load
3. If not → Train → Save

---

## Model Usage Summary

### Healthcare (8 use cases)
- **ML Models**: 1 use case (Risk Scoring)
- **Rule-based/Simulation**: 7 use cases
- **Total ML Models**: 1

### Fintech (9 use cases)
- **ML Models**: 9 use cases (ALL use ML models)
- **Model Types**: RandomForest (Classifier/Regressor)
- **Total ML Models**: 9

### Grand Total
- **Total Use Cases**: 17
- **Use Cases with ML Models**: 10
- **Use Cases without ML Models**: 7

---

## Model Training Basis

### Synthetic Data Generators

All ML models are trained on **synthetic data** generated by:

1. **Healthcare**: `HealthcareMLService._create_default_model()`
   - Generates 1,000 synthetic patient records
   - Features: Vitals, lab results, medical history

2. **Fintech**: `FintechDataGenerator`
   - Generates borrower profiles, credit history, financial behavior
   - Generates transaction events, account profiles
   - Generates customer identities, relationship networks
   - Generates market time series

3. **Market Intelligence**: `MarketIntelligenceDataGenerator`
   - Generates commodity market data
   - Generates market regime features
   - Generates digital asset adoption data
   - Generates exchange profiles

### Why Synthetic Data?

1. **Safety**: No real patient/financial data exposure
2. **Privacy**: No HIPAA/PCI compliance concerns
3. **Reproducibility**: Same seed = same data = same models
4. **Demo Stability**: Consistent behavior for demos
5. **Controlled Scenarios**: Can generate edge cases and stress scenarios

### Real Data (Future)

In production, models would be trained on:
- **Healthcare**: Real (anonymized) patient data, medical imaging datasets
- **Fintech**: Real (anonymized) transaction data, credit bureau data
- **Market Intelligence**: Real market data, exchange data

---

## Model Storage Structure (Current)

```
trained_models/
├── healthcare_risk_model.pkl          # ✅ Saved (Healthcare)
└── (Fintech models not saved yet)
```

### Recommended Structure (Future)

```
trained_models/
├── healthcare/
│   ├── risk_scoring/
│   │   ├── v1.0/
│   │   │   ├── model.pkl
│   │   │   ├── scaler.pkl
│   │   │   └── metadata.json
│   │   └── v1.1/
│   └── diagnostic_ai/
│       └── (future models)
├── fintech/
│   ├── credit_risk/
│   │   └── v1.0/
│   ├── fraud_detection/
│   │   └── v1.0/
│   ├── kyc_aml/
│   │   └── v1.0/
│   ├── market_signal/
│   │   └── v1.0/
│   ├── regime_simulation/
│   │   └── v1.0/
│   ├── commodity_trend/
│   │   └── v1.0/
│   ├── market_regime_intelligence/
│   │   └── v1.0/
│   ├── digital_asset_adoption/
│   │   └── v1.0/
│   └── exchange_risk/
│       └── v1.0/
└── metadata.json                      # Model registry
```

---

## Recommendations

### Immediate Improvements

1. **Save Fintech Models**: Update `FintechMLService` to save/load models like `HealthcareMLService`
2. **Save Market Intelligence Models**: Update `MarketIntelligenceMLService` to save/load models
3. **Model Versioning**: Implement version tracking for models
4. **Model Registry**: Create database table to track model versions and metrics

### Future Enhancements

1. **Offline Training Pipeline**: Separate training scripts that run periodically
2. **Model Evaluation**: Add test sets and evaluation metrics
3. **A/B Testing**: Support multiple model versions for comparison
4. **Model Monitoring**: Track model performance in production
5. **Automated Retraining**: Schedule periodic retraining with new data

