"""
Market Intelligence Synthetic Data Generator
Preserves real-world distributions, correlations, regime switching, stress scenarios
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


class MarketIntelligenceDataGenerator:
    """
    Synthetic data generator for Market & Digital Asset Intelligence
    Produces statistically realistic data with controlled correlations
    """
    
    def __init__(self, seed: int = 42):
        """Initialize generator with seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
    
    # ==================== MODULE 1: COMMODITY TREND ====================
    
    def generate_commodity_market_data(
        self,
        asset_id: str,
        start_date: datetime,
        days: int = 365,
        regime: str = "normal"
    ) -> List[Dict[str, Any]]:
        """Generate synthetic commodity market data with regime characteristics"""
        data = []
        current_price = 100.0  # Base price
        
        # Regime parameters
        if regime == "normal":
            volatility_base = 0.02
            trend_base = 0.0001  # Slight upward drift
        elif regime == "volatile":
            volatility_base = 0.05
            trend_base = 0.0
        elif regime == "stress":
            volatility_base = 0.08
            trend_base = -0.0005  # Downward pressure
        else:
            volatility_base = 0.03
            trend_base = 0.0002
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            
            # Add autocorrelation
            if i == 0:
                volatility = volatility_base
            else:
                volatility = 0.8 * volatility + 0.2 * np.random.normal(volatility_base, 0.005)
                volatility = max(0.01, volatility)
            
            # Price movement with trend
            daily_return = np.random.normal(trend_base, volatility)
            current_price *= (1 + daily_return)
            
            # Generate OHLC
            high_factor = np.random.uniform(1.0, 1.02)
            low_factor = np.random.uniform(0.98, 1.0)
            open_price = current_price * np.random.uniform(0.99, 1.01)
            high_price = current_price * high_factor
            low_price = current_price * low_factor
            close_price = current_price
            
            # Volume (correlated with volatility)
            volume = np.random.lognormal(10, 0.5) * (1 + volatility * 10)
            
            # Macro proxies
            inflation_index = np.random.uniform(0.01, 0.05)
            dollar_index = np.random.uniform(0.95, 1.05)
            
            # Derived features
            momentum_score = float(np.clip(np.random.normal(0.5, 0.2), 0.0, 1.0))
            rolling_variance = float(volatility ** 2)
            
            data.append({
                "asset_id": asset_id,
                "date": date.isoformat(),
                "open_price": round(open_price, 2),
                "high_price": round(high_price, 2),
                "low_price": round(low_price, 2),
                "close_price": round(close_price, 2),
                "volume": round(volume, 2),
                "volatility_indicator": round(volatility, 4),
                "inflation_index": round(inflation_index, 4),
                "dollar_index": round(dollar_index, 4),
                "daily_return": round(daily_return, 6),
                "momentum_score": round(momentum_score, 3),
                "rolling_variance": round(rolling_variance, 6)
            })
        
        return data
    
    # ==================== MODULE 2: MARKET REGIME ====================
    
    def generate_market_regime_features(
        self,
        market_id: str,
        start_date: datetime,
        days: int = 365,
        regime: str = "calm"
    ) -> List[Dict[str, Any]]:
        """Generate market regime features"""
        data = []
        
        # Regime parameters
        if regime == "calm":
            vol_base = 0.15
            trend_base = 0.6
            drawdown_base = 0.05
            liq_base = 0.8
        elif regime == "volatile":
            vol_base = 0.4
            trend_base = 0.3
            drawdown_base = 0.2
            liq_base = 0.5
        elif regime == "stress":
            vol_base = 0.6
            trend_base = 0.2
            drawdown_base = 0.4
            liq_base = 0.3
        else:
            vol_base = 0.25
            trend_base = 0.5
            drawdown_base = 0.1
            liq_base = 0.7
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            
            # Add autocorrelation
            if i == 0:
                rolling_vol = vol_base
                trend_strength = trend_base
                drawdown_depth = drawdown_base
                liquidity_proxy = liq_base
            else:
                rolling_vol = 0.7 * rolling_vol + 0.3 * np.random.normal(vol_base, 0.05)
                trend_strength = 0.8 * trend_strength + 0.2 * np.random.normal(trend_base, 0.1)
                drawdown_depth = 0.8 * drawdown_depth + 0.2 * np.random.normal(drawdown_base, 0.05)
                liquidity_proxy = 0.9 * liquidity_proxy + 0.1 * np.random.normal(liq_base, 0.1)
            
            rolling_vol = max(0.0, rolling_vol)
            trend_strength = float(np.clip(trend_strength, 0.0, 1.0))
            drawdown_depth = float(np.clip(drawdown_depth, 0.0, 1.0))
            liquidity_proxy = float(np.clip(liquidity_proxy, 0.0, 1.0))
            
            # Correlation shift (change in correlation)
            correlation_shift = float(np.random.normal(0.0, 0.1))
            
            data.append({
                "market_id": market_id,
                "date": date.isoformat(),
                "rolling_volatility": round(rolling_vol, 4),
                "trend_strength": round(trend_strength, 3),
                "drawdown_depth": round(drawdown_depth, 3),
                "correlation_shift": round(correlation_shift, 3),
                "liquidity_proxy": round(liquidity_proxy, 3)
            })
        
        return data
    
    # ==================== MODULE 3: DIGITAL ASSET ADOPTION ====================
    
    def generate_digital_asset_adoption_data(
        self,
        country_code: str,
        start_date: datetime,
        days: int = 365,
        adoption_phase: str = "growth"
    ) -> List[Dict[str, Any]]:
        """Generate digital asset adoption data"""
        data = []
        
        # Phase parameters
        if adoption_phase == "early":
            wallet_base = 0.2
            tx_base = 0.15
            exchange_base = 0.1
            growth_rate = 0.02  # 2% daily growth
        elif adoption_phase == "growth":
            wallet_base = 0.5
            tx_base = 0.4
            exchange_base = 0.3
            growth_rate = 0.01  # 1% daily growth
        elif adoption_phase == "maturation":
            wallet_base = 0.7
            tx_base = 0.6
            exchange_base = 0.5
            growth_rate = 0.002  # 0.2% daily growth
        else:  # saturation
            wallet_base = 0.85
            tx_base = 0.75
            exchange_base = 0.65
            growth_rate = 0.0  # No growth
        
        wallet_activity = wallet_base
        tx_volume = tx_base
        exchange_activity = exchange_base
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            
            # Growth with noise
            wallet_activity = wallet_activity * (1 + growth_rate) + np.random.normal(0, 0.01)
            tx_volume = tx_volume * (1 + growth_rate) + np.random.normal(0, 0.01)
            exchange_activity = exchange_activity * (1 + growth_rate) + np.random.normal(0, 0.01)
            
            wallet_activity = float(np.clip(wallet_activity, 0.0, 1.0))
            tx_volume = float(np.clip(tx_volume, 0.0, 1.0))
            exchange_activity = float(np.clip(exchange_activity, 0.0, 1.0))
            
            # Regulatory signal (can change over time)
            regulatory_signal = float(np.random.normal(0.0, 0.3))
            regulatory_signal = np.clip(regulatory_signal, -1.0, 1.0)
            
            # Network health metrics
            network_health = {
                "node_count": int(np.random.normal(1000, 100)),
                "transaction_success_rate": float(np.clip(np.random.normal(0.95, 0.05), 0.0, 1.0)),
                "average_confirmation_time": float(np.random.normal(10, 2))
            }
            
            data.append({
                "country_code": country_code,
                "date": date.isoformat(),
                "wallet_activity_index": round(wallet_activity, 3),
                "transaction_volume_index": round(tx_volume, 3),
                "exchange_activity_index": round(exchange_activity, 3),
                "regulatory_signal_score": round(regulatory_signal, 3),
                "network_health_metrics": network_health
            })
        
        return data
    
    # ==================== MODULE 4: EXCHANGE RISK ====================
    
    def generate_exchange_profile(self, exchange_id: str, is_high_risk: bool = False) -> Dict[str, Any]:
        """Generate exchange profile"""
        if is_high_risk:
            asset_coverage = np.random.randint(50, 200)
            volume_concentration = float(np.clip(np.random.normal(0.7, 0.1), 0.0, 1.0))
            liquidity_depth = float(np.clip(np.random.normal(0.4, 0.1), 0.0, 1.0))
            dependency_ratios = {
                "top_asset_dependency": float(np.clip(np.random.normal(0.6, 0.1), 0.0, 1.0)),
                "cross_exchange_dependency": float(np.clip(np.random.normal(0.5, 0.1), 0.0, 1.0))
            }
            stress_markers = ["liquidity_crisis_2020", "volatility_spike_2021"]
        else:
            asset_coverage = np.random.randint(200, 500)
            volume_concentration = float(np.clip(np.random.normal(0.3, 0.1), 0.0, 1.0))
            liquidity_depth = float(np.clip(np.random.normal(0.8, 0.1), 0.0, 1.0))
            dependency_ratios = {
                "top_asset_dependency": float(np.clip(np.random.normal(0.2, 0.1), 0.0, 1.0)),
                "cross_exchange_dependency": float(np.clip(np.random.normal(0.2, 0.1), 0.0, 1.0))
            }
            stress_markers = []
        
        return {
            "exchange_id": exchange_id,
            "exchange_name": f"Exchange {exchange_id}",
            "asset_coverage": int(asset_coverage),
            "volume_concentration": round(volume_concentration, 3),
            "liquidity_depth_proxy": round(liquidity_depth, 3),
            "dependency_ratios": dependency_ratios,
            "historical_stress_markers": stress_markers
        }

