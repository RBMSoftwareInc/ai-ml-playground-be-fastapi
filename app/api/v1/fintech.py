"""
Fintech API Routes - Boardroom-Grade Intelligence Layer
5 Modules: Credit Risk, Fraud Detection, KYC/AML, Market Signal, Regime Simulation
All responses include mandatory explanation contracts
"""
import numpy as np
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.schemas.fintech import (
    CreditRiskRequest, CreditRiskResponse,
    FraudDetectionRequest, FraudDetectionResponse,
    KYCRiskRequest, KYCRiskResponse,
    MarketSignalRequest, MarketSignalResponse,
    RegimeSimulationRequest, RegimeSimulationResponse,
    # Market & Digital Asset Intelligence
    CommodityTrendRequest, CommodityTrendResponse,
    MarketRegimeIntelligenceRequest, MarketRegimeIntelligenceResponse,
    DigitalAssetAdoptionRequest, DigitalAssetAdoptionResponse,
    ExchangeRiskRequest, ExchangeRiskResponse
)
from app.services.fintech_scenarios import FintechScenarioCatalog
from app.services.fintech_ml_service import fintech_ml_service
from app.services.fintech_explanation_engine import fintech_explanation_engine
from app.services.fintech_data_generator import FintechDataGenerator
from app.services.market_intelligence_ml_service import market_intelligence_ml_service
from app.services.market_intelligence_explanation_engine import market_intelligence_explanation_engine
from app.services.market_intelligence_data_generator import MarketIntelligenceDataGenerator
from app.services.market_intelligence_scenarios import MarketIntelligenceScenarioEngine

router = APIRouter(tags=["Fintech"])


# ==================== MODULE 1: CREDIT RISK INTELLIGENCE ====================

@router.post("/credit-risk", response_model=CreditRiskResponse)
async def credit_risk_assessment(
    request: CreditRiskRequest
):
    """
    Credit Risk Intelligence - Boardroom-grade credit risk assessment
    
    Scenarios:
    - stable_economy: Normal economic conditions
    - rising_interest_rates: Rising rates increase default risk
    - economic_downturn: Recession with high unemployment
    - high_inflation: High inflation erodes purchasing power
    """
    try:
        # Get scenario parameters
        scenario_catalog = FintechScenarioCatalog()
        scenario_params = scenario_catalog.get_credit_risk_scenario(request.scenario)
        
        # Generate or retrieve borrower data
        if request.borrower_id:
            # In production, fetch from database
            # For now, generate synthetic data
            generator = FintechDataGenerator()
            borrower_profile = generator.generate_borrower_profile(request.borrower_id)
            credit_history = generator.generate_credit_history(request.borrower_id, borrower_profile)
            financial_behavior = generator.generate_financial_behavior(
                request.borrower_id, borrower_profile, credit_history
            )
        else:
            # Use provided borrower data
            borrower_data = request.borrower_data or {}
            borrower_profile = {
                "age": borrower_data.get("age", 35),
                "employment_stability_score": borrower_data.get("employment_stability_score", 0.7),
                "annual_income": borrower_data.get("annual_income", 50000),
                "income_volatility_index": borrower_data.get("income_volatility_index", 0.3),
                "residence_stability_score": borrower_data.get("residence_stability_score", 0.7)
            }
            credit_history = {
                "credit_score_band": borrower_data.get("credit_score_band", "good"),
                "total_active_loans": borrower_data.get("total_active_loans", 2),
                "delinquency_count": borrower_data.get("delinquency_count", 0),
                "repayment_consistency_score": borrower_data.get("repayment_consistency_score", 0.8)
            }
            financial_behavior = {
                "debt_to_income_ratio": borrower_data.get("debt_to_income_ratio", 0.3),
                "utilization_ratio": borrower_data.get("utilization_ratio", 0.4),
                "payment_delay_frequency": borrower_data.get("payment_delay_frequency", 0.1)
            }
        
        # Prepare features for ML model
        features = [
            borrower_profile["age"] / 100.0,
            borrower_profile["employment_stability_score"],
            borrower_profile["annual_income"] / 200000.0,
            borrower_profile["income_volatility_index"],
            borrower_profile["residence_stability_score"],
            {"excellent": 0.9, "good": 0.7, "fair": 0.5, "poor": 0.3}.get(credit_history["credit_score_band"], 0.5),
            credit_history["total_active_loans"] / 10.0,
            credit_history["delinquency_count"] / 12.0,
            credit_history["repayment_consistency_score"],
            financial_behavior["debt_to_income_ratio"],
            financial_behavior["utilization_ratio"],
            financial_behavior["payment_delay_frequency"]
        ]
        
        # Predict credit risk
        risk_score, default_probability, model_metadata = fintech_ml_service.predict_credit_risk(
            features, scenario_params
        )
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = "low"
            recommendation = "Approve with standard terms"
        elif risk_score >= 0.6:
            risk_level = "medium"
            recommendation = "Approve with enhanced monitoring"
        elif risk_score >= 0.4:
            risk_level = "high"
            recommendation = "Require additional collateral or guarantees"
        else:
            risk_level = "very_high"
            recommendation = "Reject or require significant risk mitigation"
        
        # Calculate loss given default
        if default_probability < 0.1:
            lgd_estimate = 0.2
        elif default_probability < 0.3:
            lgd_estimate = 0.4
        else:
            lgd_estimate = 0.6
        
        # Generate explanation
        borrower_features = {
            "credit_score_band": credit_history["credit_score_band"],
            "debt_to_income_ratio": financial_behavior["debt_to_income_ratio"],
            "employment_stability_score": borrower_profile["employment_stability_score"]
        }
        
        explanation = fintech_explanation_engine.generate_credit_risk_explanation(
            risk_score=risk_score,
            default_probability=default_probability,
            borrower_features=borrower_features,
            scenario_params=scenario_params,
            model_metadata=model_metadata
        )
        
        return CreditRiskResponse(
            success=True,
            borrower_id=request.borrower_id or "GENERATED",
            risk_score=risk_score,
            risk_level=risk_level,
            default_probability=default_probability,
            loss_given_default_estimate=lgd_estimate,
            recommendation=recommendation,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "borrower_profile": borrower_profile,
                "credit_history": credit_history,
                "financial_behavior": financial_behavior
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Credit risk assessment failed: {str(e)}")


# ==================== MODULE 2: FRAUD DETECTION CONTROL ROOM ====================

@router.post("/fraud-detection", response_model=FraudDetectionResponse)
async def fraud_detection(
    request: FraudDetectionRequest
):
    """
    Fraud Detection Control Room - Real-time transaction fraud detection
    
    Scenarios:
    - normal_behavior: Standard transaction patterns
    - velocity_spike: Unusual transaction velocity
    - geo_shift: Transaction from unusual location
    - coordinated_fraud: Coordinated fraud attack pattern
    """
    try:
        # Get scenario parameters
        scenario_catalog = FintechScenarioCatalog()
        scenario_params = scenario_catalog.get_fraud_detection_scenario(request.scenario)
        
        # Extract transaction data
        transaction_data = request.transaction_data
        amount = transaction_data.get("amount", 0.0)
        channel_type = transaction_data.get("channel_type", "online")
        geo_location = transaction_data.get("geo_location", "US")
        timestamp_str = transaction_data.get("timestamp", datetime.now().isoformat())
        
        # Get account profile (in production, from database)
        account_id = transaction_data.get("account_id", "ACC_UNKNOWN")
        generator = FintechDataGenerator()
        account_profile = generator.generate_account_profile(account_id)
        
        # Calculate features
        amount_deviation = abs(amount - account_profile["avg_transaction_amount"]) / account_profile["avg_transaction_amount"] if account_profile["avg_transaction_amount"] > 0 else 0.0
        geo_deviation = geo_location != account_profile["typical_geo_region"]
        
        # Extract hour from timestamp
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            hour = timestamp.hour
        except:
            hour = 12
        
        velocity_anomaly = False  # Would be calculated from transaction history
        
        # Prepare features for ML model
        features = [
            amount / 10000.0,
            {"online": 0.3, "pos": 0.4, "atm": 0.1, "mobile": 0.2}.get(channel_type, 0.3),
            1.0 if geo_deviation else 0.0,
            hour / 24.0,
            account_profile["account_age_days"] / 3650.0,
            amount_deviation
        ]
        
        # Predict fraud
        fraud_probability, fraud_flag, fraud_type, model_metadata = fintech_ml_service.predict_fraud(
            features, scenario_params
        )
        
        # Determine risk level
        if fraud_probability < 0.3:
            risk_level = "low"
            recommendation = "Transaction appears legitimate. Process normally."
        elif fraud_probability < 0.6:
            risk_level = "medium"
            recommendation = "Transaction flagged for review. Consider additional authentication."
        elif fraud_probability < 0.8:
            risk_level = "high"
            recommendation = "High fraud probability. Block transaction and alert security team."
        else:
            risk_level = "critical"
            recommendation = "Critical fraud alert. Block transaction immediately and escalate."
        
        # Generate explanation
        transaction_features = {
            "amount": amount,
            "amount_deviation": amount_deviation,
            "geo_deviation": geo_deviation,
            "velocity_anomaly": velocity_anomaly,
            "channel_type": channel_type
        }
        
        explanation = fintech_explanation_engine.generate_fraud_detection_explanation(
            fraud_probability=fraud_probability,
            fraud_flag=fraud_flag,
            transaction_features=transaction_features,
            scenario_params=scenario_params,
            model_metadata=model_metadata
        )
        
        return FraudDetectionResponse(
            success=True,
            transaction_id=request.transaction_id or transaction_data.get("transaction_id", "TXN_GENERATED"),
            fraud_probability=fraud_probability,
            fraud_flag=fraud_flag,
            fraud_type=fraud_type,
            risk_level=risk_level,
            recommendation=recommendation,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "account_profile": account_profile,
                "transaction_data": transaction_data
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fraud detection failed: {str(e)}")


# ==================== MODULE 3: KYC / AML RISK ENGINE ====================

@router.post("/kyc-aml", response_model=KYCRiskResponse)
async def kyc_aml_assessment(
    request: KYCRiskRequest
):
    """
    KYC / AML Risk Engine - Customer risk assessment for compliance
    
    Scenarios:
    - low_risk_retail: Standard retail customer
    - high_risk_jurisdiction: Customer from high-risk jurisdiction
    - pep_profile: Politically Exposed Person
    - networked_entity: Entity with complex relationship network
    """
    try:
        # Get scenario parameters
        scenario_catalog = FintechScenarioCatalog()
        scenario_params = scenario_catalog.get_kyc_aml_scenario(request.scenario)
        
        # Generate or retrieve customer data
        if request.customer_id:
            generator = FintechDataGenerator()
            is_high_risk = request.scenario in ["high_risk_jurisdiction", "pep_profile", "networked_entity"]
            customer_identity = generator.generate_customer_identity(request.customer_id, is_high_risk)
            identity_verification = generator.generate_identity_verification(request.customer_id, is_high_risk)
            relationship_network = generator.generate_relationship_network(request.customer_id, is_high_risk)
        else:
            customer_data = request.customer_data or {}
            customer_identity = {
                "country_code": customer_data.get("country_code", "US"),
                "occupation_risk_level": customer_data.get("occupation_risk_level", "low")
            }
            identity_verification = {
                "document_match_score": customer_data.get("document_match_score", 0.95),
                "biometric_match_score": customer_data.get("biometric_match_score", 0.97),
                "name_similarity_score": customer_data.get("name_similarity_score", 0.92)
            }
            relationship_network = {
                "linked_entities_count": customer_data.get("linked_entities_count", 3),
                "high_risk_link_flag": customer_data.get("high_risk_link_flag", False),
                "network_complexity_score": customer_data.get("network_complexity_score", 0.3)
            }
        
        # Determine jurisdiction risk
        low_risk_countries = ["US", "CA", "UK", "DE", "FR", "AU", "NZ"]
        jurisdiction_risk = "low" if customer_identity["country_code"] in low_risk_countries else "high"
        
        # Prepare features for ML model
        features = [
            1.0 if customer_identity["country_code"] in low_risk_countries else 0.0,
            {"low": 0.2, "medium": 0.5, "high": 0.8}.get(customer_identity["occupation_risk_level"], 0.5),
            identity_verification["document_match_score"],
            identity_verification["biometric_match_score"],
            identity_verification["name_similarity_score"],
            relationship_network["linked_entities_count"] / 50.0,
            1.0 if relationship_network["high_risk_link_flag"] else 0.0,
            relationship_network["network_complexity_score"]
        ]
        
        # Apply scenario adjustments
        scenario_adjusted_params = scenario_params.copy()
        scenario_adjusted_params["aml_risk_multiplier"] = 1.0 + scenario_params.get("aml_risk_bias", 0.0)
        
        # Predict KYC/AML risk
        aml_risk_score, aml_risk_level, escalation_required, model_metadata = fintech_ml_service.predict_kyc_aml_risk(
            features, scenario_adjusted_params
        )
        
        # Determine KYC status
        if aml_risk_level == "low":
            kyc_status = "approved"
            recommendation = "Customer approved. Standard monitoring required."
        elif aml_risk_level == "medium":
            kyc_status = "pending_review"
            recommendation = "Customer requires review. Enhanced due diligence recommended."
        elif aml_risk_level == "high":
            kyc_status = "escalated"
            recommendation = "Customer escalated. Comprehensive review and additional documentation required."
        else:
            kyc_status = "rejected"
            recommendation = "Customer rejected. High AML risk profile."
        
        # Generate explanation
        customer_features = {
            "jurisdiction_risk": jurisdiction_risk,
            "occupation_risk_level": customer_identity["occupation_risk_level"],
            "network_complexity_score": relationship_network["network_complexity_score"],
            "identity_verification_scores": {
                "document": identity_verification["document_match_score"],
                "biometric": identity_verification["biometric_match_score"],
                "name": identity_verification["name_similarity_score"]
            }
        }
        
        explanation = fintech_explanation_engine.generate_kyc_aml_explanation(
            aml_risk_score=aml_risk_score,
            aml_risk_level=aml_risk_level,
            escalation_required=escalation_required,
            customer_features=customer_features,
            scenario_params=scenario_params,
            model_metadata=model_metadata
        )
        
        return KYCRiskResponse(
            success=True,
            customer_id=request.customer_id or "CUST_GENERATED",
            aml_risk_score=aml_risk_score,
            aml_risk_level=aml_risk_level,
            escalation_required=escalation_required,
            kyc_status=kyc_status,
            recommendation=recommendation,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "customer_identity": customer_identity,
                "identity_verification": identity_verification,
                "relationship_network": relationship_network
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"KYC/AML assessment failed: {str(e)}")


# ==================== MODULE 4: MARKET SIGNAL INTELLIGENCE ====================

@router.post("/market-signal", response_model=MarketSignalResponse)
async def market_signal_intelligence(
    request: MarketSignalRequest
):
    """
    Market Signal Intelligence - Market stress and sentiment analysis
    
    Scenarios:
    - calm_market: Stable market conditions
    - news_uncertainty: News-driven uncertainty
    - liquidity_stress: Liquidity constraints
    - macro_shock: Major macroeconomic shock
    """
    try:
        # Get scenario parameters
        scenario_catalog = FintechScenarioCatalog()
        scenario_params = scenario_catalog.get_market_signal_scenario(request.scenario)
        
        # Generate market time series (in production, from database)
        generator = FintechDataGenerator()
        regime = "stress" if request.scenario in ["liquidity_stress", "macro_shock"] else "calm"
        series = generator.generate_market_time_series(request.market_id, days=request.time_horizon_days, regime=regime)
        
        # Calculate features from recent window
        recent_window = series[-10:] if len(series) >= 10 else series
        features = [
            float(np.mean([s["return_volatility"] for s in recent_window])),
            float(np.std([s["return_volatility"] for s in recent_window])),
            float(np.mean([s["drawdown_level"] for s in recent_window])),
            float(np.mean([s["liquidity_shift_index"] for s in recent_window]))
        ]
        
        # Predict market signal
        stress_state, stress_score, sentiment_index, volatility_forecast, model_metadata = fintech_ml_service.predict_market_signal(
            features, scenario_params
        )
        
        # Generate recommendation
        if stress_state == "calm":
            recommendation = "Market conditions stable. Standard risk management protocols sufficient."
        elif stress_state == "stressed":
            recommendation = "Market stress detected. Increase monitoring and consider defensive positioning."
        else:
            recommendation = "High market volatility. Implement stress protocols and reduce exposure."
        
        # Generate explanation
        market_features = {
            "volatility_index": features[0],
            "liquidity_index": features[3],
            "sentiment_index": sentiment_index
        }
        
        explanation = fintech_explanation_engine.generate_market_signal_explanation(
            stress_state=stress_state,
            stress_score=stress_score,
            sentiment_index=sentiment_index,
            market_features=market_features,
            scenario_params=scenario_params,
            model_metadata=model_metadata
        )
        
        return MarketSignalResponse(
            success=True,
            market_id=request.market_id,
            market_stress_state=stress_state,
            stress_score=stress_score,
            sentiment_index=sentiment_index,
            volatility_forecast=volatility_forecast,
            recommendation=recommendation,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "time_horizon_days": request.time_horizon_days,
                "recent_volatility": features[0],
                "recent_liquidity": features[3]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market signal analysis failed: {str(e)}")


# ==================== MODULE 5: MARKET REGIME SIMULATION ENGINE ====================

@router.post("/regime-simulation", response_model=RegimeSimulationResponse)
async def regime_simulation(
    request: RegimeSimulationRequest
):
    """
    Market Regime Simulation Engine - Regime transition and stress scenario analysis
    
    Scenarios:
    - volatility_expansion: Expanding volatility regime
    - correlation_breakdown: Asset correlation breakdown
    - liquidity_freeze: Severe liquidity crisis
    """
    try:
        # Get scenario parameters
        scenario_catalog = FintechScenarioCatalog()
        scenario_params = scenario_catalog.get_regime_simulation_scenario(request.scenario)
        
        # Generate market time series
        generator = FintechDataGenerator()
        regime = "volatile" if request.scenario == "volatility_expansion" else "stress"
        series = generator.generate_market_time_series(
            request.market_id, 
            days=request.simulation_horizon_days, 
            regime=regime
        )
        
        # Calculate features
        recent_window = series[-10:] if len(series) >= 10 else series
        features = [
            float(np.mean([s["return_volatility"] for s in recent_window])),
            float(np.std([s["return_volatility"] for s in recent_window])),
            float(np.mean([s["drawdown_level"] for s in recent_window])),
            float(np.mean([s["liquidity_shift_index"] for s in recent_window]))
        ]
        
        # Apply stress level if provided
        if request.stress_level is not None:
            features[0] = float(request.stress_level)  # Override volatility
        
        # Predict regime
        current_regime, regime_confidence, projected_regime, transition_probability, stress_indicators, model_metadata = fintech_ml_service.predict_regime(
            features, scenario_params
        )
        
        # Generate recommendation
        if current_regime == projected_regime:
            recommendation = f"Regime stable at '{current_regime}'. Monitor for transition signals."
        else:
            recommendation = f"Regime transition expected to '{projected_regime}'. Prepare for regime change and adjust risk models."
        
        # Generate explanation
        explanation = fintech_explanation_engine.generate_regime_simulation_explanation(
            current_regime=current_regime,
            regime_confidence=regime_confidence,
            projected_regime=projected_regime,
            transition_probability=transition_probability,
            stress_indicators=stress_indicators,
            scenario_params=scenario_params,
            model_metadata=model_metadata
        )
        
        return RegimeSimulationResponse(
            success=True,
            market_id=request.market_id,
            current_regime=current_regime,
            regime_confidence=regime_confidence,
            projected_regime=projected_regime,
            transition_probability=transition_probability,
            stress_indicators=stress_indicators,
            recommendation=recommendation,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "simulation_horizon_days": request.simulation_horizon_days,
                "stress_level_applied": request.stress_level,
                "regime_probabilities": model_metadata.get("regime_probabilities", {})
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regime simulation failed: {str(e)}")


# ==================== UTILITY ENDPOINTS ====================

@router.get("/scenarios")
async def get_scenarios():
    """Get available scenarios for all modules"""
    return {
        "credit_risk": {
            "stable_economy": "Normal economic conditions",
            "rising_interest_rates": "Rising rates increase default risk",
            "economic_downturn": "Recession with high unemployment",
            "high_inflation": "High inflation erodes purchasing power"
        },
        "fraud_detection": {
            "normal_behavior": "Standard transaction patterns",
            "velocity_spike": "Unusual transaction velocity",
            "geo_shift": "Transaction from unusual location",
            "coordinated_fraud": "Coordinated fraud attack pattern"
        },
        "kyc_aml": {
            "low_risk_retail": "Standard retail customer",
            "high_risk_jurisdiction": "Customer from high-risk jurisdiction",
            "pep_profile": "Politically Exposed Person",
            "networked_entity": "Entity with complex relationship network"
        },
        "market_signal": {
            "calm_market": "Stable market conditions",
            "news_uncertainty": "News-driven uncertainty",
            "liquidity_stress": "Liquidity constraints",
            "macro_shock": "Major macroeconomic shock"
        },
        "regime_simulation": {
            "volatility_expansion": "Expanding volatility regime",
            "correlation_breakdown": "Asset correlation breakdown",
            "liquidity_freeze": "Severe liquidity crisis"
        },
        "market_intelligence": {
            "baseline": "Normal market conditions",
            "volatility_spike": "Sudden increase in market volatility",
            "demand_shock": "Significant increase in demand",
            "liquidity_drop": "Severe reduction in market liquidity",
            "stress_scenario": "Combined stress conditions"
        }
    }


# ==================== MARKET & DIGITAL ASSET INTELLIGENCE (FINTECH) ====================

@router.post("/commodity-trend", response_model=CommodityTrendResponse)
async def commodity_trend_intelligence(request: CommodityTrendRequest):
    """
    Commodity Trend Intelligence - Signal-based trend analysis
    
    Provides directional bias, confidence bands, and historical analogs
    """
    try:
        # Get scenario parameters
        scenario_engine = MarketIntelligenceScenarioEngine()
        scenario_params = scenario_engine.get_scenario(request.scenario)
        
        # Generate or retrieve market data
        generator = MarketIntelligenceDataGenerator()
        regime = "volatile" if request.scenario in ["volatility_spike", "stress_scenario"] else "normal"
        market_data = generator.generate_commodity_market_data(
            request.asset_id,
            datetime.now() - timedelta(days=request.lookback_days),
            days=request.lookback_days,
            regime=regime
        )
        
        # Calculate features from recent window
        recent_window = market_data[-10:] if len(market_data) >= 10 else market_data
        features = [
            float(np.mean([d["daily_return"] for d in recent_window])),
            float(np.std([d["daily_return"] for d in recent_window])),
            float(np.mean([d["volatility_indicator"] for d in recent_window])),
            float(np.mean([d["momentum_score"] for d in recent_window])),
            float(recent_window[-1]["close_price"] / recent_window[0]["close_price"] - 1.0) if len(recent_window) > 0 and recent_window[0]["close_price"] > 0 else 0.0
        ]
        
        # Apply scenario perturbations
        features = scenario_engine.apply_scenario_to_features(features, scenario_params, "commodity")
        
        # Predict trend
        directional_bias, confidence_lower, confidence_upper, trend_strength, volatility_estimate, similar_periods = market_intelligence_ml_service.predict_commodity_trend(
            features, scenario_params
        )
        
        # Generate explanation
        explanation = market_intelligence_explanation_engine.generate_commodity_trend_explanation(
            directional_bias=directional_bias,
            trend_strength=trend_strength,
            confidence_lower=confidence_lower,
            confidence_upper=confidence_upper,
            volatility_estimate=volatility_estimate,
            similar_periods=similar_periods,
            scenario_params=scenario_params
        )
        
        return CommodityTrendResponse(
            success=True,
            asset_id=request.asset_id,
            signal_date=datetime.now(),
            directional_bias=directional_bias,
            confidence_band_lower=confidence_lower,
            confidence_band_upper=confidence_upper,
            trend_strength=trend_strength,
            volatility_estimate=volatility_estimate,
            similar_periods=similar_periods,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "lookback_days": request.lookback_days,
                "recent_volatility": features[2]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Commodity trend analysis failed: {str(e)}")


@router.post("/market-regime-intelligence", response_model=MarketRegimeIntelligenceResponse)
async def market_regime_intelligence(request: MarketRegimeIntelligenceRequest):
    """
    Market Regime Intelligence - Regime identification and transition probabilities
    """
    try:
        # Get scenario parameters
        scenario_engine = MarketIntelligenceScenarioEngine()
        scenario_params = scenario_engine.get_scenario(request.scenario)
        
        # Generate regime features
        generator = MarketIntelligenceDataGenerator()
        regime = "stress" if request.scenario == "stress_scenario" else "volatile" if request.scenario == "volatility_spike" else "calm"
        regime_features = generator.generate_market_regime_features(
            request.market_id,
            datetime.now() - timedelta(days=request.lookback_days),
            days=request.lookback_days,
            regime=regime
        )
        
        # Calculate features
        recent_window = regime_features[-10:] if len(regime_features) >= 10 else regime_features
        features = [
            float(np.mean([f["rolling_volatility"] for f in recent_window])),
            float(np.mean([f["trend_strength"] for f in recent_window])),
            float(np.mean([f["drawdown_depth"] for f in recent_window])),
            float(np.mean([f["liquidity_proxy"] for f in recent_window]))
        ]
        
        # Apply scenario perturbations
        features = scenario_engine.apply_scenario_to_features(features, scenario_params, "regime")
        
        # Predict regime
        current_regime, regime_probability, stability_score, transition_probability, transition_likelihoods = market_intelligence_ml_service.predict_market_regime(
            features, scenario_params
        )
        
        # Generate explanation
        explanation = market_intelligence_explanation_engine.generate_market_regime_explanation(
            current_regime=current_regime,
            regime_probability=regime_probability,
            stability_score=stability_score,
            transition_probability=transition_probability,
            scenario_params=scenario_params
        )
        
        return MarketRegimeIntelligenceResponse(
            success=True,
            market_id=request.market_id,
            signal_date=datetime.now(),
            current_regime=current_regime,
            regime_probability=regime_probability,
            stability_score=stability_score,
            transition_probability=transition_probability,
            transition_likelihoods=transition_likelihoods,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "lookback_days": request.lookback_days,
                "recent_volatility": features[0]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market regime intelligence failed: {str(e)}")


@router.post("/digital-asset-adoption", response_model=DigitalAssetAdoptionResponse)
async def digital_asset_adoption_intelligence(request: DigitalAssetAdoptionRequest):
    """
    Digital Asset Adoption Intelligence - Adoption phase and momentum analysis
    """
    try:
        # Get scenario parameters
        scenario_engine = MarketIntelligenceScenarioEngine()
        scenario_params = scenario_engine.get_scenario(request.scenario)
        
        # Generate adoption data
        generator = MarketIntelligenceDataGenerator()
        adoption_data = generator.generate_digital_asset_adoption_data(
            request.country_code or "US",
            datetime.now() - timedelta(days=request.lookback_days),
            days=request.lookback_days,
            adoption_phase="growth"
        )
        
        # Calculate features
        recent_window = adoption_data[-10:] if len(adoption_data) >= 10 else adoption_data
        features = [
            float(np.mean([d["wallet_activity_index"] for d in recent_window])),
            float(np.mean([d["transaction_volume_index"] for d in recent_window])),
            float(np.mean([d["exchange_activity_index"] for d in recent_window])),
            float(np.mean([d["regulatory_signal_score"] for d in recent_window])),
            float((recent_window[-1]["wallet_activity_index"] - recent_window[0]["wallet_activity_index"]) / recent_window[0]["wallet_activity_index"]) if len(recent_window) > 0 and recent_window[0]["wallet_activity_index"] > 0 else 0.0
        ]
        
        # Apply scenario perturbations
        features = scenario_engine.apply_scenario_to_features(features, scenario_params, "adoption")
        
        # Predict adoption
        adoption_phase, momentum_score, growth_rate, acceleration_indicator = market_intelligence_ml_service.predict_digital_asset_adoption(
            features, scenario_params
        )
        
        # Generate explanation
        explanation = market_intelligence_explanation_engine.generate_digital_asset_adoption_explanation(
            adoption_phase=adoption_phase,
            momentum_score=momentum_score,
            growth_rate=growth_rate,
            acceleration_indicator=acceleration_indicator,
            scenario_params=scenario_params
        )
        
        return DigitalAssetAdoptionResponse(
            success=True,
            country_code=request.country_code,
            signal_date=datetime.now(),
            adoption_phase=adoption_phase,
            momentum_score=momentum_score,
            growth_rate=growth_rate,
            acceleration_indicator=acceleration_indicator,
            regional_rank=None,  # Would be calculated from regional comparison
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "lookback_days": request.lookback_days,
                "wallet_activity": features[0]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Digital asset adoption analysis failed: {str(e)}")


@router.post("/exchange-risk", response_model=ExchangeRiskResponse)
async def exchange_risk_mapping(request: ExchangeRiskRequest):
    """
    Exchange & Market Risk Mapping - Risk concentration and dependency analysis
    """
    try:
        # Get scenario parameters
        scenario_engine = MarketIntelligenceScenarioEngine()
        scenario_params = scenario_engine.get_scenario(request.scenario)
        
        # Generate exchange profile
        generator = MarketIntelligenceDataGenerator()
        is_high_risk = request.scenario in ["stress_scenario", "liquidity_drop"]
        exchange_profile = generator.generate_exchange_profile(
            request.exchange_id or "EXCHANGE_DEFAULT",
            is_high_risk=is_high_risk
        )
        
        # Prepare features
        features = [
            float(exchange_profile["asset_coverage"] / 1000.0),
            exchange_profile["volume_concentration"],
            exchange_profile["liquidity_depth_proxy"],
            exchange_profile["dependency_ratios"]["top_asset_dependency"],
            exchange_profile["dependency_ratios"]["cross_exchange_dependency"],
            float(len(exchange_profile["historical_stress_markers"]) / 10.0)
        ]
        
        # Apply scenario perturbations
        features = scenario_engine.apply_scenario_to_features(features, scenario_params, "exchange")
        
        # Predict risk
        risk_concentration, dependency_hotspots, systemic_exposure, stress_propagation = market_intelligence_ml_service.predict_exchange_risk(
            features, scenario_params
        )
        
        # Generate explanation
        explanation = market_intelligence_explanation_engine.generate_exchange_risk_explanation(
            risk_concentration_score=risk_concentration,
            dependency_hotspots=dependency_hotspots,
            systemic_exposure_indicator=systemic_exposure,
            stress_propagation_risk=stress_propagation,
            scenario_params=scenario_params
        )
        
        return ExchangeRiskResponse(
            success=True,
            exchange_id=request.exchange_id,
            signal_date=datetime.now(),
            risk_concentration_score=risk_concentration,
            dependency_hotspots=dependency_hotspots,
            systemic_exposure_indicator=systemic_exposure,
            stress_propagation_risk=stress_propagation,
            explanation=explanation,
            scenario_applied=request.scenario,
            metadata={
                "exchange_profile": exchange_profile
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exchange risk analysis failed: {str(e)}")
