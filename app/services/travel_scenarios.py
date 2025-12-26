"""
Travel AI Scenario Catalog
User-driven scenarios that map to backend parameters
"""
from typing import Dict, Any, Optional


class TravelScenarioCatalog:
    """Scenario catalog for Travel AI modules"""
    
    @staticmethod
    def get_dynamic_pricing_scenarios() -> Dict[str, Dict[str, Any]]:
        """Get available scenarios for dynamic pricing"""
        return {
            "baseline": {
                "name": "Baseline Conditions",
                "description": "Normal market conditions with standard demand patterns",
                "params": {}
            },
            "peak_season": {
                "name": "Peak Season",
                "description": "High-demand peak travel season",
                "params": {
                    "demand_surge": 0.4,
                    "seasonality_impact": 1.3
                }
            },
            "low_season": {
                "name": "Low Season",
                "description": "Low-demand off-peak travel season",
                "params": {
                    "demand_surge": -0.3,
                    "seasonality_impact": 0.7
                }
            },
            "event_surge": {
                "name": "Event-Driven Surge",
                "description": "Major event causing demand spike",
                "params": {
                    "demand_surge": 0.6,
                    "event_impact": 0.5
                }
            },
            "last_minute": {
                "name": "Last-Minute Booking",
                "description": "Short lead time with high urgency",
                "params": {
                    "lead_time_factor": 0.1,
                    "demand_surge": 0.2
                }
            }
        }
    
    @staticmethod
    def get_demand_forecast_scenarios() -> Dict[str, Dict[str, Any]]:
        """Get available scenarios for demand forecasting"""
        return {
            "baseline": {
                "name": "Baseline Forecast",
                "description": "Standard demand forecast based on historical patterns",
                "params": {}
            },
            "holiday_boost": {
                "name": "Holiday Period",
                "description": "Upcoming holiday period expected to boost demand",
                "params": {
                    "holiday_boost": 0.3
                }
            },
            "event_boost": {
                "name": "Special Event",
                "description": "Special event in the area expected to increase demand",
                "params": {
                    "event_boost": 0.25
                }
            },
            "economic_downturn": {
                "name": "Economic Downturn",
                "description": "Economic conditions reducing travel demand",
                "params": {
                    "demand_reduction": 0.2
                }
            },
            "seasonal_transition": {
                "name": "Seasonal Transition",
                "description": "Transition between peak and off-peak seasons",
                "params": {
                    "volatility_increase": 0.15
                }
            }
        }
    
    @staticmethod
    def get_route_optimization_scenarios() -> Dict[str, Dict[str, Any]]:
        """Get available scenarios for route optimization"""
        return {
            "baseline": {
                "name": "Baseline Conditions",
                "description": "Normal traffic and weather conditions",
                "params": {}
            },
            "heavy_traffic": {
                "name": "Heavy Traffic",
                "description": "Heavy traffic conditions expected",
                "params": {
                    "disruption_boost": 0.3,
                    "traffic_impact": 0.4
                }
            },
            "weather_disruption": {
                "name": "Weather Disruption",
                "description": "Adverse weather conditions affecting routes",
                "params": {
                    "weather_impact": 0.5,
                    "disruption_boost": 0.4
                }
            },
            "peak_travel": {
                "name": "Peak Travel Period",
                "description": "High-traffic peak travel period",
                "params": {
                    "disruption_boost": 0.2,
                    "traffic_impact": 0.3
                }
            },
            "optimal_conditions": {
                "name": "Optimal Conditions",
                "description": "Ideal travel conditions with minimal disruptions",
                "params": {
                    "disruption_boost": -0.2,
                    "weather_impact": -0.1
                }
            }
        }
    
    @staticmethod
    def get_all_scenarios() -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Get all available scenarios for all modules"""
        return {
            "dynamic_pricing": TravelScenarioCatalog.get_dynamic_pricing_scenarios(),
            "demand_forecast": TravelScenarioCatalog.get_demand_forecast_scenarios(),
            "route_optimization": TravelScenarioCatalog.get_route_optimization_scenarios()
        }
    
    @staticmethod
    def get_scenario_params(module: str, scenario_name: str) -> Optional[Dict[str, Any]]:
        """Get scenario parameters for a specific module and scenario"""
        all_scenarios = TravelScenarioCatalog.get_all_scenarios()
        if module in all_scenarios and scenario_name in all_scenarios[module]:
            return all_scenarios[module][scenario_name].get("params", {})
        return None


# Global instance
travel_scenario_catalog = TravelScenarioCatalog()

