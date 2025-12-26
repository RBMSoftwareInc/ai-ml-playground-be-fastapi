"""
Restaurant Data Generator
Generates synthetic restaurant operational data for ML model training
Includes: order patterns, time series demand, kitchen workflow data, staffing patterns
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random


class RestaurantDataGenerator:
    """Generate synthetic restaurant operational data"""
    
    def __init__(self, seed: int = 42):
        """Initialize data generator with seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Menu items with typical prep times
        self.menu_items = [
            {"id": "burger", "name": "Classic Burger", "prep_time_min": 12, "complexity": "medium"},
            {"id": "pizza", "name": "Margherita Pizza", "prep_time_min": 18, "complexity": "high"},
            {"id": "salad", "name": "Caesar Salad", "prep_time_min": 6, "complexity": "low"},
            {"id": "pasta", "name": "Spaghetti Carbonara", "prep_time_min": 15, "complexity": "medium"},
            {"id": "wings", "name": "Buffalo Wings", "prep_time_min": 20, "complexity": "medium"},
            {"id": "tacos", "name": "Fish Tacos", "prep_time_min": 10, "complexity": "low"},
            {"id": "steak", "name": "Ribeye Steak", "prep_time_min": 22, "complexity": "high"},
            {"id": "soup", "name": "Tomato Soup", "prep_time_min": 5, "complexity": "low"},
        ]
        
        # Day of week patterns (0=Monday, 6=Sunday)
        self.day_patterns = {
            0: {"peak_start": 18, "peak_end": 21, "base_demand": 0.6},  # Monday
            1: {"peak_start": 18, "peak_end": 21, "base_demand": 0.7},
            2: {"peak_start": 18, "peak_end": 21, "base_demand": 0.75},
            3: {"peak_start": 18, "peak_end": 21, "base_demand": 0.8},
            4: {"peak_start": 18, "peak_end": 22, "base_demand": 0.9},  # Friday
            5: {"peak_start": 17, "peak_end": 22, "base_demand": 1.0},  # Saturday
            6: {"peak_start": 17, "peak_end": 21, "base_demand": 0.85},  # Sunday
        }
        
        # Weather impact (affects demand)
        self.weather_impact = {
            "sunny": 1.0,
            "cloudy": 0.95,
            "rainy": 0.85,
            "snowy": 0.70,
            "storm": 0.60,
        }
    
    def generate_historical_orders(
        self,
        start_date: datetime,
        days: int = 90,
        orders_per_day_avg: int = 150
    ) -> pd.DataFrame:
        """
        Generate historical order data
        
        Returns DataFrame with columns:
        - timestamp
        - order_id
        - items (list)
        - total_items
        - order_value
        - prep_time_required
        - hour
        - day_of_week
        - weather
        - is_peak_hour
        """
        orders = []
        current_date = start_date
        
        for day in range(days):
            day_of_week = current_date.weekday()
            pattern = self.day_patterns[day_of_week]
            
            # Generate orders for this day (6 AM to 11 PM)
            orders_today = np.random.poisson(orders_per_day_avg * pattern["base_demand"])
            
            for order_num in range(orders_today):
                # Random hour (weighted towards meal times)
                hour = self._sample_hour(day_of_week)
                minute = random.randint(0, 59)
                
                order_timestamp = current_date.replace(hour=hour, minute=minute, second=0)
                
                # Generate order items
                num_items = np.random.choice([1, 2, 2, 3, 3, 4], p=[0.2, 0.3, 0.2, 0.15, 0.1, 0.05])
                items = random.sample(self.menu_items, min(num_items, len(self.menu_items)))
                
                total_prep_time = max(item["prep_time_min"] for item in items)
                order_value = sum(random.uniform(12, 45) for _ in range(num_items))
                
                # Weather (simplified - could be more sophisticated)
                weather = random.choice(list(self.weather_impact.keys()))
                
                # Peak hour detection
                is_peak = pattern["peak_start"] <= hour < pattern["peak_end"]
                
                orders.append({
                    "timestamp": order_timestamp,
                    "order_id": f"ORD-{day:03d}-{order_num:04d}",
                    "items": [item["id"] for item in items],
                    "item_names": [item["name"] for item in items],
                    "total_items": num_items,
                    "order_value": round(order_value, 2),
                    "prep_time_required": total_prep_time,
                    "hour": hour,
                    "day_of_week": day_of_week,
                    "weather": weather,
                    "is_peak_hour": is_peak,
                })
            
            current_date += timedelta(days=1)
        
        df = pd.DataFrame(orders)
        df = df.sort_values("timestamp").reset_index(drop=True)
        return df
    
    def _sample_hour(self, day_of_week: int) -> int:
        """Sample hour with weights favoring meal times"""
        pattern = self.day_patterns[day_of_week]
        
        # Create hour weights (favor meal times: 11-14 lunch, 17-21 dinner)
        hour_weights = np.zeros(24)
        for hour in range(24):
            if 11 <= hour <= 14:  # Lunch
                hour_weights[hour] = 2.0
            elif pattern["peak_start"] <= hour < pattern["peak_end"]:  # Dinner peak
                hour_weights[hour] = 3.0
            elif 17 <= hour < 23:  # Evening
                hour_weights[hour] = 1.5
            else:
                hour_weights[hour] = 0.3
        
        hour_weights = hour_weights / hour_weights.sum()
        return np.random.choice(24, p=hour_weights)
    
    def generate_time_series_demand(
        self,
        start_time: datetime,
        hours_ahead: int = 2,
        interval_minutes: int = 15
    ) -> pd.DataFrame:
        """
        Generate demand forecast time series for next N hours
        
        Returns DataFrame with columns:
        - timestamp (15-min intervals)
        - predicted_orders
        - confidence_lower
        - confidence_upper
        - cumulative_orders
        """
        intervals = []
        current_time = start_time
        
        intervals_count = (hours_ahead * 60) // interval_minutes
        
        for i in range(intervals_count):
            hour = current_time.hour
            day_of_week = current_time.weekday()
            pattern = self.day_patterns[day_of_week]
            
            # Base demand for this interval
            base_demand = pattern["base_demand"]
            
            # Hour adjustment
            if 11 <= hour <= 14:  # Lunch
                hour_multiplier = 1.8
            elif pattern["peak_start"] <= hour < pattern["peak_end"]:  # Dinner peak
                hour_multiplier = 2.5
            elif 17 <= hour < 23:  # Evening
                hour_multiplier = 1.3
            else:
                hour_multiplier = 0.4
            
            # Predict orders for this 15-min interval
            expected_orders = base_demand * hour_multiplier * (interval_minutes / 60) * 10  # Scale factor
            
            # Add some randomness
            predicted_orders = max(0, np.random.poisson(expected_orders))
            
            # Confidence bands (simulate model uncertainty)
            confidence_width = predicted_orders * 0.25  # 25% uncertainty
            confidence_lower = max(0, int(predicted_orders - confidence_width))
            confidence_upper = int(predicted_orders + confidence_width)
            
            intervals.append({
                "timestamp": current_time,
                "predicted_orders": predicted_orders,
                "confidence_lower": confidence_lower,
                "confidence_upper": confidence_upper,
                "interval_index": i,
            })
            
            current_time += timedelta(minutes=interval_minutes)
        
        df = pd.DataFrame(intervals)
        
        # Calculate cumulative orders
        df["cumulative_orders"] = df["predicted_orders"].cumsum()
        
        return df
    
    def generate_kitchen_workflow_data(
        self,
        current_orders: List[Dict[str, Any]],
        staff_count: int = 4
    ) -> Dict[str, Any]:
        """
        Generate current kitchen workflow state
        
        Returns:
        - active_orders: Orders currently being prepared
        - queue_wait_time: Estimated wait time for new orders
        - kitchen_capacity_utilization: Current capacity usage
        - bottleneck_items: Items causing delays
        """
        # Calculate current kitchen load
        total_prep_time = sum(order.get("prep_time_required", 15) for order in current_orders)
        
        # Assume each staff member can handle 1 order every 15 minutes on average
        staff_capacity = staff_count * 15  # minutes of prep capacity per 15-min window
        utilization = min(1.0, total_prep_time / staff_capacity) if staff_capacity > 0 else 0.0
        
        # Estimate wait time based on queue
        if len(current_orders) > 0:
            avg_prep_time = total_prep_time / len(current_orders)
            queue_wait_time = avg_prep_time * len(current_orders) / staff_count
        else:
            queue_wait_time = 0
        
        # Identify bottleneck items (items with longest prep times that are common)
        item_counts = {}
        for order in current_orders:
            for item in order.get("items", []):
                item_counts[item] = item_counts.get(item, 0) + 1
        
        bottleneck_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "active_orders_count": len(current_orders),
            "queue_wait_time_minutes": round(queue_wait_time, 1),
            "kitchen_capacity_utilization": round(utilization, 2),
            "bottleneck_items": [item for item, count in bottleneck_items],
            "staff_count": staff_count,
            "total_prep_time_minutes": round(total_prep_time, 1),
        }


# Global instance
restaurant_data_generator = RestaurantDataGenerator()

