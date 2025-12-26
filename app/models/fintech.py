"""
Fintech Industry Models - Boardroom-Grade Data Schemas
Canonical, stable, versioned schemas for financial intelligence modules
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


# ==================== MODULE 1: CREDIT RISK INTELLIGENCE ====================

class BorrowerProfile(Base):
    """Borrower profile for credit risk assessment"""
    __tablename__ = "borrower_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    employment_type = Column(String(50), nullable=False)  # 'full_time', 'part_time', 'self_employed', 'unemployed'
    employment_stability_score = Column(Float, nullable=False)  # 0.0 to 1.0
    annual_income = Column(Float, nullable=False)
    income_volatility_index = Column(Float, nullable=False)  # 0.0 to 1.0
    residence_stability_score = Column(Float, nullable=False)  # 0.0 to 1.0
    region_id = Column(String(50), ForeignKey("macro_economic_contexts.region_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    credit_history = relationship("CreditHistorySummary", back_populates="borrower", uselist=False)
    financial_behavior = relationship("FinancialBehavior", back_populates="borrower", uselist=False)
    credit_outcomes = relationship("CreditOutcome", back_populates="borrower")


class CreditHistorySummary(Base):
    """Credit history summary for borrowers"""
    __tablename__ = "credit_history_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(String(100), ForeignKey("borrower_profiles.borrower_id"), unique=True, nullable=False, index=True)
    credit_score_band = Column(String(20), nullable=False)  # 'excellent', 'good', 'fair', 'poor'
    total_active_loans = Column(Integer, default=0)
    delinquency_count = Column(Integer, default=0)
    historical_default_flag = Column(Boolean, default=False)
    repayment_consistency_score = Column(Float, nullable=False)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    borrower = relationship("BorrowerProfile", back_populates="credit_history")


class FinancialBehavior(Base):
    """Financial behavior patterns"""
    __tablename__ = "financial_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(String(100), ForeignKey("borrower_profiles.borrower_id"), unique=True, nullable=False, index=True)
    avg_monthly_obligation = Column(Float, nullable=False)
    debt_to_income_ratio = Column(Float, nullable=False)  # 0.0 to 1.0+
    utilization_ratio = Column(Float, nullable=False)  # 0.0 to 1.0
    payment_delay_frequency = Column(Float, nullable=False)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    borrower = relationship("BorrowerProfile", back_populates="financial_behavior")


class MacroEconomicContext(Base):
    """Macro-economic context for regions"""
    __tablename__ = "macro_economic_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(String(50), unique=True, index=True, nullable=False)
    region_name = Column(String(100), nullable=False)
    interest_rate_level = Column(Float, nullable=False)  # Percentage
    inflation_index = Column(Float, nullable=False)  # 0.0 to 1.0
    unemployment_index = Column(Float, nullable=False)  # 0.0 to 1.0
    economic_stress_level = Column(Float, nullable=False)  # 0.0 to 1.0
    effective_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CreditOutcome(Base):
    """Credit outcomes for training (not used in production inference)"""
    __tablename__ = "credit_outcomes"
    
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(String(100), ForeignKey("borrower_profiles.borrower_id"), nullable=False, index=True)
    default_within_12m = Column(Boolean, nullable=False)
    loss_given_default_band = Column(String(20))  # 'low', 'medium', 'high'
    outcome_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    borrower = relationship("BorrowerProfile", back_populates="credit_outcomes")


# ==================== MODULE 2: FRAUD DETECTION CONTROL ROOM ====================

class TransactionEvent(Base):
    """Transaction events for fraud detection"""
    __tablename__ = "transaction_events"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    account_id = Column(String(100), ForeignKey("account_profiles.account_id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    channel_type = Column(String(50), nullable=False)  # 'online', 'pos', 'atm', 'mobile'
    merchant_category = Column(String(100))
    geo_location = Column(String(100))  # Country/region code
    device_id = Column(String(100), ForeignKey("device_contexts.device_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    account = relationship("AccountProfile", back_populates="transactions")
    device = relationship("DeviceContext", back_populates="transactions")
    fraud_label = relationship("FraudLabel", back_populates="transaction", uselist=False)
    
    __table_args__ = (
        Index('idx_account_timestamp', 'account_id', 'timestamp'),
    )


class AccountProfile(Base):
    """Account profiles for fraud detection"""
    __tablename__ = "account_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(100), unique=True, index=True, nullable=False)
    account_age_days = Column(Integer, nullable=False)
    avg_transaction_amount = Column(Float, nullable=False)
    typical_geo_region = Column(String(100), nullable=False)
    typical_active_hours = Column(JSON)  # Array of typical hours [9, 10, 11, ...]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transactions = relationship("TransactionEvent", back_populates="account")
    behavioral_pattern = relationship("BehavioralPattern", back_populates="account", uselist=False)
    devices = relationship("DeviceContext", back_populates="account")


class DeviceContext(Base):
    """Device context for transactions"""
    __tablename__ = "device_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, index=True, nullable=False)
    account_id = Column(String(100), ForeignKey("account_profiles.account_id"), nullable=False, index=True)
    device_trust_score = Column(Float, nullable=False)  # 0.0 to 1.0
    device_change_frequency = Column(Float, nullable=False)  # 0.0 to 1.0
    device_type = Column(String(50))  # 'mobile', 'desktop', 'tablet'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    account = relationship("AccountProfile", back_populates="devices")
    transactions = relationship("TransactionEvent", back_populates="device")


class BehavioralPattern(Base):
    """Behavioral patterns for accounts"""
    __tablename__ = "behavioral_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(100), ForeignKey("account_profiles.account_id"), unique=True, nullable=False, index=True)
    transaction_velocity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    geo_deviation_score = Column(Float, nullable=False)  # 0.0 to 1.0
    behavioral_consistency_score = Column(Float, nullable=False)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    account = relationship("AccountProfile", back_populates="behavioral_pattern")


class FraudLabel(Base):
    """Fraud labels for training (not used in production inference)"""
    __tablename__ = "fraud_labels"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), ForeignKey("transaction_events.transaction_id"), unique=True, nullable=False, index=True)
    fraud_flag = Column(Boolean, nullable=False)
    fraud_type = Column(String(50))  # 'card_testing', 'account_takeover', 'identity_theft', etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    transaction = relationship("TransactionEvent", back_populates="fraud_label")


# ==================== MODULE 3: KYC / AML RISK ENGINE ====================

class CustomerIdentity(Base):
    """Customer identity for KYC/AML"""
    __tablename__ = "customer_identities"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(100), unique=True, index=True, nullable=False)
    nationality = Column(String(50), nullable=False)
    residency_country = Column(String(50), nullable=False)
    occupation_risk_level = Column(String(20), nullable=False)  # 'low', 'medium', 'high'
    onboarding_channel = Column(String(50), nullable=False)  # 'online', 'branch', 'mobile'
    country_code = Column(String(10), ForeignKey("jurisdiction_risks.country_code"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    identity_verification = relationship("IdentityVerificationSignals", back_populates="customer", uselist=False)
    relationship_network = relationship("RelationshipNetwork", back_populates="customer", uselist=False)
    compliance_outcome = relationship("ComplianceOutcome", back_populates="customer", uselist=False)


class IdentityVerificationSignals(Base):
    """Identity verification signals"""
    __tablename__ = "identity_verification_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(100), ForeignKey("customer_identities.customer_id"), unique=True, nullable=False, index=True)
    document_match_score = Column(Float, nullable=False)  # 0.0 to 1.0
    biometric_match_score = Column(Float, nullable=False)  # 0.0 to 1.0
    name_similarity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("CustomerIdentity", back_populates="identity_verification")


class JurisdictionRisk(Base):
    """Jurisdiction risk ratings"""
    __tablename__ = "jurisdiction_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(10), unique=True, index=True, nullable=False)
    country_name = Column(String(100), nullable=False)
    aml_risk_rating = Column(String(20), nullable=False)  # 'low', 'medium', 'high', 'very_high'
    sanctions_exposure_level = Column(Float, nullable=False)  # 0.0 to 1.0
    effective_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RelationshipNetwork(Base):
    """Relationship networks for AML"""
    __tablename__ = "relationship_networks"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(100), ForeignKey("customer_identities.customer_id"), nullable=False, index=True)
    linked_entities_count = Column(Integer, default=0)
    high_risk_link_flag = Column(Boolean, default=False)
    network_complexity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("CustomerIdentity", back_populates="relationship_network")


class ComplianceOutcome(Base):
    """Compliance outcomes for training (not used in production inference)"""
    __tablename__ = "compliance_outcomes"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(100), ForeignKey("customer_identities.customer_id"), unique=True, nullable=False, index=True)
    escalation_required = Column(Boolean, nullable=False)
    aml_risk_level = Column(String(20), nullable=False)  # 'low', 'medium', 'high', 'very_high'
    outcome_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    customer = relationship("CustomerIdentity", back_populates="compliance_outcome")


# ==================== MODULE 4: MARKET SIGNAL INTELLIGENCE ====================

class MarketEnvironment(Base):
    """Market environment context"""
    __tablename__ = "market_environments"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), unique=True, index=True, nullable=False)
    market_name = Column(String(100), nullable=False)
    volatility_index = Column(Float, nullable=False)  # 0.0 to 1.0+
    liquidity_index = Column(Float, nullable=False)  # 0.0 to 1.0
    macro_uncertainty_score = Column(Float, nullable=False)  # 0.0 to 1.0
    effective_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    news_signals = relationship("NewsSignal", back_populates="market")
    sentiment_aggregate = relationship("SentimentAggregate", back_populates="market", uselist=False)
    market_context_label = relationship("MarketContextLabel", back_populates="market", uselist=False)


class NewsSignal(Base):
    """News signals for market intelligence"""
    __tablename__ = "news_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(String(100), unique=True, index=True, nullable=False)
    market_id = Column(String(50), ForeignKey("market_environments.market_id"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    sentiment_score = Column(Float, nullable=False)  # -1.0 to 1.0
    topic_cluster = Column(String(100), nullable=False)  # 'economic_policy', 'corporate_earnings', etc.
    relevance_weight = Column(Float, nullable=False)  # 0.0 to 1.0
    source = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    market = relationship("MarketEnvironment", back_populates="news_signals")
    
    __table_args__ = (
        Index('idx_market_timestamp', 'market_id', 'timestamp'),
    )


class SentimentAggregate(Base):
    """Aggregated sentiment for markets"""
    __tablename__ = "sentiment_aggregates"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), ForeignKey("market_environments.market_id"), unique=True, nullable=False, index=True)
    rolling_sentiment_index = Column(Float, nullable=False)  # -1.0 to 1.0
    sentiment_divergence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    aggregation_window_days = Column(Integer, default=30)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    market = relationship("MarketEnvironment", back_populates="sentiment_aggregate")


class MarketContextLabel(Base):
    """Market context labels for training (not used in production inference)"""
    __tablename__ = "market_context_labels"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), ForeignKey("market_environments.market_id"), unique=True, nullable=False, index=True)
    stress_state = Column(String(20), nullable=False)  # 'calm', 'stressed', 'volatile'
    label_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    market = relationship("MarketEnvironment", back_populates="market_context_label")


# ==================== MODULE 5: MARKET REGIME SIMULATION ENGINE ====================

class MarketTimeSeries(Base):
    """Market time series data"""
    __tablename__ = "market_time_series"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    return_volatility = Column(Float, nullable=False)  # 0.0 to 1.0+
    drawdown_level = Column(Float, nullable=False)  # 0.0 to 1.0
    liquidity_shift_index = Column(Float, nullable=False)  # 0.0 to 1.0
    price_level = Column(Float)
    volume = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # Note: Relationship to RegimeState would require composite foreign key on (market_id, timestamp)
    # For now, removed to avoid SQLAlchemy join condition errors
    # Use explicit queries with market_id and timestamp if relationship is needed
    
    __table_args__ = (
        Index('idx_market_timestamp_ts', 'market_id', 'timestamp'),
    )


class RegimeState(Base):
    """Market regime states"""
    __tablename__ = "regime_states"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    regime_label = Column(String(50), nullable=False)  # 'bull', 'bear', 'volatile', 'calm', 'stress'
    regime_confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    transition_probability = Column(Float)  # Probability of regime change
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # Note: Relationship to MarketTimeSeries would require composite foreign key on (market_id, timestamp)
    # For now, removed to avoid SQLAlchemy join condition errors
    # Use explicit queries with market_id and timestamp if relationship is needed
    
    __table_args__ = (
        Index('idx_market_timestamp_regime', 'market_id', 'timestamp'),
    )


class StressScenarioProfile(Base):
    """Stress scenario profiles"""
    __tablename__ = "stress_scenario_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(100), unique=True, index=True, nullable=False)
    scenario_name = Column(String(200), nullable=False)
    volatility_shock_level = Column(Float, nullable=False)  # 0.0 to 1.0+
    correlation_breakdown_score = Column(Float, nullable=False)  # 0.0 to 1.0
    liquidity_crisis_level = Column(Float, nullable=False)  # 0.0 to 1.0
    scenario_description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ==================== MARKET & DIGITAL ASSET INTELLIGENCE (FINTECH) ====================

# Module 1: Commodity Trend Intelligence
class CommodityMarketData(Base):
    """Commodity market price and volume data"""
    __tablename__ = "commodity_market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String(50), nullable=False, index=True)  # 'gold', 'silver', 'oil', etc.
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    volatility_indicator = Column(Float)  # Rolling volatility
    inflation_index = Column(Float)  # Optional macro proxy
    dollar_index = Column(Float)  # Optional macro proxy
    # Derived features
    daily_return = Column(Float)  # Calculated from close prices
    momentum_score = Column(Float)  # Rolling momentum
    rolling_variance = Column(Float)  # Rolling variance
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_commodity_asset_date', 'asset_id', 'date'),
    )


class CommodityTrendSignal(Base):
    """Commodity trend intelligence signals"""
    __tablename__ = "commodity_trend_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String(50), nullable=False, index=True)
    signal_date = Column(DateTime(timezone=True), nullable=False, index=True)
    directional_bias = Column(String(20), nullable=False)  # 'up', 'down', 'sideways'
    confidence_band_lower = Column(Float, nullable=False)  # 0.0 to 1.0
    confidence_band_upper = Column(Float, nullable=False)  # 0.0 to 1.0
    trend_strength = Column(Float, nullable=False)  # 0.0 to 1.0
    volatility_estimate = Column(Float, nullable=False)
    similar_periods = Column(JSON)  # Top 3 historical analogs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_commodity_asset_signal_date', 'asset_id', 'signal_date'),
    )


# Module 2: Market Regime Signals (additional to existing MarketRegimeState)
class MarketRegimeFeature(Base):
    """Derived market regime features"""
    __tablename__ = "market_regime_features"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    rolling_volatility = Column(Float, nullable=False)
    trend_strength = Column(Float, nullable=False)  # 0.0 to 1.0
    drawdown_depth = Column(Float, nullable=False)  # 0.0 to 1.0
    correlation_shift = Column(Float)  # Change in correlation
    liquidity_proxy = Column(Float, nullable=False)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_regime_market_date', 'market_id', 'date'),
    )


# Module 3: Digital Asset Adoption Intelligence
class DigitalAssetAdoptionData(Base):
    """Digital asset adoption metrics by country"""
    __tablename__ = "digital_asset_adoption_data"
    
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(10), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    wallet_activity_index = Column(Float, nullable=False)  # 0.0 to 1.0
    transaction_volume_index = Column(Float, nullable=False)  # 0.0 to 1.0
    exchange_activity_index = Column(Float, nullable=False)  # 0.0 to 1.0
    regulatory_signal_score = Column(Float)  # -1.0 to 1.0 (negative = restrictive)
    network_health_metrics = Column(JSON)  # Additional network metrics
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_adoption_country_date', 'country_code', 'date'),
    )


class DigitalAssetAdoptionSignal(Base):
    """Digital asset adoption intelligence signals"""
    __tablename__ = "digital_asset_adoption_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(10), nullable=False, index=True)
    signal_date = Column(DateTime(timezone=True), nullable=False, index=True)
    adoption_phase = Column(String(50), nullable=False)  # 'early', 'growth', 'maturation', 'saturation'
    momentum_score = Column(Float, nullable=False)  # -1.0 to 1.0
    growth_rate = Column(Float)  # Percentage change
    acceleration_indicator = Column(Float)  # -1.0 to 1.0 (negative = deceleration)
    regional_rank = Column(Integer)  # Rank among regions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_adoption_country_signal_date', 'country_code', 'signal_date'),
    )


# Module 4: Exchange & Market Risk Mapping
class ExchangeProfile(Base):
    """Exchange profiles and characteristics"""
    __tablename__ = "exchange_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(String(100), unique=True, index=True, nullable=False)
    exchange_name = Column(String(200), nullable=False)
    asset_coverage = Column(Integer)  # Number of assets traded
    volume_concentration = Column(Float, nullable=False)  # 0.0 to 1.0
    liquidity_depth_proxy = Column(Float, nullable=False)  # 0.0 to 1.0
    dependency_ratios = Column(JSON)  # Dependencies on other exchanges/assets
    historical_stress_markers = Column(JSON)  # Past stress events
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExchangeRiskSignal(Base):
    """Exchange and market risk mapping signals"""
    __tablename__ = "exchange_risk_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(String(100), ForeignKey("exchange_profiles.exchange_id"), nullable=False, index=True)
    signal_date = Column(DateTime(timezone=True), nullable=False, index=True)
    risk_concentration_score = Column(Float, nullable=False)  # 0.0 to 1.0
    dependency_hotspots = Column(JSON)  # List of high-dependency relationships
    systemic_exposure_indicator = Column(Float, nullable=False)  # 0.0 to 1.0
    stress_propagation_risk = Column(Float)  # Risk of cascading failures
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    exchange = relationship("ExchangeProfile", backref="risk_signals")
    
    __table_args__ = (
        Index('idx_exchange_risk_signal_date', 'exchange_id', 'signal_date'),
    )

