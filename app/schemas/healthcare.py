"""
Healthcare-specific schemas for use case metadata
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from enum import Enum


class DataSourceType(str, Enum):
    """Data source type"""
    TEST = "test"
    ACTUAL = "actual"
    SYNTHETIC = "synthetic"
    MOCK = "mock"


class PipelineStep(BaseModel):
    """AI pipeline processing step"""
    step_id: str
    step_name: str
    description: str
    input_type: str
    output_type: str
    model_used: Optional[str] = None
    processing_time_ms: Optional[float] = None
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class Classification(BaseModel):
    """Classification result"""
    category: str
    label: str
    confidence: float
    explanation: Optional[str] = None


class DataMapping(BaseModel):
    """Data mapping information"""
    field_name: str
    field_type: str
    description: str
    source: DataSourceType
    example_value: Any
    required: bool = True
    validation_rules: Optional[List[str]] = None


class UseCaseTheory(BaseModel):
    """Use case theory and educational content"""
    overview: str
    problem_statement: str
    solution_approach: str
    ai_techniques: List[str]
    benefits: List[str]
    limitations: List[str]
    best_practices: List[str]
    references: Optional[List[str]] = None


class UseCaseStats(BaseModel):
    """Use case statistics"""
    total_executions: int = 0
    success_rate: float = 0.0
    average_confidence: float = 0.0
    average_latency_ms: float = 0.0
    data_points_processed: int = 0
    model_versions_used: List[str] = []


class InputSchema(BaseModel):
    """Input schema definition"""
    schema_name: str
    fields: List[DataMapping]
    example: Dict[str, Any]
    validation_schema: Optional[Dict[str, Any]] = None


class OutputSchema(BaseModel):
    """Output schema definition"""
    schema_name: str
    fields: List[DataMapping]
    example: Dict[str, Any]
    classifications: Optional[List[Classification]] = None


class UseCaseMetadata(BaseModel):
    """Comprehensive use case metadata"""
    use_case_id: str
    display_name: str
    short_description: str
    long_description: Optional[str] = None
    category: str
    theory: UseCaseTheory
    stats: UseCaseStats
    input_schema: InputSchema
    output_schema: OutputSchema
    pipeline_steps: List[PipelineStep]
    data_mapping: Dict[str, DataMapping]  # Field name -> mapping
    api_endpoint: str
    is_dynamic: bool = False
    keywords: List[str] = []
    tips: List[str] = []
    icon: Optional[str] = None


class HealthcareUseCaseResponse(BaseModel):
    """Enhanced response with use case metadata"""
    success: bool = True
    use_case_metadata: UseCaseMetadata
    execution_result: Dict[str, Any]
    pipeline_execution: List[PipelineStep]
    classifications: List[Classification]
    data_source_info: Dict[str, DataSourceType]
    confidence: Optional[float] = None
    recommendations: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class HealthcareUseCasesListResponse(BaseModel):
    """Response for listing all healthcare use cases"""
    success: bool = True
    industry: str = "healthcare"
    total_use_cases: int
    use_cases: List[UseCaseMetadata]
