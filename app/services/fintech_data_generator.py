"""
Fintech Synthetic Data Generator
Statistically realistic synthetic data for training
Preserves correlations, rarity, nonlinear risk spikes, regime shifts
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


class FintechDataGenerator:
    """
    Synthetic data generator for Fintech modules
    Produces statistically realistic data with controlled correlations
    """
    
    def __init__(self, seed: int = 42):
        """Initialize generator with seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
    
    # ==================== MODULE 1: CREDIT RISK ====================
    
    def generate_borrower_profile(self, borrower_id: str, region_id: str = "US") -> Dict[str, Any]:
        """Generate synthetic borrower profile with realistic correlations"""
        age = np.random.normal(42, 12)
        age = max(18, min(80, int(age)))
        
        # Employment type correlated with age and income
        employment_weights = {
            "full_time": 0.6,
            "part_time": 0.15,
            "self_employed": 0.2,
            "unemployed": 0.05
        }
        employment_type = np.random.choice(
            list(employment_weights.keys()),
            p=list(employment_weights.values())
        )
        
        # Income correlated with employment and age
        if employment_type == "full_time":
            base_income = np.random.lognormal(10.5, 0.5)  # ~$36k base
            age_factor = (age - 25) / 40  # Peak around 45
        elif employment_type == "self_employed":
            base_income = np.random.lognormal(10.8, 0.8)  # Higher variance
            age_factor = (age - 30) / 30
        elif employment_type == "part_time":
            base_income = np.random.lognormal(9.8, 0.4)
            age_factor = 0.5
        else:  # unemployed
            base_income = np.random.lognormal(9.0, 0.3)
            age_factor = 0.2
        
        annual_income = max(10000, base_income * (1 + age_factor * 0.5))
        
        # Employment stability correlated with employment type and income
        if employment_type == "full_time":
            stability_base = 0.7
        elif employment_type == "self_employed":
            stability_base = 0.5
        else:
            stability_base = 0.3
        
        # Ensure beta parameters are valid (> 0)
        alpha = max(0.1, stability_base * 10)
        beta = max(0.1, (1 - stability_base) * 10)
        employment_stability_score = np.clip(
            np.random.beta(alpha, beta),
            0.0, 1.0
        )
        
        # Income volatility inversely correlated with stability
        income_volatility_index = np.clip(1.0 - employment_stability_score + np.random.normal(0, 0.1), 0.0, 1.0)
        
        # Residence stability correlated with age and income
        # Ensure beta parameters are valid (> 0)
        age_factor = max(0.1, (age / 10) * 2)
        age_inverse = max(0.1, (1 - age / 80) * 2)
        residence_stability_score = np.clip(
            np.random.beta(age_factor, age_inverse),
            0.0, 1.0
        )
        
        return {
            "borrower_id": borrower_id,
            "age": age,
            "employment_type": employment_type,
            "employment_stability_score": round(employment_stability_score, 3),
            "annual_income": round(annual_income, 2),
            "income_volatility_index": round(income_volatility_index, 3),
            "residence_stability_score": round(residence_stability_score, 3),
            "region_id": region_id
        }
    
    def generate_credit_history(self, borrower_id: str, borrower_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate credit history correlated with borrower profile"""
        age = borrower_profile["age"]
        income = borrower_profile["annual_income"]
        employment_stability = borrower_profile["employment_stability_score"]
        
        # Credit score correlated with income and stability
        income_factor = min(income / 100000, 1.0)  # Normalize to 0-1
        stability_factor = employment_stability
        
        # Base credit score (300-850 scale)
        base_score = 300 + (income_factor * 0.4 + stability_factor * 0.3) * 550
        credit_score = np.clip(np.random.normal(base_score, 50), 300, 850)
        
        if credit_score >= 750:
            credit_score_band = "excellent"
        elif credit_score >= 700:
            credit_score_band = "good"
        elif credit_score >= 650:
            credit_score_band = "fair"
        else:
            credit_score_band = "poor"
        
        # Active loans correlated with income
        total_active_loans = max(0, int(np.random.poisson(income / 50000)))
        
        # Delinquency inversely correlated with credit score
        delinquency_prob = max(0, (850 - credit_score) / 550)
        delinquency_count = int(np.random.binomial(12, delinquency_prob * 0.1))
        
        # Historical default inversely correlated with credit score
        default_prob = max(0, (850 - credit_score) / 550 * 0.05)
        historical_default_flag = bool(np.random.random() < default_prob)
        
        # Repayment consistency correlated with credit score
        repayment_consistency_score = float(np.clip(credit_score / 850, 0.0, 1.0))
        repayment_consistency_score += float(np.random.normal(0, 0.1))
        repayment_consistency_score = float(np.clip(repayment_consistency_score, 0.0, 1.0))
        
        return {
            "borrower_id": borrower_id,
            "credit_score_band": credit_score_band,
            "total_active_loans": int(total_active_loans),
            "delinquency_count": int(delinquency_count),
            "historical_default_flag": bool(historical_default_flag),
            "repayment_consistency_score": round(repayment_consistency_score, 3)
        }
    
    def generate_financial_behavior(self, borrower_id: str, borrower_profile: Dict[str, Any], 
                                   credit_history: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial behavior correlated with profile and history"""
        income = borrower_profile["annual_income"]
        credit_score_band = credit_history["credit_score_band"]
        
        # Average monthly obligation (rent, utilities, etc.)
        avg_monthly_obligation = income / 12 * np.random.uniform(0.2, 0.5)
        
        # Debt-to-income ratio
        if credit_score_band in ["excellent", "good"]:
            dti_base = 0.2
        elif credit_score_band == "fair":
            dti_base = 0.35
        else:
            dti_base = 0.5
        
        debt_to_income_ratio = np.clip(
            np.random.normal(dti_base, 0.1),
            0.0, 1.0
        )
        
        # Utilization ratio (credit card usage)
        if credit_score_band in ["excellent", "good"]:
            util_base = 0.2
        else:
            util_base = 0.6
        
        util_alpha = max(0.1, util_base * 10)
        util_beta = max(0.1, (1 - util_base) * 10)
        utilization_ratio = np.clip(
            np.random.beta(util_alpha, util_beta),
            0.0, 1.0
        )
        
        # Payment delay frequency inversely correlated with credit score
        if credit_score_band == "excellent":
            delay_base = 0.05
        elif credit_score_band == "good":
            delay_base = 0.1
        elif credit_score_band == "fair":
            delay_base = 0.25
        else:
            delay_base = 0.5
        
        delay_alpha = max(0.1, delay_base * 10)
        delay_beta = max(0.1, (1 - delay_base) * 10)
        payment_delay_frequency = np.clip(
            np.random.beta(delay_alpha, delay_beta),
            0.0, 1.0
        )
        
        return {
            "borrower_id": borrower_id,
            "avg_monthly_obligation": round(avg_monthly_obligation, 2),
            "debt_to_income_ratio": round(debt_to_income_ratio, 3),
            "utilization_ratio": round(utilization_ratio, 3),
            "payment_delay_frequency": round(payment_delay_frequency, 3)
        }
    
    def generate_credit_outcome(self, borrower_id: str, borrower_profile: Dict[str, Any],
                               credit_history: Dict[str, Any], financial_behavior: Dict[str, Any],
                               macro_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate credit outcome for training (with controlled rarity)"""
        # Default probability based on multiple factors
        credit_score_band = credit_history["credit_score_band"]
        dti = financial_behavior["debt_to_income_ratio"]
        utilization = financial_behavior["utilization_ratio"]
        delay_freq = financial_behavior["payment_delay_frequency"]
        economic_stress = macro_context.get("economic_stress_level", 0.2)
        
        # Base default probability (rare event)
        if credit_score_band == "excellent":
            base_prob = 0.01
        elif credit_score_band == "good":
            base_prob = 0.03
        elif credit_score_band == "fair":
            base_prob = 0.08
        else:
            base_prob = 0.15
        
        # Adjust for financial behavior
        behavior_multiplier = 1.0 + (dti - 0.3) * 2 + (utilization - 0.4) * 1.5 + delay_freq * 1.5
        behavior_multiplier = max(0.5, min(3.0, behavior_multiplier))
        
        # Adjust for economic stress
        stress_multiplier = 1.0 + economic_stress * 2.0
        
        default_probability = min(0.5, base_prob * behavior_multiplier * stress_multiplier)
        default_within_12m = bool(np.random.random() < default_probability)
        
        # Loss given default
        if default_within_12m:
            if credit_score_band in ["excellent", "good"]:
                lgd_band = "low"
            elif credit_score_band == "fair":
                lgd_band = "medium"
            else:
                lgd_band = "high"
        else:
            lgd_band = None
        
        return {
            "borrower_id": borrower_id,
            "default_within_12m": default_within_12m,
            "loss_given_default_band": lgd_band,
            "outcome_date": (datetime.now() + timedelta(days=365)).isoformat()
        }
    
    # ==================== MODULE 2: FRAUD DETECTION ====================
    
    def generate_transaction_event(self, transaction_id: str, account_id: str, 
                                  is_fraud: bool = False) -> Dict[str, Any]:
        """Generate transaction event (fraud is rare)"""
        channels = ["online", "pos", "atm", "mobile"]
        merchant_categories = ["retail", "restaurant", "gas", "grocery", "travel", "entertainment"]
        geo_locations = ["US", "CA", "UK", "DE", "FR", "BR", "MX", "IN"]
        
        if is_fraud:
            # Fraud patterns: unusual amounts, locations, times
            amount = np.random.lognormal(7, 1.5)  # Higher variance
            channel_type = np.random.choice(channels, p=[0.4, 0.2, 0.1, 0.3])  # Favor online/mobile
            geo_location = np.random.choice(geo_locations)  # Can be unusual
            # Fraud often happens at unusual times
            hour = np.random.choice([0, 1, 2, 3, 4, 5, 22, 23])
        else:
            # Normal patterns
            amount = np.random.lognormal(4.5, 0.8)  # Lower, more consistent
            channel_type = np.random.choice(channels, p=[0.3, 0.4, 0.1, 0.2])
            geo_location = "US"  # Usually home country
            hour = np.random.choice(list(range(9, 21)))  # Business hours
        
        timestamp = datetime.now() - timedelta(
            hours=np.random.randint(0, 168)  # Last week
        )
        timestamp = timestamp.replace(hour=hour, minute=np.random.randint(0, 60))
        
        return {
            "transaction_id": transaction_id,
            "account_id": account_id,
            "amount": round(amount, 2),
            "timestamp": timestamp.isoformat(),
            "channel_type": channel_type,
            "merchant_category": np.random.choice(merchant_categories),
            "geo_location": geo_location
        }
    
    def generate_account_profile(self, account_id: str) -> Dict[str, Any]:
        """Generate account profile"""
        account_age_days = np.random.randint(30, 3650)  # 1 month to 10 years
        avg_transaction_amount = np.random.lognormal(4.0, 0.6)
        typical_geo_region = "US"
        typical_active_hours = list(range(9, 18))  # Business hours
        
        return {
            "account_id": account_id,
            "account_age_days": account_age_days,
            "avg_transaction_amount": round(avg_transaction_amount, 2),
            "typical_geo_region": typical_geo_region,
            "typical_active_hours": typical_active_hours
        }
    
    def generate_fraud_label(self, transaction_id: str, transaction: Dict[str, Any],
                            account_profile: Dict[str, Any], fraud_probability: float = 0.01) -> Dict[str, Any]:
        """Generate fraud label (fraud is rare - 1% base rate)"""
        is_fraud = np.random.random() < fraud_probability
        
        if is_fraud:
            fraud_types = ["card_testing", "account_takeover", "identity_theft", "synthetic_identity"]
            fraud_type = np.random.choice(fraud_types)
        else:
            fraud_type = None
        
        return {
            "transaction_id": transaction_id,
            "fraud_flag": bool(is_fraud),
            "fraud_type": fraud_type
        }
    
    # ==================== MODULE 3: KYC / AML ====================
    
    def generate_customer_identity(self, customer_id: str, is_high_risk: bool = False) -> Dict[str, Any]:
        """Generate customer identity"""
        low_risk_countries = ["US", "CA", "UK", "DE", "FR", "AU", "NZ"]
        high_risk_countries = ["XX", "YY", "ZZ"]  # Placeholder high-risk codes
        
        if is_high_risk:
            nationality = np.random.choice(high_risk_countries)
            residency_country = np.random.choice(high_risk_countries)
            occupation_risk_level = np.random.choice(["medium", "high"], p=[0.3, 0.7])
        else:
            nationality = np.random.choice(low_risk_countries)
            residency_country = np.random.choice(low_risk_countries)
            occupation_risk_level = np.random.choice(["low", "medium"], p=[0.8, 0.2])
        
        onboarding_channels = ["online", "branch", "mobile"]
        onboarding_channel = np.random.choice(onboarding_channels)
        
        return {
            "customer_id": customer_id,
            "nationality": nationality,
            "residency_country": residency_country,
            "occupation_risk_level": occupation_risk_level,
            "onboarding_channel": onboarding_channel,
            "country_code": residency_country
        }
    
    def generate_identity_verification(self, customer_id: str, is_high_risk: bool = False) -> Dict[str, Any]:
        """Generate identity verification signals"""
        if is_high_risk:
            # Lower match scores for high-risk
            document_match_score = float(np.clip(np.random.normal(0.7, 0.15), 0.0, 1.0))
            biometric_match_score = float(np.clip(np.random.normal(0.75, 0.12), 0.0, 1.0))
            name_similarity_score = float(np.clip(np.random.normal(0.65, 0.2), 0.0, 1.0))
        else:
            # Higher match scores for low-risk
            document_match_score = float(np.clip(np.random.normal(0.95, 0.05), 0.0, 1.0))
            biometric_match_score = float(np.clip(np.random.normal(0.97, 0.03), 0.0, 1.0))
            name_similarity_score = float(np.clip(np.random.normal(0.92, 0.08), 0.0, 1.0))
        
        return {
            "customer_id": customer_id,
            "document_match_score": round(document_match_score, 3),
            "biometric_match_score": round(biometric_match_score, 3),
            "name_similarity_score": round(name_similarity_score, 3)
        }
    
    def generate_relationship_network(self, customer_id: str, is_high_risk: bool = False) -> Dict[str, Any]:
        """Generate relationship network"""
        if is_high_risk:
            linked_entities_count = int(np.random.poisson(15))  # More links
            high_risk_link_flag = bool(np.random.random() < 0.6)  # 60% chance
            network_complexity_score = float(np.clip(np.random.normal(0.7, 0.15), 0.0, 1.0))
        else:
            linked_entities_count = int(np.random.poisson(3))  # Fewer links
            high_risk_link_flag = bool(np.random.random() < 0.05)  # 5% chance
            network_complexity_score = float(np.clip(np.random.normal(0.3, 0.1), 0.0, 1.0))
        
        return {
            "customer_id": customer_id,
            "linked_entities_count": linked_entities_count,
            "high_risk_link_flag": high_risk_link_flag,
            "network_complexity_score": round(network_complexity_score, 3)
        }
    
    def generate_compliance_outcome(self, customer_id: str, customer_identity: Dict[str, Any],
                                   relationship_network: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compliance outcome for training"""
        # AML risk based on multiple factors
        country_risk = 0.3 if customer_identity["country_code"] in ["US", "CA", "UK"] else 0.7
        occupation_risk = {"low": 0.2, "medium": 0.5, "high": 0.8}[customer_identity["occupation_risk_level"]]
        network_risk = 0.3 if relationship_network["high_risk_link_flag"] else 0.1
        network_risk += relationship_network["network_complexity_score"] * 0.3
        
        aml_risk_score = (country_risk * 0.4 + occupation_risk * 0.3 + network_risk * 0.3)
        
        if aml_risk_score < 0.3:
            aml_risk_level = "low"
            escalation_required = False
        elif aml_risk_score < 0.5:
            aml_risk_level = "medium"
            escalation_required = bool(np.random.random() < 0.3)
        elif aml_risk_score < 0.7:
            aml_risk_level = "high"
            escalation_required = True
        else:
            aml_risk_level = "very_high"
            escalation_required = True
        
        return {
            "customer_id": customer_id,
            "escalation_required": bool(escalation_required),
            "aml_risk_level": str(aml_risk_level),
            "outcome_date": datetime.now().isoformat()
        }
    
    # ==================== MODULE 4 & 5: MARKET DATA ====================
    
    def generate_market_time_series(self, market_id: str, days: int = 365, 
                                    regime: str = "calm") -> List[Dict[str, Any]]:
        """Generate market time series with regime characteristics"""
        series = []
        base_date = datetime.now() - timedelta(days=days)
        
        # Regime parameters
        if regime == "calm":
            volatility_base = 0.15
            drawdown_base = 0.05
            liquidity_base = 0.8
        elif regime == "volatile":
            volatility_base = 0.4
            drawdown_base = 0.2
            liquidity_base = 0.5
        elif regime == "stress":
            volatility_base = 0.6
            drawdown_base = 0.4
            liquidity_base = 0.3
        else:
            volatility_base = 0.25
            drawdown_base = 0.1
            liquidity_base = 0.7
        
        for i in range(days):
            timestamp = base_date + timedelta(days=i)
            
            # Add some autocorrelation
            if i == 0:
                return_volatility = volatility_base
                drawdown_level = drawdown_base
                liquidity_shift_index = liquidity_base
            else:
                return_volatility = 0.7 * return_volatility + 0.3 * np.random.normal(volatility_base, 0.1)
                drawdown_level = 0.8 * drawdown_level + 0.2 * np.random.normal(drawdown_base, 0.05)
                liquidity_shift_index = 0.9 * liquidity_shift_index + 0.1 * np.random.normal(liquidity_base, 0.1)
            
            return_volatility = max(0.0, return_volatility)
            drawdown_level = max(0.0, min(1.0, drawdown_level))
            liquidity_shift_index = max(0.0, min(1.0, liquidity_shift_index))
            
            series.append({
                "market_id": market_id,
                "timestamp": timestamp.isoformat(),
                "return_volatility": round(return_volatility, 4),
                "drawdown_level": round(drawdown_level, 4),
                "liquidity_shift_index": round(liquidity_shift_index, 4),
                "price_level": round(100 * (1 + np.random.normal(0, return_volatility)), 2),
                "volume": round(np.random.lognormal(10, 0.5), 2)
            })
        
        return series

