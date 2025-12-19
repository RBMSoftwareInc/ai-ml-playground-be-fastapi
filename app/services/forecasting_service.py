"""
Forecasting Service for time series prediction, demand forecasting, and ETA prediction
"""
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class ForecastingService:
    """Forecasting service for time series and demand prediction"""
    
    def __init__(self):
        """Initialize forecasting models"""
        self.models = {}
        self.scalers = {}
    
    def forecast_time_series(
        self,
        historical_data: List[Dict[str, Any]],
        forecast_horizon: int = 30,
        method: str = "moving_average"
    ) -> Dict[str, Any]:
        """
        Forecast time series data
        
        Args:
            historical_data: List of {date, value} dictionaries
            forecast_horizon: Number of periods to forecast
            method: Forecasting method (moving_average, exponential_smoothing, arima)
            
        Returns:
            Forecast results with predictions and confidence intervals
        """
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        values = df['value'].values
        
        if method == "moving_average":
            # Simple moving average
            window = min(7, len(values))
            forecast = []
            for i in range(forecast_horizon):
                if len(values) >= window:
                    avg = np.mean(values[-window:])
                else:
                    avg = np.mean(values) if len(values) > 0 else 0
                forecast.append(avg)
                values = np.append(values, avg)
        
        elif method == "exponential_smoothing":
            # Exponential smoothing
            alpha = 0.3
            forecast = []
            last_value = values[-1] if len(values) > 0 else 0
            for _ in range(forecast_horizon):
                forecast.append(last_value)
        
        else:
            # Default: linear trend
            if len(values) >= 2:
                trend = (values[-1] - values[0]) / len(values)
                last_value = values[-1]
            else:
                trend = 0
                last_value = values[-1] if len(values) > 0 else 0
            
            forecast = [last_value + trend * (i + 1) for i in range(forecast_horizon)]
        
        # Calculate confidence intervals (simplified)
        std_dev = np.std(values) if len(values) > 0 else 0
        confidence_intervals = [
            [max(0, f - 1.96 * std_dev), f + 1.96 * std_dev]
            for f in forecast
        ]
        
        return {
            "forecast": [float(f) for f in forecast],
            "confidence_intervals": confidence_intervals,
            "method": method
        }
    
    def predict_eta(
        self,
        origin: str,
        destination: str,
        carrier: str,
        historical_etas: Optional[List[Dict[str, Any]]] = None,
        factors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Predict Estimated Time of Arrival
        
        Args:
            origin: Origin location
            destination: Destination location
            carrier: Carrier name
            historical_etas: Historical ETA data
            factors: Additional factors (weather, traffic, etc.)
            
        Returns:
            ETA prediction with confidence
        """
        # Base ETA (simplified - in production use route optimization)
        base_hours = 24.0  # Default
        
        # Adjust based on carrier (placeholder)
        carrier_multipliers = {
            "BlueDart": 1.0,
            "Delhivery": 1.1,
            "FedEx": 0.9,
            "DHL": 0.95
        }
        multiplier = carrier_multipliers.get(carrier, 1.0)
        
        # Adjust based on factors
        if factors:
            if factors.get("weather_delay"):
                multiplier += 0.2
            if factors.get("traffic_delay"):
                multiplier += 0.15
        
        eta_hours = base_hours * multiplier
        
        # Calculate confidence based on historical data
        confidence = 0.85
        if historical_etas and len(historical_etas) > 10:
            confidence = 0.95
        
        return {
            "eta_hours": float(eta_hours),
            "eta_date": (datetime.now() + timedelta(hours=eta_hours)).isoformat(),
            "confidence": confidence,
            "factors": [
                "Base delivery time",
                f"Carrier: {carrier}",
                "Route optimization"
            ]
        }
    
    def predict_demand(
        self,
        product_id: str,
        historical_sales: List[Dict[str, Any]],
        forecast_days: int = 30,
        seasonality: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Predict product demand
        
        Args:
            product_id: Product identifier
            historical_sales: Historical sales data
            forecast_days: Number of days to forecast
            seasonality: Seasonal factors
            
        Returns:
            Demand forecast
        """
        if not historical_sales:
            return {
                "forecast": [0] * forecast_days,
                "confidence_intervals": [[0, 0]] * forecast_days
            }
        
        df = pd.DataFrame(historical_sales)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
        
        # Use forecasting method
        result = self.forecast_time_series(
            historical_data=[
                {"date": row.get('date', datetime.now()), "value": row.get('quantity', 0)}
                for row in historical_sales
            ],
            forecast_horizon=forecast_days,
            method="exponential_smoothing"
        )
        
        return result


forecasting_service = ForecastingService()

