"""
Restaurant ML Service
Demand forecasting and kitchen workflow optimization using time series models
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os
from app.core.config import settings
from app.services.restaurant_data_generator import restaurant_data_generator


class RestaurantMLService:
    """
    ML service for restaurant demand forecasting and workflow optimization
    
    Models:
    - Demand Forecasting: Time series model predicting orders per 15-min interval
    - Kitchen Optimization: Rule-based + ML for workflow recommendations
    """
    
    def __init__(self):
        """Initialize restaurant ML models"""
        self.models_dir = settings.MODELS_DIR
        os.makedirs(self.models_dir, exist_ok=True)
        
        self.models = {}
        self.scalers = {}
        self.model_version = "1.0.0"
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize and train demand forecasting models"""
        # Generate training data
        start_date = datetime.now() - timedelta(days=90)
        historical_orders = restaurant_data_generator.generate_historical_orders(
            start_date=start_date,
            days=90
        )
        
        # Train demand forecasting model
        self._train_demand_forecasting_model(historical_orders)
    
    def _train_demand_forecasting_model(self, historical_orders: pd.DataFrame):
        """Train model to predict orders per 15-minute interval"""
        # Aggregate orders to 15-minute intervals
        historical_orders['timestamp'] = pd.to_datetime(historical_orders['timestamp'])
        historical_orders['interval_start'] = historical_orders['timestamp'].dt.floor('15min')
        
        # Group by interval
        interval_data = historical_orders.groupby('interval_start').agg({
            'order_id': 'count',  # Number of orders
            'total_items': 'sum',
            'order_value': 'sum',
            'hour': 'first',
            'day_of_week': 'first',
            'is_peak_hour': 'first',
        }).reset_index()
        interval_data.columns = ['timestamp', 'order_count', 'total_items', 'order_value', 'hour', 'day_of_week', 'is_peak_hour']
        
        # Extract features
        interval_data['hour_sin'] = np.sin(2 * np.pi * interval_data['hour'] / 24)
        interval_data['hour_cos'] = np.cos(2 * np.pi * interval_data['hour'] / 24)
        interval_data['day_sin'] = np.sin(2 * np.pi * interval_data['day_of_week'] / 7)
        interval_data['day_cos'] = np.cos(2 * np.pi * interval_data['day_of_week'] / 7)
        
        # Lag features (previous interval's order count)
        interval_data = interval_data.sort_values('timestamp')
        interval_data['prev_order_count'] = interval_data['order_count'].shift(1).fillna(0)
        interval_data['prev_2_order_count'] = interval_data['order_count'].shift(2).fillna(0)
        
        # Rolling averages
        interval_data['rolling_mean_4'] = interval_data['order_count'].rolling(window=4, min_periods=1).mean()
        interval_data['rolling_mean_8'] = interval_data['order_count'].rolling(window=8, min_periods=1).mean()
        
        # Prepare features
        feature_cols = [
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
            'is_peak_hour',
            'prev_order_count', 'prev_2_order_count',
            'rolling_mean_4', 'rolling_mean_8'
        ]
        
        X = interval_data[feature_cols].fillna(0).values
        y = interval_data['order_count'].values
        
        # Train model
        self.models['demand_forecast'] = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        self.scalers['demand_forecast'] = StandardScaler()
        X_scaled = self.scalers['demand_forecast'].fit_transform(X)
        
        self.models['demand_forecast'].fit(X_scaled, y)
        
        # Save feature columns for later use
        self.feature_columns = feature_cols
        
        print("✓ Trained restaurant demand forecasting model")
    
    def predict_demand_forecast(
        self,
        start_time: datetime,
        hours_ahead: int = 2,
        interval_minutes: int = 15
    ) -> pd.DataFrame:
        """
        Predict demand for next N hours in 15-minute intervals
        
        Returns DataFrame with predicted orders and confidence bands
        """
        intervals = []
        current_time = start_time
        
        intervals_count = (hours_ahead * 60) // interval_minutes
        
        # Get historical context (last 8 intervals for rolling averages)
        historical_context = self._get_historical_context(current_time)
        
        for i in range(intervals_count):
            hour = current_time.hour
            day_of_week = current_time.weekday()
            
            # Prepare features for this interval
            hour_sin = np.sin(2 * np.pi * hour / 24)
            hour_cos = np.cos(2 * np.pi * hour / 24)
            day_sin = np.sin(2 * np.pi * day_of_week / 7)
            day_cos = np.cos(2 * np.pi * day_of_week / 7)
            
            # Check if peak hour
            pattern = restaurant_data_generator.day_patterns[day_of_week]
            is_peak_hour = pattern["peak_start"] <= hour < pattern["peak_end"]
            
            # Previous order counts (use historical context or predicted)
            if i == 0:
                prev_order_count = historical_context.get('prev_1', 8.0)
                prev_2_order_count = historical_context.get('prev_2', 7.5)
                rolling_mean_4 = historical_context.get('rolling_mean_4', 8.0)
                rolling_mean_8 = historical_context.get('rolling_mean_8', 7.8)
            elif i == 1:
                prev_order_count = intervals[i-1]['predicted_orders']
                prev_2_order_count = historical_context.get('prev_1', 8.0)
                rolling_mean_4 = (historical_context.get('rolling_mean_4', 8.0) * 3 + intervals[i-1]['predicted_orders']) / 4
                rolling_mean_8 = (historical_context.get('rolling_mean_8', 7.8) * 7 + intervals[i-1]['predicted_orders']) / 8
            else:
                prev_order_count = intervals[i-1]['predicted_orders']
                prev_2_order_count = intervals[i-2]['predicted_orders']
                # Update rolling averages
                recent_orders = [intervals[j]['predicted_orders'] for j in range(max(0, i-3), i)]
                if len(recent_orders) >= 4:
                    rolling_mean_4 = np.mean(recent_orders[-4:])
                else:
                    rolling_mean_4 = (rolling_mean_4 * (4 - len(recent_orders)) + sum(recent_orders)) / 4
                
                recent_8 = [intervals[j]['predicted_orders'] for j in range(max(0, i-7), i)]
                if len(recent_8) >= 8:
                    rolling_mean_8 = np.mean(recent_8[-8:])
                else:
                    rolling_mean_8 = (rolling_mean_8 * (8 - len(recent_8)) + sum(recent_8)) / 8
            
            # Create feature vector
            features = np.array([[
                hour_sin, hour_cos, day_sin, day_cos,
                float(is_peak_hour),
                prev_order_count, prev_2_order_count,
                rolling_mean_4, rolling_mean_8
            ]])
            
            # Scale features
            features_scaled = self.scalers['demand_forecast'].transform(features)
            
            # Predict
            predicted_orders = self.models['demand_forecast'].predict(features_scaled)[0]
            predicted_orders = max(0, int(round(predicted_orders)))
            
            # Calculate confidence bands (model uncertainty estimation)
            # In production, would use prediction intervals from ensemble
            confidence_width = predicted_orders * 0.25  # 25% uncertainty
            confidence_lower = max(0, int(predicted_orders - confidence_width))
            confidence_upper = int(predicted_orders + confidence_width)
            
            intervals.append({
                "timestamp": current_time,
                "predicted_orders": predicted_orders,
                "confidence_lower": confidence_lower,
                "confidence_upper": confidence_upper,
                "interval_index": i,
                "hour": hour,
                "day_of_week": day_of_week,
                "is_peak_hour": is_peak_hour,
            })
            
            current_time += timedelta(minutes=interval_minutes)
        
        df = pd.DataFrame(intervals)
        df["cumulative_orders"] = df["predicted_orders"].cumsum()
        
        return df
    
    def _get_historical_context(self, current_time: datetime) -> Dict[str, float]:
        """Get historical order context for feature engineering"""
        # In production, would fetch from database
        # For now, return reasonable defaults
        return {
            'prev_1': 8.0,
            'prev_2': 7.5,
            'rolling_mean_4': 8.0,
            'rolling_mean_8': 7.8,
        }
    
    def generate_kitchen_recommendations(
        self,
        demand_forecast: pd.DataFrame,
        current_kitchen_state: Dict[str, Any],
        current_time: datetime
    ) -> List[Dict[str, Any]]:
        """
        Generate AI recommendations for kitchen workflow optimization
        
        Returns list of recommendations with:
        - type: "prep_action", "staffing", "workflow"
        - title: Short description
        - reasoning: Why this recommendation
        - confidence: Confidence level (0-1)
        - impact_if_ignored: What happens if ignored
        - suggested_action: What to do
        """
        recommendations = []
        
        # Analyze demand forecast for spikes
        forecast_peak_intervals = demand_forecast.nlargest(3, 'predicted_orders')
        
        # Check for upcoming demand spike
        for idx, interval in forecast_peak_intervals.iterrows():
            time_until_spike = (interval['timestamp'] - current_time).total_seconds() / 60  # minutes
            
            if 15 <= time_until_spike <= 45:  # Spike coming in 15-45 minutes
                predicted_orders = interval['predicted_orders']
                current_capacity = current_kitchen_state.get('kitchen_capacity_utilization', 0.5)
                
                if predicted_orders > 12 and current_capacity < 0.7:  # Significant spike predicted
                    recommendations.append({
                        "type": "prep_action",
                        "title": f"Pre-prep high-demand items for {interval['timestamp'].strftime('%H:%M')} spike",
                        "reasoning": f"Forecast shows {predicted_orders} orders expected at {interval['timestamp'].strftime('%H:%M')} (peak hour). Current kitchen utilization is {current_capacity:.0%}. Pre-prepping reduces wait time by 30-40%.",
                        "confidence": min(0.95, 0.70 + (predicted_orders / 20) * 0.25),
                        "impact_if_ignored": f"Wait times could increase to {int(predicted_orders * 2.5)} minutes. Customer satisfaction drops. Kitchen stress increases.",
                        "suggested_action": "Begin pre-prepping 8-10 high-demand items (burgers, pizzas) now. Allocate 1 staff member to prep station.",
                        "time_until_impact": int(time_until_spike),
                        "predicted_orders": int(predicted_orders),
                    })
        
        # Staffing recommendations
        total_predicted_orders = demand_forecast['predicted_orders'].sum()
        current_staff = current_kitchen_state.get('staff_count', 4)
        
        # Optimal staff calculation: ~4 orders per staff member per 15-min interval during peak
        optimal_staff = max(3, int(np.ceil(total_predicted_orders / (2 * 8))))  # 8 orders per staff per hour
        
        if optimal_staff > current_staff:
            recommendations.append({
                "type": "staffing",
                "title": f"Increase kitchen staff from {current_staff} to {optimal_staff}",
                "reasoning": f"Forecast predicts {int(total_predicted_orders)} orders over next 2 hours. Current staff of {current_staff} may create bottlenecks during peak periods.",
                "confidence": 0.85,
                "impact_if_ignored": f"Kitchen capacity utilization could reach 95%+ during peak. Wait times increase 40-60%. Risk of order backlog and customer complaints.",
                "suggested_action": f"Schedule {optimal_staff - current_staff} additional kitchen staff to start in next 30 minutes.",
                "current_staff": current_staff,
                "recommended_staff": optimal_staff,
            })
        
        # Workflow optimization
        bottleneck_items = current_kitchen_state.get('bottleneck_items', [])
        if bottleneck_items and len(bottleneck_items) > 0:
            recommendations.append({
                "type": "workflow",
                "title": f"Reallocate prep resources for {bottleneck_items[0]}",
                "reasoning": f"{bottleneck_items[0]} is currently the bottleneck item. Forecast shows continued demand. Pre-allocating prep station for this item reduces queue time.",
                "confidence": 0.80,
                "impact_if_ignored": f"Orders with {bottleneck_items[0]} may experience 15-20 minute delays. Overall kitchen throughput reduced.",
                "suggested_action": f"Dedicate one prep station specifically for {bottleneck_items[0]} preparation. Pre-prep base components.",
                "bottleneck_item": bottleneck_items[0],
            })
        
        # Sort by confidence (highest first)
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return recommendations
    
    def simulate_what_if_scenario(
        self,
        recommendations: List[Dict[str, Any]],
        accepted_recommendations: List[str],
        demand_forecast: Optional[pd.DataFrame],
        current_kitchen_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate operational impact of accepting/ignoring recommendations
        
        Returns:
        - avg_wait_time: Average wait time (minutes)
        - max_wait_time: Maximum wait time (minutes)
        - order_backlog: Number of orders in backlog
        - customer_satisfaction_score: 0-100
        - kitchen_stress_level: 0-100
        - waste_percentage: Food waste percentage
        """
        # Base metrics
        base_avg_wait = 18.0  # minutes
        base_max_wait = 35.0
        base_backlog = 2
        base_satisfaction = 85
        base_stress = 40
        base_waste = 8.0  # percentage
        
        # Calculate impact of accepted recommendations
        prep_actions_accepted = any(r['type'] == 'prep_action' and r['title'] in accepted_recommendations 
                                    for r in recommendations)
        staffing_accepted = any(r['type'] == 'staffing' and r['title'] in accepted_recommendations 
                               for r in recommendations)
        workflow_accepted = any(r['type'] == 'workflow' and r['title'] in accepted_recommendations 
                               for r in recommendations)
        
        # Apply improvements
        avg_wait = base_avg_wait
        max_wait = base_max_wait
        backlog = base_backlog
        satisfaction = base_satisfaction
        stress = base_stress
        waste = base_waste
        
        if prep_actions_accepted:
            avg_wait *= 0.70  # 30% reduction
            max_wait *= 0.65
            satisfaction += 8
            stress -= 15
        
        if staffing_accepted:
            avg_wait *= 0.75  # 25% reduction
            max_wait *= 0.70
            backlog = max(0, backlog - 3)
            satisfaction += 10
            stress -= 20
        
        if workflow_accepted:
            avg_wait *= 0.85  # 15% reduction
            max_wait *= 0.80
            satisfaction += 5
            stress -= 10
        
        # If no recommendations accepted, simulate worse conditions
        if not accepted_recommendations and demand_forecast is not None and len(demand_forecast) > 0:
            peak_orders = demand_forecast['predicted_orders'].max()
            if peak_orders > 15:
                avg_wait *= 1.40  # 40% increase
                max_wait *= 1.50
                backlog += 5
                satisfaction -= 15
                stress += 25
                waste += 3.0  # More waste due to rush
        
        return {
            "avg_wait_time_minutes": round(avg_wait, 1),
            "max_wait_time_minutes": round(max_wait, 1),
            "order_backlog": max(0, int(backlog)),
            "customer_satisfaction_score": max(0, min(100, int(satisfaction))),
            "kitchen_stress_level": max(0, min(100, int(stress))),
            "waste_percentage": round(waste, 1),
        }


# Global instance
restaurant_ml_service = RestaurantMLService()

