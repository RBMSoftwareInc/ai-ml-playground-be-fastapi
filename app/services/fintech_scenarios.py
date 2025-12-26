"""
Fintech Scenario Catalog
User-driven scenarios that map to backend parameters
Scenarios are NOT data-driven - they adjust model behavior
"""
from typing import Dict, Any
from enum import Enum


class CreditRiskScenario(str, Enum):
    """Credit risk scenarios"""
    STABLE_ECONOMY = "stable_economy"
    RISING_INTEREST_RATES = "rising_interest_rates"
    ECONOMIC_DOWNTURN = "economic_downturn"
    HIGH_INFLATION = "high_inflation"


class FraudDetectionScenario(str, Enum):
    """Fraud detection scenarios"""
    NORMAL_BEHAVIOR = "normal_behavior"
    VELOCITY_SPIKE = "velocity_spike"
    GEO_SHIFT = "geo_shift"
    COORDINATED_FRAUD = "coordinated_fraud"


class KYCAMLScenario(str, Enum):
    """KYC/AML scenarios"""
    LOW_RISK_RETAIL = "low_risk_retail"
    HIGH_RISK_JURISDICTION = "high_risk_jurisdiction"
    PEP_PROFILE = "pep_profile"
    NETWORKED_ENTITY = "networked_entity"


class MarketSignalScenario(str, Enum):
    """Market signal scenarios"""
    CALM_MARKET = "calm_market"
    NEWS_UNCERTAINTY = "news_uncertainty"
    LIQUIDITY_STRESS = "liquidity_stress"
    MACRO_SHOCK = "macro_shock"


class RegimeSimulationScenario(str, Enum):
    """Regime simulation scenarios"""
    VOLATILITY_EXPANSION = "volatility_expansion"
    CORRELATION_BREAKDOWN = "correlation_breakdown"
    LIQUIDITY_FREEZE = "liquidity_freeze"


class FintechScenarioCatalog:
    """Scenario catalog for all Fintech modules"""
    
    @staticmethod
    def get_credit_risk_scenario(scenario_name: str) -> Dict[str, Any]:
        """Get credit risk scenario parameters"""
        scenarios = {
            "stable_economy": {
                "name": "Stable Economy",
                "macro_context": {
                    "interest_rate_level": 2.5,
                    "inflation_index": 0.2,
                    "unemployment_index": 0.15,
                    "economic_stress_level": 0.2
                },
                "default_probability_sensitivity": 1.0,  # Baseline
                "confidence_degradation": 0.0,
                "description": "Normal economic conditions with stable interest rates and low inflation"
            },
            "rising_interest_rates": {
                "name": "Rising Interest Rates",
                "macro_context": {
                    "interest_rate_level": 5.5,
                    "inflation_index": 0.4,
                    "unemployment_index": 0.25,
                    "economic_stress_level": 0.5
                },
                "default_probability_sensitivity": 1.4,  # 40% increase
                "confidence_degradation": 0.1,
                "description": "Rising interest rates increase borrowing costs and default risk"
            },
            "economic_downturn": {
                "name": "Economic Downturn",
                "macro_context": {
                    "interest_rate_level": 1.5,
                    "inflation_index": 0.3,
                    "unemployment_index": 0.6,
                    "economic_stress_level": 0.8
                },
                "default_probability_sensitivity": 2.0,  # 100% increase
                "confidence_degradation": 0.2,
                "description": "Economic recession with high unemployment and financial stress"
            },
            "high_inflation": {
                "name": "High Inflation Environment",
                "macro_context": {
                    "interest_rate_level": 7.0,
                    "inflation_index": 0.8,
                    "unemployment_index": 0.35,
                    "economic_stress_level": 0.6
                },
                "default_probability_sensitivity": 1.6,  # 60% increase
                "confidence_degradation": 0.15,
                "description": "High inflation erodes purchasing power and increases financial stress"
            }
        }
        return scenarios.get(scenario_name, scenarios["stable_economy"])
    
    @staticmethod
    def get_fraud_detection_scenario(scenario_name: str) -> Dict[str, Any]:
        """Get fraud detection scenario parameters"""
        scenarios = {
            "normal_behavior": {
                "name": "Normal Transaction Behavior",
                "velocity_threshold_multiplier": 1.0,
                "geo_deviation_weight": 1.0,
                "device_trust_weight": 1.0,
                "fraud_probability_bias": 0.0,
                "description": "Standard transaction patterns with normal velocity and location"
            },
            "velocity_spike": {
                "name": "Sudden Velocity Spike",
                "velocity_threshold_multiplier": 0.5,  # Lower threshold
                "geo_deviation_weight": 1.2,
                "device_trust_weight": 1.1,
                "fraud_probability_bias": 0.2,  # Increase fraud probability
                "description": "Unusual transaction velocity indicating potential fraud"
            },
            "geo_shift": {
                "name": "Geo-Location Shift",
                "velocity_threshold_multiplier": 1.0,
                "geo_deviation_weight": 2.0,  # Double weight on geo
                "device_trust_weight": 1.5,
                "fraud_probability_bias": 0.3,
                "description": "Transaction from unusual geographic location"
            },
            "coordinated_fraud": {
                "name": "Coordinated Fraud Pattern",
                "velocity_threshold_multiplier": 0.3,
                "geo_deviation_weight": 1.5,
                "device_trust_weight": 2.0,
                "fraud_probability_bias": 0.4,
                "description": "Pattern suggesting coordinated fraud attack across multiple accounts"
            }
        }
        return scenarios.get(scenario_name, scenarios["normal_behavior"])
    
    @staticmethod
    def get_kyc_aml_scenario(scenario_name: str) -> Dict[str, Any]:
        """Get KYC/AML scenario parameters"""
        scenarios = {
            "low_risk_retail": {
                "name": "Low-Risk Retail Customer",
                "jurisdiction_risk_multiplier": 0.8,
                "occupation_risk_weight": 0.5,
                "network_risk_weight": 0.5,
                "aml_risk_bias": -0.2,  # Decrease risk
                "description": "Standard retail customer from low-risk jurisdiction"
            },
            "high_risk_jurisdiction": {
                "name": "High-Risk Jurisdiction",
                "jurisdiction_risk_multiplier": 2.0,  # Double risk
                "occupation_risk_weight": 1.2,
                "network_risk_weight": 1.5,
                "aml_risk_bias": 0.3,
                "description": "Customer from high-risk jurisdiction with sanctions exposure"
            },
            "pep_profile": {
                "name": "Politically Exposed Profile",
                "jurisdiction_risk_multiplier": 1.5,
                "occupation_risk_weight": 2.0,  # Double weight
                "network_risk_weight": 1.8,
                "aml_risk_bias": 0.4,
                "description": "Politically Exposed Person requiring enhanced due diligence"
            },
            "networked_entity": {
                "name": "Networked Entity Exposure",
                "jurisdiction_risk_multiplier": 1.3,
                "occupation_risk_weight": 1.0,
                "network_risk_weight": 3.0,  # Triple weight
                "aml_risk_bias": 0.35,
                "description": "Entity with complex relationship network and high-risk links"
            }
        }
        return scenarios.get(scenario_name, scenarios["low_risk_retail"])
    
    @staticmethod
    def get_market_signal_scenario(scenario_name: str) -> Dict[str, Any]:
        """Get market signal scenario parameters"""
        scenarios = {
            "calm_market": {
                "name": "Calm Market",
                "volatility_bias": -0.2,
                "sentiment_bias": 0.1,
                "liquidity_bias": 0.1,
                "stress_threshold": 0.3,
                "description": "Stable market conditions with low volatility"
            },
            "news_uncertainty": {
                "name": "News-Driven Uncertainty",
                "volatility_bias": 0.3,
                "sentiment_bias": -0.4,
                "liquidity_bias": 0.0,
                "stress_threshold": 0.5,
                "description": "Market uncertainty driven by news events and sentiment shifts"
            },
            "liquidity_stress": {
                "name": "Liquidity Stress",
                "volatility_bias": 0.4,
                "sentiment_bias": -0.2,
                "liquidity_bias": -0.5,  # Decrease liquidity
                "stress_threshold": 0.7,
                "description": "Market experiencing liquidity constraints and stress"
            },
            "macro_shock": {
                "name": "Macro Shock Event",
                "volatility_bias": 0.6,
                "sentiment_bias": -0.6,
                "liquidity_bias": -0.4,
                "stress_threshold": 0.9,
                "description": "Major macroeconomic shock affecting market stability"
            }
        }
        return scenarios.get(scenario_name, scenarios["calm_market"])
    
    @staticmethod
    def get_regime_simulation_scenario(scenario_name: str) -> Dict[str, Any]:
        """Get regime simulation scenario parameters"""
        scenarios = {
            "volatility_expansion": {
                "name": "Volatility Expansion",
                "volatility_shock_level": 0.7,
                "correlation_breakdown_score": 0.4,
                "liquidity_crisis_level": 0.3,
                "regime_transition_probability": 0.6,
                "description": "Market experiencing expanding volatility regime"
            },
            "correlation_breakdown": {
                "name": "Correlation Breakdown",
                "volatility_shock_level": 0.5,
                "correlation_breakdown_score": 0.8,  # High breakdown
                "liquidity_crisis_level": 0.4,
                "regime_transition_probability": 0.7,
                "description": "Traditional asset correlations breaking down"
            },
            "liquidity_freeze": {
                "name": "Liquidity Freeze",
                "volatility_shock_level": 0.6,
                "correlation_breakdown_score": 0.5,
                "liquidity_crisis_level": 0.9,  # Very high
                "regime_transition_probability": 0.8,
                "description": "Severe liquidity crisis with market freeze conditions"
            }
        }
        return scenarios.get(scenario_name, scenarios["volatility_expansion"])

