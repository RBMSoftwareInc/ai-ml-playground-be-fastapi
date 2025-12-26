"""
Market Intelligence Scenario Simulation Engine
Applies controlled perturbations and compares baseline vs scenario
"""
from typing import Dict, Any, Optional


class MarketIntelligenceScenarioEngine:
    """
    Scenario simulation engine for Market Intelligence
    Applies controlled perturbations to market conditions
    """
    
    @staticmethod
    def get_scenario(scenario_name: str) -> Dict[str, Any]:
        """Get scenario parameters"""
        scenarios = {
            "baseline": {
                "name": "Baseline",
                "volatility_multiplier": 1.0,
                "demand_shock": 0.0,
                "liquidity_multiplier": 1.0,
                "description": "Normal market conditions without perturbations"
            },
            "volatility_spike": {
                "name": "Volatility Spike",
                "volatility_multiplier": 2.5,
                "demand_shock": 0.0,
                "liquidity_multiplier": 0.8,
                "description": "Sudden increase in market volatility with reduced liquidity"
            },
            "demand_shock": {
                "name": "Demand Shock",
                "volatility_multiplier": 1.5,
                "demand_shock": 0.3,  # 30% demand increase
                "liquidity_multiplier": 1.2,
                "description": "Significant increase in demand with elevated volatility"
            },
            "liquidity_drop": {
                "name": "Liquidity Drop",
                "volatility_multiplier": 1.8,
                "demand_shock": 0.0,
                "liquidity_multiplier": 0.5,
                "description": "Severe reduction in market liquidity with increased volatility"
            },
            "stress_scenario": {
                "name": "Stress Scenario",
                "volatility_multiplier": 3.0,
                "demand_shock": -0.2,  # 20% demand decrease
                "liquidity_multiplier": 0.4,
                "description": "Combined stress: high volatility, demand contraction, low liquidity"
            }
        }
        return scenarios.get(scenario_name, scenarios["baseline"])
    
    @staticmethod
    def apply_scenario_to_features(
        features: list,
        scenario_params: Dict[str, Any],
        feature_type: str
    ) -> list:
        """Apply scenario perturbations to feature vector"""
        modified_features = features.copy()
        
        if feature_type == "commodity":
            # Features: [mean_return, std_return, volatility, momentum, price_change]
            if len(modified_features) >= 3:
                # Apply volatility multiplier
                modified_features[2] *= scenario_params.get("volatility_multiplier", 1.0)
                # Apply demand shock to price change
                if len(modified_features) >= 5:
                    modified_features[4] += scenario_params.get("demand_shock", 0.0)
        
        elif feature_type == "regime":
            # Features: [rolling_vol, trend_strength, drawdown, liquidity]
            if len(modified_features) >= 1:
                modified_features[0] *= scenario_params.get("volatility_multiplier", 1.0)
            if len(modified_features) >= 4:
                modified_features[3] *= scenario_params.get("liquidity_multiplier", 1.0)
                modified_features[3] = min(1.0, max(0.0, modified_features[3]))
        
        elif feature_type == "adoption":
            # Features: [wallet, tx_volume, exchange, regulatory, growth_rate]
            if len(modified_features) >= 5:
                # Demand shock affects growth rate
                modified_features[4] += scenario_params.get("demand_shock", 0.0)
        
        elif feature_type == "exchange":
            # Features: [asset_coverage, volume_concentration, liquidity, deps...]
            if len(modified_features) >= 3:
                modified_features[2] *= scenario_params.get("liquidity_multiplier", 1.0)
                modified_features[2] = min(1.0, max(0.0, modified_features[2]))
        
        return modified_features
    
    @staticmethod
    def compare_baseline_vs_scenario(
        baseline_result: Dict[str, Any],
        scenario_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare baseline and scenario results"""
        comparison = {
            "direction_change": None,
            "confidence_change": None,
            "risk_posture_change": None,
            "magnitude_change": None
        }
        
        # Direction change
        baseline_dir = baseline_result.get("direction", baseline_result.get("signal_direction"))
        scenario_dir = scenario_result.get("direction", scenario_result.get("signal_direction"))
        if baseline_dir != scenario_dir:
            comparison["direction_change"] = f"Changed from {baseline_dir} to {scenario_dir}"
        else:
            comparison["direction_change"] = f"Remained {baseline_dir}"
        
        # Confidence change
        baseline_conf = baseline_result.get("confidence_score", baseline_result.get("confidence", {}).get("confidence_score", 0.7))
        scenario_conf = scenario_result.get("confidence_score", scenario_result.get("confidence", {}).get("confidence_score", 0.7))
        conf_diff = scenario_conf - baseline_conf
        comparison["confidence_change"] = {
            "baseline": baseline_conf,
            "scenario": scenario_conf,
            "change": conf_diff,
            "description": f"Confidence {'increased' if conf_diff > 0 else 'decreased' if conf_diff < 0 else 'unchanged'} by {abs(conf_diff):.2f}"
        }
        
        # Risk posture change
        baseline_risk = baseline_result.get("risk_score", baseline_result.get("risk_concentration_score", 0.5))
        scenario_risk = scenario_result.get("risk_score", scenario_result.get("risk_concentration_score", 0.5))
        risk_diff = scenario_risk - baseline_risk
        comparison["risk_posture_change"] = {
            "baseline": baseline_risk,
            "scenario": scenario_risk,
            "change": risk_diff,
            "description": f"Risk {'increased' if risk_diff > 0 else 'decreased' if risk_diff < 0 else 'unchanged'}"
        }
        
        # Magnitude change
        baseline_strength = baseline_result.get("strength", baseline_result.get("signal_strength", 0.5))
        scenario_strength = scenario_result.get("strength", scenario_result.get("signal_strength", 0.5))
        strength_diff = scenario_strength - baseline_strength
        comparison["magnitude_change"] = {
            "baseline": baseline_strength,
            "scenario": scenario_strength,
            "change": strength_diff,
            "description": f"Signal strength {'increased' if strength_diff > 0 else 'decreased' if strength_diff < 0 else 'unchanged'}"
        }
        
        return comparison

