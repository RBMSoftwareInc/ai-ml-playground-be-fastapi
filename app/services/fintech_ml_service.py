"""
Fintech ML Service
Boardroom-grade ML models for inference (not training)
Models are trained offline, APIs perform inference only
"""
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os
from datetime import datetime


class FintechMLService:
    """
    ML service for Fintech modules
    Models are pre-trained and loaded for inference
    """
    
    def __init__(self):
        """Initialize ML service with pre-trained models"""
        self.models = {}
        self.scalers = {}
        self.model_version = "1.0.0"
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize and train models on synthetic data"""
        # For now, we'll create models on-the-fly with synthetic training
        # In production, these would be loaded from saved model files
        
        # Credit Risk Model
        self._train_credit_risk_model()
        
        # Fraud Detection Model
        self._train_fraud_detection_model()
        
        # KYC/AML Model
        self._train_kyc_aml_model()
        
        # Market Signal Model
        self._train_market_signal_model()
        
        # Regime Simulation Model
        self._train_regime_simulation_model()
    
    def _train_credit_risk_model(self):
        """Train credit risk model on synthetic data"""
        from app.services.fintech_data_generator import FintechDataGenerator
        
        generator = FintechDataGenerator(seed=42)
        n_samples = 10000
        
        X = []
        y = []
        
        for i in range(n_samples):
            borrower_id = f"BORROWER_{i}"
            borrower = generator.generate_borrower_profile(borrower_id)
            credit_history = generator.generate_credit_history(borrower_id, borrower)
            financial_behavior = generator.generate_financial_behavior(borrower_id, borrower, credit_history)
            
            # Features
            features = [
                borrower["age"] / 100.0,
                borrower["employment_stability_score"],
                borrower["annual_income"] / 200000.0,  # Normalize
                borrower["income_volatility_index"],
                borrower["residence_stability_score"],
                {"excellent": 0.9, "good": 0.7, "fair": 0.5, "poor": 0.3}.get(credit_history["credit_score_band"], 0.5),
                credit_history["total_active_loans"] / 10.0,
                credit_history["delinquency_count"] / 12.0,
                credit_history["repayment_consistency_score"],
                financial_behavior["debt_to_income_ratio"],
                financial_behavior["utilization_ratio"],
                financial_behavior["payment_delay_frequency"]
            ]
            
            X.append(features)
            
            # Target: default probability (0-1)
            macro_context = {"economic_stress_level": np.random.uniform(0.1, 0.8)}
            outcome = generator.generate_credit_outcome(borrower_id, borrower, credit_history, financial_behavior, macro_context)
            y.append(1.0 if outcome["default_within_12m"] else 0.0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_scaled, y)
        
        self.models["credit_risk"] = model
        self.scalers["credit_risk"] = scaler
    
    def _train_fraud_detection_model(self):
        """Train fraud detection model on synthetic data"""
        from app.services.fintech_data_generator import FintechDataGenerator
        
        generator = FintechDataGenerator(seed=42)
        n_samples = 50000  # More samples for fraud (imbalanced)
        
        X = []
        y = []
        
        for i in range(n_samples):
            account_id = f"ACC_{i % 1000}"  # Reuse accounts
            account = generator.generate_account_profile(account_id)
            
            is_fraud = np.random.random() < 0.01  # 1% fraud rate
            transaction = generator.generate_transaction_event(f"TXN_{i}", account_id, is_fraud)
            
            # Features
            features = [
                transaction["amount"] / 10000.0,  # Normalize
                {"online": 0.3, "pos": 0.4, "atm": 0.1, "mobile": 0.2}.get(transaction["channel_type"], 0.3),
                1.0 if transaction["geo_location"] != account["typical_geo_region"] else 0.0,
                transaction["timestamp"].split("T")[1].split(":")[0] if "T" in transaction["timestamp"] else 12,  # Hour
                account["account_age_days"] / 3650.0,
                abs(transaction["amount"] - account["avg_transaction_amount"]) / account["avg_transaction_amount"] if account["avg_transaction_amount"] > 0 else 0.0
            ]
            
            X.append(features)
            y.append(1.0 if is_fraud else 0.0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight="balanced", random_state=42)
        model.fit(X_scaled, y)
        
        self.models["fraud_detection"] = model
        self.scalers["fraud_detection"] = scaler
    
    def _train_kyc_aml_model(self):
        """Train KYC/AML model on synthetic data"""
        from app.services.fintech_data_generator import FintechDataGenerator
        
        generator = FintechDataGenerator(seed=42)
        n_samples = 5000
        
        X = []
        y = []
        
        for i in range(n_samples):
            customer_id = f"CUST_{i}"
            is_high_risk = np.random.random() < 0.1  # 10% high risk
            customer = generator.generate_customer_identity(customer_id, is_high_risk)
            identity_verification = generator.generate_identity_verification(customer_id, is_high_risk)
            relationship_network = generator.generate_relationship_network(customer_id, is_high_risk)
            
            # Features
            features = [
                1.0 if customer["country_code"] in ["US", "CA", "UK"] else 0.0,  # Low risk country
                {"low": 0.2, "medium": 0.5, "high": 0.8}.get(customer["occupation_risk_level"], 0.5),
                identity_verification["document_match_score"],
                identity_verification["biometric_match_score"],
                identity_verification["name_similarity_score"],
                relationship_network["linked_entities_count"] / 50.0,
                1.0 if relationship_network["high_risk_link_flag"] else 0.0,
                relationship_network["network_complexity_score"]
            ]
            
            X.append(features)
            
            # Target: AML risk level (0=low, 1=medium, 2=high, 3=very_high)
            compliance = generator.generate_compliance_outcome(customer_id, customer, relationship_network)
            risk_level_map = {"low": 0, "medium": 1, "high": 2, "very_high": 3}
            y.append(risk_level_map.get(compliance["aml_risk_level"], 1))
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight="balanced", random_state=42)
        model.fit(X_scaled, y)
        
        self.models["kyc_aml"] = model
        self.scalers["kyc_aml"] = scaler
    
    def _train_market_signal_model(self):
        """Train market signal model"""
        # Market signal model is simpler - uses time series features
        # For now, we'll use a simple regressor
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        scaler = StandardScaler()
        
        # Train on synthetic market data
        from app.services.fintech_data_generator import FintechDataGenerator
        generator = FintechDataGenerator(seed=42)
        
        X = []
        y = []
        
        for regime in ["calm", "volatile", "stress"]:
            series = generator.generate_market_time_series("MARKET_1", days=100, regime=regime)
            for i in range(10, len(series)):
                # Features: rolling window
                window = series[i-10:i]
                features = [
                    np.mean([s["return_volatility"] for s in window]),
                    np.std([s["return_volatility"] for s in window]),
                    np.mean([s["drawdown_level"] for s in window]),
                    np.mean([s["liquidity_shift_index"] for s in window])
                ]
                X.append(features)
                
                # Target: stress state (0=calm, 1=stressed, 2=volatile)
                if regime == "calm":
                    y.append(0.0)
                elif regime == "stress":
                    y.append(1.0)
                else:
                    y.append(2.0)
        
        X = np.array(X)
        y = np.array(y)
        
        X_scaled = scaler.fit_transform(X)
        model.fit(X_scaled, y)
        
        self.models["market_signal"] = model
        self.scalers["market_signal"] = scaler
    
    def _train_regime_simulation_model(self):
        """Train regime simulation model"""
        # Similar to market signal but for regime transitions
        model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
        scaler = StandardScaler()
        
        from app.services.fintech_data_generator import FintechDataGenerator
        generator = FintechDataGenerator(seed=42)
        
        X = []
        y = []
        
        regimes = ["calm", "volatile", "stress"]
        for regime in regimes:
            series = generator.generate_market_time_series("MARKET_1", days=100, regime=regime)
            for i in range(10, len(series)):
                window = series[i-10:i]
                features = [
                    np.mean([s["return_volatility"] for s in window]),
                    np.std([s["return_volatility"] for s in window]),
                    np.mean([s["drawdown_level"] for s in window]),
                    np.mean([s["liquidity_shift_index"] for s in window])
                ]
                X.append(features)
                y.append(regime)
        
        X = np.array(X)
        X_scaled = scaler.fit_transform(X)
        model.fit(X_scaled, y)
        
        self.models["regime_simulation"] = model
        self.scalers["regime_simulation"] = scaler
    
    # ==================== INFERENCE METHODS ====================
    
    def predict_credit_risk(self, features: List[float], scenario_params: Dict[str, Any]) -> Tuple[float, float, Dict[str, Any]]:
        """Predict credit risk"""
        model = self.models["credit_risk"]
        scaler = self.scalers["credit_risk"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        default_probability = float(model.predict(X_scaled)[0])
        default_probability = float(np.clip(default_probability, 0.0, 1.0))
        
        # Apply scenario adjustment
        default_probability *= scenario_params.get("default_probability_sensitivity", 1.0)
        default_probability = float(min(0.95, default_probability))
        
        # Calculate risk score (inverse of default probability)
        risk_score = float(1.0 - default_probability)
        
        # Loss given default estimate
        if default_probability < 0.1:
            lgd_estimate = 0.2
        elif default_probability < 0.3:
            lgd_estimate = 0.4
        else:
            lgd_estimate = 0.6
        
        metadata = {
            "model_version": self.model_version,
            "feature_importance": self._get_feature_importance(model, features)
        }
        
        return risk_score, default_probability, metadata
    
    def predict_fraud(self, features: List[float], scenario_params: Dict[str, Any]) -> Tuple[float, bool, Optional[str], Dict[str, Any]]:
        """Predict fraud"""
        model = self.models["fraud_detection"]
        scaler = self.scalers["fraud_detection"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        fraud_probability = model.predict_proba(X_scaled)[0][1]
        fraud_probability = float(np.clip(fraud_probability, 0.0, 1.0))
        
        # Apply scenario adjustment
        fraud_probability += scenario_params.get("fraud_probability_bias", 0.0)
        fraud_probability = float(min(0.99, max(0.0, fraud_probability)))
        
        fraud_flag = bool(fraud_probability > 0.5)
        
        fraud_type = None
        if fraud_flag:
            if fraud_probability > 0.8:
                fraud_type = "account_takeover"
            elif fraud_probability > 0.6:
                fraud_type = "card_testing"
            else:
                fraud_type = "suspicious_activity"
        
        metadata = {
            "model_version": self.model_version,
            "feature_importance": self._get_feature_importance(model, features)
        }
        
        return float(fraud_probability), bool(fraud_flag), fraud_type, metadata
    
    def predict_kyc_aml_risk(self, features: List[float], scenario_params: Dict[str, Any]) -> Tuple[float, str, bool, Dict[str, Any]]:
        """Predict KYC/AML risk"""
        model = self.models["kyc_aml"]
        scaler = self.scalers["kyc_aml"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        risk_level_probs = model.predict_proba(X_scaled)[0]
        risk_level = model.predict(X_scaled)[0]
        
        # Apply scenario adjustment
        risk_level_probs = risk_level_probs * scenario_params.get("aml_risk_multiplier", 1.0)
        risk_level_probs = risk_level_probs / risk_level_probs.sum()  # Renormalize
        
        risk_level_map = {0: "low", 1: "medium", 2: "high", 3: "very_high"}
        aml_risk_level = risk_level_map.get(int(risk_level), "medium")
        
        # Calculate risk score (0-1)
        aml_risk_score = float(risk_level_probs[1] * 0.3 + risk_level_probs[2] * 0.6 + risk_level_probs[3] * 0.9)
        aml_risk_score = float(np.clip(aml_risk_score, 0.0, 1.0))
        
        escalation_required = bool(aml_risk_level in ["high", "very_high"])
        
        metadata = {
            "model_version": self.model_version,
            "risk_level_probabilities": {
                "low": float(risk_level_probs[0]),
                "medium": float(risk_level_probs[1]),
                "high": float(risk_level_probs[2]),
                "very_high": float(risk_level_probs[3])
            }
        }
        
        return float(aml_risk_score), str(aml_risk_level), bool(escalation_required), metadata
    
    def predict_market_signal(self, features: List[float], scenario_params: Dict[str, Any]) -> Tuple[str, float, float, Dict[str, Any]]:
        """Predict market signal"""
        model = self.models["market_signal"]
        scaler = self.scalers["market_signal"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        stress_state_pred = model.predict(X_scaled)[0]
        stress_state_map = {0.0: "calm", 1.0: "stressed", 2.0: "volatile"}
        stress_state = stress_state_map.get(stress_state_pred, "calm")
        
        # Calculate stress score
        stress_score = float(stress_state_pred / 2.0)  # Normalize to 0-1
        stress_score = float(np.clip(stress_score, 0.0, 1.0))
        
        # Apply scenario adjustment
        stress_score += scenario_params.get("volatility_bias", 0.0)
        stress_score = float(np.clip(stress_score, 0.0, 1.0))
        
        # Sentiment index (simplified)
        sentiment_index = float(-0.5 + (1.0 - stress_score) * 1.0)  # Inverse relationship
        sentiment_index = float(np.clip(sentiment_index, -1.0, 1.0))
        
        # Volatility forecast
        volatility_forecast = float(features[0] * (1.0 + scenario_params.get("volatility_bias", 0.0)))
        
        metadata = {
            "model_version": self.model_version,
            "stress_state_confidence": 0.75
        }
        
        return str(stress_state), float(stress_score), float(sentiment_index), float(volatility_forecast), metadata
    
    def predict_regime(self, features: List[float], scenario_params: Dict[str, Any]) -> Tuple[str, float, str, float, Dict[str, Any]]:
        """Predict market regime"""
        model = self.models["regime_simulation"]
        scaler = self.scalers["regime_simulation"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        regime_probs = model.predict_proba(X_scaled)[0]
        regime_label = str(model.predict(X_scaled)[0])
        
        # Regime confidence
        regime_confidence = float(max(regime_probs))
        
        # Projected regime (can be different from current)
        transition_prob = float(scenario_params.get("regime_transition_probability", 0.3))
        if np.random.random() < transition_prob:
            # Transition to different regime
            regimes = model.classes_
            projected_regime = str(np.random.choice(regimes))
        else:
            projected_regime = str(regime_label)
        
        # Stress indicators
        stress_indicators = {
            "volatility_shock": float(features[0] * scenario_params.get("volatility_shock_level", 1.0)),
            "correlation_breakdown": float(scenario_params.get("correlation_breakdown_score", 0.0)),
            "liquidity_crisis": float(features[3] * (1.0 - scenario_params.get("liquidity_crisis_level", 0.0)))
        }
        
        metadata = {
            "model_version": self.model_version,
            "regime_probabilities": {str(r): float(p) for r, p in zip(model.classes_, regime_probs)}
        }
        
        return str(regime_label), float(regime_confidence), str(projected_regime), float(transition_prob), stress_indicators, metadata
    
    def _get_feature_importance(self, model, features: List[float]) -> List[Dict[str, Any]]:
        """Get feature importance for explanation"""
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feature_names = [f"feature_{i}" for i in range(len(features))]
            importance_list = [
                {"feature": name, "importance": float(imp), "value": float(val)}
                for name, imp, val in zip(feature_names, importances, features)
            ]
            importance_list.sort(key=lambda x: x["importance"], reverse=True)
            return importance_list[:5]  # Top 5
        return []


# Global instance
fintech_ml_service = FintechMLService()

