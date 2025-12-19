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
]
