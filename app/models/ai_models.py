"""
AI Model Management Models
For tracking model versions, metrics, and deployments
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ModelVersion(Base):
    """Model version tracking"""
    __tablename__ = "model_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    model_type = Column(String(50), nullable=False, index=True)  # 'intent_classifier', 'code_understanding', 'conversational', etc.
    training_strategy = Column(String(50))  # 'pretrained', 'fine_tuned', 'custom'
    file_path = Column(String(500))  # Path to model file
    training_data_version = Column(String(50))
    training_data_source = Column(String(100))  # 'public_only', 'rbm_codebase', 'mixed'
    base_model = Column(String(100))  # Base model name (e.g., 'codebert', 'gpt-4')
    external_service = Column(String(50))  # 'openai', 'anthropic', 'self_hosted', 'hybrid'
    parameters = Column(JSON)  # Model parameters and hyperparameters
    description = Column(Text)
    is_active = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    metrics = relationship("ModelMetric", back_populates="model_version")
    deployments = relationship("ModelDeployment", back_populates="model_version")


class ModelMetric(Base):
    """Model performance metrics"""
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version_id = Column(Integer, ForeignKey("model_versions.id"), nullable=False)
    metric_type = Column(String(50), nullable=False)  # 'accuracy', 'precision', 'recall', 'f1', 'latency'
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    dataset_type = Column(String(50))  # 'train', 'validation', 'test'
    evaluation_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    # Relationships
    model_version = relationship("ModelVersion", back_populates="metrics")


class ModelDeployment(Base):
    """Model deployment tracking"""
    __tablename__ = "model_deployments"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version_id = Column(Integer, ForeignKey("model_versions.id"), nullable=False)
    environment = Column(String(50), nullable=False)  # 'dev', 'staging', 'prod'
    endpoint_url = Column(String(500))
    deployment_status = Column(String(50), default='pending')  # 'pending', 'deployed', 'failed', 'rolled_back'
    deployed_at = Column(DateTime(timezone=True))
    rolled_back_at = Column(DateTime(timezone=True))
    deployment_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    model_version = relationship("ModelVersion", back_populates="deployments")

