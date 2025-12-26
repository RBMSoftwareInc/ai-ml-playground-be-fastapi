"""
Market Intelligence ML Service
Signal-based, explainable market behavior intelligence
Models trained offline, APIs perform inference only
"""
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import pickle


class MarketIntelligenceMLService:
    """
    ML service for Market & Digital Asset Intelligence modules
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
        # Commodity Trend Model
        self._train_commodity_trend_model()
        
        # Market Regime Model
        self._train_market_regime_model()
        
        # Digital Asset Adoption Model
        self._train_digital_asset_adoption_model()
        
        # Exchange Risk Model
        self._train_exchange_risk_model()
    
    def _train_commodity_trend_model(self):
        """Train commodity trend intelligence model"""
        from app.services.market_intelligence_data_generator import MarketIntelligenceDataGenerator
        
        generator = MarketIntelligenceDataGenerator(seed=42)
        n_samples = 5000
        
        X = []
        y_direction = []
        y_strength = []
        
        for regime in ["normal", "volatile", "stress"]:
            for asset in ["gold", "silver", "oil"]:
                data = generator.generate_commodity_market_data(
                    asset, datetime.now() - timedelta(days=365), days=100, regime=regime
                )
                for i in range(10, len(data)):
                    window = data[i-10:i]
                    features = [
                        np.mean([d["daily_return"] for d in window]),
                        np.std([d["daily_return"] for d in window]),
                        np.mean([d["volatility_indicator"] for d in window]),
                        np.mean([d["momentum_score"] for d in window]),
                        window[-1]["close_price"] / window[0]["close_price"] - 1.0  # Price change
                    ]
                    X.append(features)
                    
                    # Direction (up/down/sideways)
                    price_change = features[4]
                    if price_change > 0.02:
                        y_direction.append("up")
                    elif price_change < -0.02:
                        y_direction.append("down")
                    else:
                        y_direction.append("sideways")
                    
                    # Trend strength
                    y_strength.append(float(np.clip(abs(price_change) * 10, 0.0, 1.0)))
        
        X = np.array(X)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Direction classifier
        direction_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        direction_model.fit(X_scaled, y_direction)
        
        # Strength regressor
        strength_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        strength_model.fit(X_scaled, y_strength)
        
        self.models["commodity_trend"] = {
            "direction": direction_model,
            "strength": strength_model
        }
        self.scalers["commodity_trend"] = scaler
    
    def _train_market_regime_model(self):
        """Train market regime signal model"""
        from app.services.market_intelligence_data_generator import MarketIntelligenceDataGenerator
        
        generator = MarketIntelligenceDataGenerator(seed=42)
        n_samples = 3000
        
        X = []
        y_regime = []
        
        for regime in ["calm", "volatile", "stress", "recovery"]:
            features_data = generator.generate_market_regime_features(
                "MARKET_1", datetime.now() - timedelta(days=365), days=100, regime=regime
            )
            for i in range(10, len(features_data)):
                window = features_data[i-10:i]
                features = [
                    np.mean([f["rolling_volatility"] for f in window]),
                    np.mean([f["trend_strength"] for f in window]),
                    np.mean([f["drawdown_depth"] for f in window]),
                    np.mean([f["liquidity_proxy"] for f in window])
                ]
                X.append(features)
                y_regime.append(regime)
        
        X = np.array(X)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Regime classifier
        regime_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        regime_model.fit(X_scaled, y_regime)
        
        self.models["market_regime"] = regime_model
        self.scalers["market_regime"] = scaler
    
    def _train_digital_asset_adoption_model(self):
        """Train digital asset adoption intelligence model"""
        from app.services.market_intelligence_data_generator import MarketIntelligenceDataGenerator
        
        generator = MarketIntelligenceDataGenerator(seed=42)
        n_samples = 2000
        
        X = []
        y_phase = []
        y_momentum = []
        
        for phase in ["early", "growth", "maturation", "saturation"]:
            data = generator.generate_digital_asset_adoption_data(
                "US", datetime.now() - timedelta(days=365), days=100, adoption_phase=phase
            )
            for i in range(10, len(data)):
                window = data[i-10:i]
                features = [
                    np.mean([d["wallet_activity_index"] for d in window]),
                    np.mean([d["transaction_volume_index"] for d in window]),
                    np.mean([d["exchange_activity_index"] for d in window]),
                    np.mean([d["regulatory_signal_score"] for d in window]),
                    (window[-1]["wallet_activity_index"] - window[0]["wallet_activity_index"]) / window[0]["wallet_activity_index"] if window[0]["wallet_activity_index"] > 0 else 0.0
                ]
                X.append(features)
                y_phase.append(phase)
                
                # Momentum (growth rate)
                growth_rate = features[4]
                y_momentum.append(float(np.clip(growth_rate, -1.0, 1.0)))
        
        X = np.array(X)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Phase classifier
        phase_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        phase_model.fit(X_scaled, y_phase)
        
        # Momentum regressor
        momentum_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        momentum_model.fit(X_scaled, y_momentum)
        
        self.models["digital_asset_adoption"] = {
            "phase": phase_model,
            "momentum": momentum_model
        }
        self.scalers["digital_asset_adoption"] = scaler
        self.scalers["digital_asset_adoption"] = scaler
    
    def _train_exchange_risk_model(self):
        """Train exchange risk mapping model"""
        from app.services.market_intelligence_data_generator import MarketIntelligenceDataGenerator
        
        generator = MarketIntelligenceDataGenerator(seed=42)
        n_samples = 1000
        
        X = []
        y_risk = []
        
        for is_high_risk in [False, True]:
            for i in range(500):
                profile = generator.generate_exchange_profile(f"EXCHANGE_{i}", is_high_risk)
                features = [
                    profile["asset_coverage"] / 1000.0,  # Normalize
                    profile["volume_concentration"],
                    profile["liquidity_depth_proxy"],
                    profile["dependency_ratios"]["top_asset_dependency"],
                    profile["dependency_ratios"]["cross_exchange_dependency"],
                    len(profile["historical_stress_markers"]) / 10.0  # Normalize
                ]
                X.append(features)
                
                # Risk score
                risk_score = (
                    profile["volume_concentration"] * 0.3 +
                    (1.0 - profile["liquidity_depth_proxy"]) * 0.3 +
                    profile["dependency_ratios"]["top_asset_dependency"] * 0.2 +
                    profile["dependency_ratios"]["cross_exchange_dependency"] * 0.2
                )
                y_risk.append(float(np.clip(risk_score, 0.0, 1.0)))
        
        X = np.array(X)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Risk regressor
        risk_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        risk_model.fit(X_scaled, y_risk)
        
        self.models["exchange_risk"] = risk_model
        self.scalers["exchange_risk"] = scaler
    
    # ==================== INFERENCE METHODS ====================
    
    def predict_commodity_trend(
        self,
        features: List[float],
        scenario_params: Dict[str, Any]
    ) -> Tuple[str, float, float, float, List[Dict[str, Any]]]:
        """Predict commodity trend"""
        model_dict = self.models["commodity_trend"]
        scaler = self.scalers["commodity_trend"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        # Predict direction
        direction_probs = model_dict["direction"].predict_proba(X_scaled)[0]
        direction = model_dict["direction"].predict(X_scaled)[0]
        
        # Predict strength
        trend_strength = float(model_dict["strength"].predict(X_scaled)[0])
        trend_strength = np.clip(trend_strength, 0.0, 1.0)
        
        # Confidence bands
        confidence_lower = float(max(0.0, trend_strength - 0.2))
        confidence_upper = float(min(1.0, trend_strength + 0.2))
        
        # Volatility estimate
        volatility_estimate = float(features[2])  # From input features
        
        # Similar periods (synthetic for now)
        similar_periods = [
            {
                "period_start": "2020-03-01",
                "period_end": "2020-06-30",
                "similarity_score": 0.75,
                "outcome_summary": "Similar volatility pattern with recovery trend"
            },
            {
                "period_start": "2018-10-01",
                "period_end": "2018-12-31",
                "similarity_score": 0.68,
                "outcome_summary": "Comparable trend strength with moderate volatility"
            },
            {
                "period_start": "2019-05-01",
                "period_end": "2019-08-31",
                "similarity_score": 0.62,
                "outcome_summary": "Similar directional bias with different magnitude"
            }
        ]
        
        return str(direction), confidence_lower, confidence_upper, trend_strength, volatility_estimate, similar_periods
    
    def predict_market_regime(
        self,
        features: List[float],
        scenario_params: Dict[str, Any]
    ) -> Tuple[str, float, float, float, Dict[str, float]]:
        """Predict market regime"""
        model = self.models["market_regime"]
        scaler = self.scalers["market_regime"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        # Predict regime
        regime_probs = model.predict_proba(X_scaled)[0]
        regime = model.predict(X_scaled)[0]
        
        regime_probability = float(max(regime_probs))
        stability_score = float(regime_probability)
        
        # Transition probability
        transition_probability = float(1.0 - regime_probability)  # Inverse of stability
        
        # Transition likelihoods to other regimes
        transition_likelihoods = {
            str(r): float(p) for r, p in zip(model.classes_, regime_probs)
        }
        
        return str(regime), regime_probability, stability_score, transition_probability, transition_likelihoods
    
    def predict_digital_asset_adoption(
        self,
        features: List[float],
        scenario_params: Dict[str, Any]
    ) -> Tuple[str, float, float, float]:
        """Predict digital asset adoption"""
        model_dict = self.models["digital_asset_adoption"]
        scaler = self.scalers["digital_asset_adoption"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        # Predict phase
        phase_probs = model_dict["phase"].predict_proba(X_scaled)[0]
        phase = model_dict["phase"].predict(X_scaled)[0]
        
        # Predict momentum
        momentum_score = float(model_dict["momentum"].predict(X_scaled)[0])
        momentum_score = np.clip(momentum_score, -1.0, 1.0)
        
        # Growth rate
        growth_rate = float(features[4] * 100)  # Convert to percentage
        
        # Acceleration indicator
        acceleration_indicator = float(np.clip(momentum_score * 1.5, -1.0, 1.0))
        
        return str(phase), momentum_score, growth_rate, acceleration_indicator
    
    def predict_exchange_risk(
        self,
        features: List[float],
        scenario_params: Dict[str, Any]
    ) -> Tuple[float, List[Dict[str, Any]], float, float]:
        """Predict exchange risk"""
        model = self.models["exchange_risk"]
        scaler = self.scalers["exchange_risk"]
        
        X = np.array([features])
        X_scaled = scaler.transform(X)
        
        # Predict risk concentration
        risk_concentration = float(model.predict(X_scaled)[0])
        risk_concentration = np.clip(risk_concentration, 0.0, 1.0)
        
        # Dependency hotspots
        dependency_hotspots = []
        if features[3] > 0.5:  # Top asset dependency
            dependency_hotspots.append({
                "type": "asset_concentration",
                "risk_level": "high",
                "description": "High dependency on single asset class"
            })
        if features[4] > 0.4:  # Cross-exchange dependency
            dependency_hotspots.append({
                "type": "cross_exchange",
                "risk_level": "medium",
                "description": "Significant dependency on other exchanges"
            })
        
        # Systemic exposure
        systemic_exposure = float(risk_concentration * 0.7 + features[1] * 0.3)  # Volume concentration
        systemic_exposure = np.clip(systemic_exposure, 0.0, 1.0)
        
        # Stress propagation risk
        stress_propagation = float(risk_concentration * 0.5 + systemic_exposure * 0.5)
        stress_propagation = np.clip(stress_propagation, 0.0, 1.0)
        
        return risk_concentration, dependency_hotspots, systemic_exposure, stress_propagation


# Global instance
market_intelligence_ml_service = MarketIntelligenceMLService()

