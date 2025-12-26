"""
Travel AI ML Service
ML models for travel use cases - trained offline, inference only
"""
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.travel_data_generator import TravelDataGenerator


class TravelMLService:
    """
    ML service for Travel AI modules
    Models are pre-trained on synthetic data and loaded for inference
    """
    
    def __init__(self):
        """Initialize ML service with pre-trained models"""
        self.models = {}
        self.scalers = {}
        self.model_version = "1.0.0"
        self.models_dir = settings.MODELS_DIR
        os.makedirs(self.models_dir, exist_ok=True)
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize and train models on synthetic data"""
        # Use Case 1: Dynamic Pricing
        self._train_dynamic_pricing_model()
        
        # Use Case 2: Demand Forecasting
        self._train_demand_forecast_model()
        
        # Use Case 3: Personalized Recommendations (uses embeddings, no traditional ML)
        # Use Case 4: AI Concierge (uses NLP/LLM, no traditional ML)
        
        # Use Case 5: Route Optimization
        self._train_route_optimization_model()
        
        # Use Case 6: Hotel Matching (uses embeddings, no traditional ML)
    
    # ==================== USE CASE 1: DYNAMIC PRICING ====================
    
    def _train_dynamic_pricing_model(self):
        """Train dynamic pricing model on synthetic data"""
        generator = TravelDataGenerator(seed=42)
        n_samples = 5000
        
        X = []
        y = []
        
        base_date = datetime.now()
        for i in range(n_samples):
            event_date = base_date + timedelta(days=np.random.randint(-365, 365))
            base_price = np.random.uniform(50, 500)
            
            pricing_event = generator.generate_pricing_event(
                f"PROP_{i % 100}",
                event_date,
                base_price
            )
            
            # Features: demand_level, booking_velocity, seasonality_factor, event_impact,
            #           lead_time_days, occupancy_rate, competitor_price_ratio
            features = [
                pricing_event["demand_level"],
                pricing_event["booking_velocity"] / 20.0,  # Normalize
                pricing_event["seasonality_factor"],
                pricing_event["event_impact"],
                pricing_event["lead_time_days"] / 365.0,  # Normalize
                pricing_event["occupancy_rate"],
                pricing_event["competitor_price_avg"] / base_price  # Ratio
            ]
            
            X.append(features)
            
            # Target: optimal price multiplier (0.5 to 2.0)
            optimal_multiplier = pricing_event["actual_price"] / base_price
            y.append(optimal_multiplier)
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_scaled, y)
        
        self.models["dynamic_pricing"] = model
        self.scalers["dynamic_pricing"] = scaler
    
    def predict_dynamic_pricing(
        self,
        features: List[float],
        scenario_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, float, float, float, Dict[str, Any]]:
        """
        Predict optimal price range
        
        Returns:
            (price_min, price_max, price_optimal, confidence_score, model_metadata)
        """
        if scenario_params:
            # Adjust features based on scenario
            if "demand_surge" in scenario_params:
                features[0] = min(1.0, features[0] + scenario_params["demand_surge"])
            if "event_impact" in scenario_params:
                features[3] = scenario_params["event_impact"]
        
        X = np.array(features).reshape(1, -1)
        X_scaled = self.scalers["dynamic_pricing"].transform(X)
        
        price_multiplier = self.models["dynamic_pricing"].predict(X_scaled)[0]
        
        # Get feature importance
        feature_importance = self.models["dynamic_pricing"].feature_importances_
        
        # Calculate price range (±15% around optimal)
        price_optimal = features[6] * price_multiplier  # features[6] is base_price
        price_min = price_optimal * 0.85
        price_max = price_optimal * 1.15
        
        # Confidence based on feature quality
        confidence_score = float(np.clip(
            0.7 + (1.0 - features[0]) * 0.2 + features[2] * 0.1,  # Higher confidence with stable demand
            0.5, 1.0
        ))
        
        model_metadata = {
            "model_type": "RandomForestRegressor",
            "model_version": self.model_version,
            "feature_importance": {
                "demand_level": float(feature_importance[0]),
                "booking_velocity": float(feature_importance[1]),
                "seasonality": float(feature_importance[2]),
                "event_impact": float(feature_importance[3]),
                "lead_time": float(feature_importance[4]),
                "occupancy": float(feature_importance[5]),
                "competitor_ratio": float(feature_importance[6])
            }
        }
        
        return float(price_min), float(price_max), float(price_optimal), confidence_score, model_metadata
    
    # ==================== USE CASE 2: DEMAND FORECASTING ====================
    
    def _train_demand_forecast_model(self):
        """Train demand forecasting model on synthetic data"""
        generator = TravelDataGenerator(seed=42)
        n_samples = 3000
        
        X = []
        y = []
        
        base_date = datetime.now()
        for i in range(n_samples):
            travel_date = base_date + timedelta(days=np.random.randint(0, 365))
            booking_date = travel_date - timedelta(days=np.random.randint(1, 180))
            
            booking_history = generator.generate_booking_history(
                f"PROP_{i % 100}",
                booking_date,
                travel_date
            )
            
            # Features: lead_time_days, season_encoded, holiday_flag, event_flag, weather_impact
            season_encoded = {"peak": 1.0, "shoulder": 0.5, "off": 0.0}.get(booking_history["season"], 0.5)
            
            features = [
                booking_history["lead_time_days"] / 180.0,  # Normalize
                season_encoded,
                1.0 if booking_history["holiday_flag"] else 0.0,
                1.0 if booking_history["event_flag"] else 0.0,
                booking_history["weather_impact"]
            ]
            
            X.append(features)
            
            # Target: booking count
            y.append(booking_history["booking_count"])
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_scaled, y)
        
        self.models["demand_forecast"] = model
        self.scalers["demand_forecast"] = scaler
    
    def predict_demand_forecast(
        self,
        features: List[float],
        scenario_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, float, float, str, List[Dict[str, Any]], float, float, Dict[str, Any]]:
        """
        Predict demand forecast
        
        Returns:
            (forecasted_demand, confidence_lower, confidence_upper, trend_direction,
             risk_zones, holiday_impact, event_impact, model_metadata)
        """
        if scenario_params:
            # Adjust features based on scenario
            if "holiday_boost" in scenario_params:
                features[2] = 1.0
            if "event_boost" in scenario_params:
                features[3] = 1.0
        
        X = np.array(features).reshape(1, -1)
        X_scaled = self.scalers["demand_forecast"].transform(X)
        
        forecasted_demand = self.models["demand_forecast"].predict(X_scaled)[0]
        forecasted_demand = max(0.0, forecasted_demand)  # Non-negative
        
        # Confidence bands (±20% for now, would use prediction intervals in production)
        confidence_lower = forecasted_demand * 0.8
        confidence_upper = forecasted_demand * 1.2
        
        # Trend direction (simplified - would use time series analysis in production)
        if features[1] > 0.7:  # Peak season
            trend_direction = "increasing"
        elif features[1] < 0.3:  # Off season
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"
        
        # Risk zones
        risk_zones = [
            {"period": "next_7_days", "risk_level": "medium", "demand": forecasted_demand * 0.9},
            {"period": "next_30_days", "risk_level": "low", "demand": forecasted_demand},
            {"period": "next_90_days", "risk_level": "medium", "demand": forecasted_demand * 1.1}
        ]
        
        holiday_impact = float(features[2] * 0.3)  # 30% boost if holiday
        event_impact = float(features[3] * 0.2)  # 20% boost if event
        
        model_metadata = {
            "model_type": "RandomForestRegressor",
            "model_version": self.model_version,
            "forecast_horizon_days": int(features[0] * 180)
        }
        
        return (
            float(forecasted_demand),
            float(confidence_lower),
            float(confidence_upper),
            trend_direction,
            risk_zones,
            holiday_impact,
            event_impact,
            model_metadata
        )
    
    # ==================== USE CASE 5: ROUTE OPTIMIZATION ====================
    
    def _train_route_optimization_model(self):
        """Train route optimization model on synthetic data"""
        generator = TravelDataGenerator(seed=42)
        n_samples = 2000
        
        X = []
        y = []
        
        base_date = datetime.now()
        for i in range(n_samples):
            segment_date = base_date + timedelta(days=np.random.randint(0, 30))
            
            route_segment = generator.generate_route_segment(
                f"ROUTE_{i % 50}",
                f"ORIGIN_{i % 10}",
                f"DEST_{i % 10}",
                segment_date
            )
            
            # Features: distance_km, disruption_risk, weather_impact, traffic_encoded
            traffic_encoded = {"normal": 0.0, "heavy": 0.5, "light": -0.2}.get(route_segment["traffic_conditions"], 0.0)
            
            features = [
                route_segment["distance_km"] / 2000.0,  # Normalize
                route_segment["disruption_risk"],
                route_segment["weather_impact"],
                traffic_encoded
            ]
            
            X.append(features)
            
            # Target: delay risk score (0.0 to 1.0)
            delay_risk = (
                route_segment["disruption_risk"] * 0.5 +
                abs(route_segment["weather_impact"]) * 0.3 +
                (0.5 if route_segment["traffic_conditions"] == "heavy" else 0.0) * 0.2
            )
            y.append(min(1.0, delay_risk))
        
        X = np.array(X)
        y = np.array(y)
        
        # Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_scaled, y)
        
        self.models["route_optimization"] = model
        self.scalers["route_optimization"] = scaler
    
    def predict_route_delay_risk(
        self,
        features: List[float],
        scenario_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Predict delay risk for route
        
        Returns:
            (delay_risk_score, model_metadata)
        """
        if scenario_params:
            # Adjust features based on scenario
            if "disruption_boost" in scenario_params:
                features[1] = min(1.0, features[1] + scenario_params["disruption_boost"])
            if "weather_impact" in scenario_params:
                features[2] = scenario_params["weather_impact"]
        
        X = np.array(features).reshape(1, -1)
        X_scaled = self.scalers["route_optimization"].transform(X)
        
        delay_risk_score = self.models["route_optimization"].predict(X_scaled)[0]
        delay_risk_score = float(np.clip(delay_risk_score, 0.0, 1.0))
        
        model_metadata = {
            "model_type": "RandomForestRegressor",
            "model_version": self.model_version
        }
        
        return delay_risk_score, model_metadata

