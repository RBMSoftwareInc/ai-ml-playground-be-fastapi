"""
Database Models - Comprehensive Schema
Covers: Industries, Use Cases, Products, Orders, Customers, Analytics,
Training Data, Models, DevLab, Discovery Tools
"""
from app.models.user import User
from app.models.industry import Industry
from app.models.use_case import UseCase, UseCaseExecution, UseCaseCategory
from app.models.product import Product, ProductCategory, ProductVariant
from app.models.order import Order, OrderItem
from app.models.transaction import Transaction
from app.models.customer import Customer, CustomerSegment
from app.models.inventory import Inventory, InventoryMovement
from app.models.analytics import AnalyticsEvent, ABTest, ABTestResult
from app.models.training import (
    ContentChunk, TrainingDataset, ConversationExample, 
    SimulationExample, CodeExample
)
from app.models.ai_models import (
    ModelVersion, ModelMetric, ModelDeployment
)
from app.models.devlab import (
    DevLabProject, DevLabFile, DevLabExecution, DevLabAnalysis,
    DevLabTest, DevLabVulnerability, DevLabInsight
)
from app.models.discovery import DiscoveryTool, DiscoveryToolExecution
from app.models.content import ContentVersion, ContentSync
from app.models.admin import (
    ContentAsset, Theme, ContentBlock, ActionDefinition,
    OutputTheme, AIModelConfiguration, ContentAuditLog
)
from app.models.auth import (
    Role, Permission, UserRole, RolePermission, RefreshToken, LoginAttempt
)
from app.models.cms_workflow import (
    WorkflowContentVersion, ContentApproval, WorkflowDefinition,
    ContentSchedule, CMSSettings, ContentStatus, ContentProject
)
from app.models.intelligence import (
    IntelligenceContent, IntelligenceConversation, WorkflowComparison, ModelHonestyMetadata,
    ContentCategory, ConfidenceLevel
)
from app.models.fintech import (
    # Credit Risk
    BorrowerProfile, CreditHistorySummary, FinancialBehavior,
    MacroEconomicContext, CreditOutcome,
    # Fraud Detection
    TransactionEvent, AccountProfile, DeviceContext,
    BehavioralPattern, FraudLabel,
    # KYC/AML
    CustomerIdentity, IdentityVerificationSignals, JurisdictionRisk,
    RelationshipNetwork, ComplianceOutcome,
    # Market Signal
    MarketEnvironment, NewsSignal, SentimentAggregate, MarketContextLabel,
    # Regime Simulation
    MarketTimeSeries, RegimeState, StressScenarioProfile,
    # Market & Digital Asset Intelligence
    CommodityMarketData, CommodityTrendSignal, MarketRegimeFeature,
    DigitalAssetAdoptionData, DigitalAssetAdoptionSignal,
    ExchangeProfile, ExchangeRiskSignal
)
from app.models.travel import (
    # Pricing & Revenue Intelligence
    PricingEvent, PricingRecommendation,
    BookingHistory, DemandForecast,
    # Personalized Travel Intelligence
    TravelerProfile, TravelerIntent, RecommendationResult,
    ConversationContext,
    # Operational Intelligence
    RouteSegment, RouteOptimization,
    HotelProfile, HotelMatch
)

__all__ = [
    # Core
    "User",
    "Industry",
    "UseCase",
    "UseCaseExecution",
    "UseCaseCategory",
    # Products & Commerce
    "Product",
    "ProductCategory",
    "ProductVariant",
    "Order",
    "OrderItem",
    "Transaction",
    "Customer",
    "CustomerSegment",
    "Inventory",
    "InventoryMovement",
    # Analytics
    "AnalyticsEvent",
    "ABTest",
    "ABTestResult",
    # Training & AI Models
    "ContentChunk",
    "TrainingDataset",
    "ConversationExample",
    "SimulationExample",
    "CodeExample",
    "ModelVersion",
    "ModelMetric",
    "ModelDeployment",
    # DevLab
    "DevLabProject",
    "DevLabFile",
    "DevLabExecution",
    "DevLabAnalysis",
    "DevLabTest",
    "DevLabVulnerability",
    "DevLabInsight",
    # Discovery
    "DiscoveryTool",
    "DiscoveryToolExecution",
    # Content Management
    "ContentVersion",
    "ContentSync",
    # Admin & CMS
    "ContentAsset",
    "Theme",
    "ContentBlock",
    "ActionDefinition",
    "OutputTheme",
    "AIModelConfiguration",
    "ContentAuditLog",
    # Auth & RBAC
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "RefreshToken",
    "LoginAttempt",
    # CMS Workflow
    "WorkflowContentVersion",
    "ContentApproval",
    "WorkflowDefinition",
    "ContentSchedule",
    "CMSSettings",
    "ContentStatus",
    # Intelligence Content Store
    "IntelligenceContent",
    "IntelligenceConversation",
    "WorkflowComparison",
    "ModelHonestyMetadata",
    "ContentCategory",
    "ConfidenceLevel",
    # Fintech - Credit Risk
    "BorrowerProfile",
    "CreditHistorySummary",
    "FinancialBehavior",
    "MacroEconomicContext",
    "CreditOutcome",
    # Fintech - Fraud Detection
    "TransactionEvent",
    "AccountProfile",
    "DeviceContext",
    "BehavioralPattern",
    "FraudLabel",
    # Fintech - KYC/AML
    "CustomerIdentity",
    "IdentityVerificationSignals",
    "JurisdictionRisk",
    "RelationshipNetwork",
    "ComplianceOutcome",
    # Fintech - Market Signal
    "MarketEnvironment",
    "NewsSignal",
    "SentimentAggregate",
    "MarketContextLabel",
    # Fintech - Regime Simulation
    "MarketTimeSeries",
    "RegimeState",
    "StressScenarioProfile",
    # Fintech - Market & Digital Asset Intelligence
    "CommodityMarketData",
    "CommodityTrendSignal",
    "MarketRegimeFeature",
    "DigitalAssetAdoptionData",
    "DigitalAssetAdoptionSignal",
    "ExchangeProfile",
    "ExchangeRiskSignal",
    # Travel - Pricing & Revenue Intelligence
    "PricingEvent",
    "PricingRecommendation",
    "BookingHistory",
    "DemandForecast",
    # Travel - Personalized Travel Intelligence
    "TravelerProfile",
    "TravelerIntent",
    "RecommendationResult",
    "ConversationContext",
    # Travel - Operational Intelligence
    "RouteSegment",
    "RouteOptimization",
    "HotelProfile",
    "HotelMatch",
]
