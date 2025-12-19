"""
Training Data Models
For AI model training and content management
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.database import Base


class ContentChunk(Base):
    """Content chunks for embeddings and semantic search"""
    __tablename__ = "content_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    use_case_id = Column(String(100), ForeignKey("use_cases.use_case_id"), nullable=True)
    discovery_tool_id = Column(String(100), ForeignKey("discovery_tools.tool_id"), nullable=True)
    content_type = Column(String(50), nullable=False, index=True)  # 'theory', 'tip', 'description', 'scenario', 'copilot_knowledge'
    content_text = Column(Text, nullable=False)
    source = Column(String(100))  # 'component', 'json', 'documentation', 'user_generated'
    source_file = Column(String(500))  # Original file path
    meta_data = Column(JSON)  # Additional metadata
    embedding = Column(JSON)  # Vector embedding for semantic search (stored as JSON array)
    embedding_model = Column(String(100))  # Model used for embedding
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TrainingDataset(Base):
    """Training datasets for model training"""
    __tablename__ = "training_datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    dataset_type = Column(String(50), nullable=False)  # 'conversation', 'code', 'simulation', 'general'
    use_case_ids = Column(ARRAY(String))  # Array of use case IDs
    description = Column(Text)
    data_snapshot = Column(JSON)  # Full data at time of training
    data_source = Column(String(100))  # 'frontend', 'public_repos', 'rbm_codebase', 'mixed'
    record_count = Column(Integer, default=0)
    file_path = Column(String(500))  # Path to dataset file
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)


class ConversationExample(Base):
    """Conversation examples for conversational AI training"""
    __tablename__ = "conversation_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    context = Column(JSON)  # {industry, use_case, conversation_history}
    use_case_id = Column(String(100), ForeignKey("use_cases.use_case_id"), nullable=True)
    suggestions = Column(ARRAY(String))  # Array of suggested follow-ups
    source = Column(String(50))  # 'synthetic', 'real', 'template'
    quality_score = Column(Float)  # Quality rating
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulationExample(Base):
    """Interactive simulation examples for training"""
    __tablename__ = "simulation_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(String(100), nullable=False, index=True)
    scenario_id = Column(String(100), nullable=False)
    input_data = Column(JSON, nullable=False)
    expected_output = Column(JSON, nullable=False)
    pipeline_steps = Column(JSON)  # Pipeline step data
    business_impact = Column(JSON)  # Impact metrics
    source = Column(String(50))  # 'json_config', 'user_generated', 'synthetic'
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CodeExample(Base):
    """Code examples for DevLab training"""
    __tablename__ = "code_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False, index=True)
    code_type = Column(String(50))  # 'function', 'class', 'script', 'test'
    description = Column(Text)
    explanation = Column(Text)  # Code explanation
    test_code = Column(Text)  # Associated test code
    refactored_code = Column(Text)  # Refactored version
    security_issues = Column(JSON)  # Detected security issues
    performance_notes = Column(Text)
    complexity_score = Column(Float)
    source = Column(String(50))  # 'public_repo', 'rbm_codebase', 'synthetic'
    source_repo = Column(String(500))
    embedding = Column(JSON)  # Code embedding
    created_at = Column(DateTime(timezone=True), server_default=func.now())

