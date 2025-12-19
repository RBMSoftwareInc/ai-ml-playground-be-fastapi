"""
DevLab Models
For code sandbox, reverse engineering, testing, and API builder
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class ExecutionStatus(enum.Enum):
    """Code execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    KILLED = "killed"


class AnalysisType(enum.Enum):
    """Code analysis type"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    COMPLEXITY = "complexity"
    DEPENDENCY = "dependency"


class DevLabProject(Base):
    """DevLab project model"""
    __tablename__ = "devlab_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    language = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    environment = Column(String(50), default='dev')  # 'dev', 'staging', 'prod'
    is_active = Column(Boolean, default=True)
    meta_data = Column(JSON)  # Project metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    files = relationship("DevLabFile", back_populates="project", cascade="all, delete-orphan")
    executions = relationship("DevLabExecution", back_populates="project")
    analyses = relationship("DevLabAnalysis", back_populates="project")
    tests = relationship("DevLabTest", back_populates="project")


class DevLabFile(Base):
    """DevLab file model"""
    __tablename__ = "devlab_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), ForeignKey("devlab_projects.project_id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    content = Column(Text)
    language = Column(String(50))
    file_type = Column(String(50))  # 'code', 'test', 'config', 'documentation'
    size_bytes = Column(Integer)
    encoding = Column(String(50), default='utf-8')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("DevLabProject", back_populates="files")


class DevLabExecution(Base):
    """Code execution log"""
    __tablename__ = "devlab_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), ForeignKey("devlab_projects.project_id"), nullable=False)
    file_id = Column(Integer, ForeignKey("devlab_files.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    language = Column(String(50), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING, index=True)
    output = Column(Text)
    error = Column(Text)
    exit_code = Column(Integer)
    execution_time_ms = Column(Integer)
    memory_used_mb = Column(Float)
    cpu_time_seconds = Column(Float)
    container_id = Column(String(255))  # Docker container ID
    security_scan_result = Column(JSON)  # Security scan results
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    project = relationship("DevLabProject", back_populates="executions")


class DevLabAnalysis(Base):
    """Code analysis results"""
    __tablename__ = "devlab_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), ForeignKey("devlab_projects.project_id"), nullable=False)
    file_id = Column(Integer, ForeignKey("devlab_files.id"), nullable=True)
    analysis_type = Column(Enum(AnalysisType), nullable=False, index=True)
    code_snippet = Column(Text)
    findings = Column(JSON)  # Array of findings
    severity = Column(String(50))  # 'low', 'medium', 'high', 'critical'
    confidence = Column(Float)
    suggestions = Column(JSON)  # Array of suggestions
    model_version = Column(String(50))  # Model version used
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    project = relationship("DevLabProject", back_populates="analyses")


class DevLabTest(Base):
    """Test execution and generation"""
    __tablename__ = "devlab_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), ForeignKey("devlab_projects.project_id"), nullable=False)
    test_name = Column(String(255), nullable=False)
    test_type = Column(String(50))  # 'unit', 'integration', 'e2e'
    framework = Column(String(50))  # 'jest', 'pytest', 'junit', etc.
    test_code = Column(Text)
    status = Column(String(50), default='pending')  # 'pending', 'pass', 'fail', 'error'
    duration_ms = Column(Integer)
    coverage_percentage = Column(Float)
    generated_by_ai = Column(Boolean, default=False)
    model_version = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("DevLabProject", back_populates="tests")


class DevLabVulnerability(Base):
    """Security vulnerabilities detected"""
    __tablename__ = "devlab_vulnerabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), ForeignKey("devlab_projects.project_id"), nullable=False)
    file_id = Column(Integer, ForeignKey("devlab_files.id"), nullable=True)
    vulnerability_type = Column(String(100), nullable=False)  # 'sql_injection', 'xss', 'csrf', etc.
    severity = Column(String(50), nullable=False)  # 'low', 'medium', 'high', 'critical'
    description = Column(Text, nullable=False)
    code_location = Column(JSON)  # {line, column, file_path}
    cve_id = Column(String(50))  # CVE identifier if applicable
    fix_suggestion = Column(Text)
    is_fixed = Column(Boolean, default=False)
    detected_by = Column(String(100))  # Tool/model that detected it
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class DevLabInsight(Base):
    """AI insights for code"""
    __tablename__ = "devlab_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(100), ForeignKey("devlab_projects.project_id"), nullable=True)
    file_id = Column(Integer, ForeignKey("devlab_files.id"), nullable=True)
    insight_type = Column(String(50), nullable=False, index=True)  # 'optimization', 'security', 'refactor', 'test', 'dependency'
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    action = Column(String(255))  # Suggested action
    code_reference = Column(JSON)  # Reference to code location
    priority = Column(String(50))  # 'low', 'medium', 'high'
    is_applied = Column(Boolean, default=False)
    model_version = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

