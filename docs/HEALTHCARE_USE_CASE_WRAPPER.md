# Healthcare Use Case Comprehensive Wrapper

## Overview

The Healthcare API has been enhanced with a comprehensive wrapper that provides detailed metadata for each use case, including:

- **Theory & Statistics**: Educational content, problem statements, AI techniques, benefits, limitations
- **Input/Output Schemas**: Detailed field definitions with data type, source (test/actual), examples
- **AI Pipeline Processing**: Step-by-step execution tracking with processing times and model versions
- **Classifications**: AI-generated classifications with confidence scores and explanations
- **Data Mappings**: Clear indication of which data is test vs actual
- **Recommendations**: Actionable insights and best practices

## Architecture

### Components

1. **Schemas** (`app/schemas/healthcare.py`)
   - `UseCaseMetadata`: Complete use case information
   - `UseCaseTheory`: Educational content and AI approach
   - `UseCaseStats`: Execution statistics
   - `InputSchema` / `OutputSchema`: Data structure definitions
   - `PipelineStep`: AI processing step details
   - `Classification`: AI classification results
   - `DataMapping`: Field-level data source information
   - `HealthcareUseCaseResponse`: Enhanced API response

2. **Metadata Service** (`app/services/healthcare_metadata_service.py`)
   - Provides comprehensive metadata for all healthcare use cases
   - Centralized definition of theory, schemas, pipelines, and data mappings

3. **API Endpoints** (`app/api/v1/healthcare.py`)
   - Enhanced endpoints with metadata wrapper
   - New endpoints for listing and querying use cases

## Use Cases Covered

1. **Patient Risk Scoring** (`risk-scoring`)
   - Risk assessment based on vitals, lab results, medical history
   - 5-step AI pipeline: Validation → Feature Extraction → Risk Calculation → Classification → Recommendations

2. **Diagnostic AI** (`diagnostic-ai`)
   - Medical image analysis (X-rays, CT scans, MRIs)
   - 5-step AI pipeline: Preprocessing → Feature Extraction → Abnormality Detection → Classification → Report Generation

3. **Drug Discovery** (`drug-discovery`)
   - Molecular analysis and drug candidate screening
   - 4-step AI pipeline: Molecular Parsing → Property Prediction → Virtual Screening → Ranking

4. **Clinical Trials** (`clinical-trials`)
   - Patient matching and enrollment forecasting
   - 4-step AI pipeline: Criteria Parsing → Patient Matching → Enrollment Forecasting → Optimization

5. **Patient Flow** (`patient-flow`)
   - Admission and bed requirement forecasting
   - 5-step AI pipeline: Data Preparation → Feature Engineering → Forecasting → Capacity Planning → Recommendations

6. **Resource Allocation** (`resource-allocation`)
   - Hospital resource optimization
   - 5-step AI pipeline: Demand Analysis → Constraint Modeling → Optimization → Efficiency Calculation → Recommendations

## API Endpoints

### 1. Get All Healthcare Use Cases

```http
GET /api/v1/healthcare/use-cases
```

**Query Parameters:**
- `include_inactive` (bool, default: false): Include inactive use cases

**Response:**
```json
{
  "success": true,
  "industry": "healthcare",
  "total_use_cases": 6,
  "use_cases": [
    {
      "use_case_id": "risk-scoring",
      "display_name": "Patient Risk Scoring",
      "short_description": "...",
      "theory": {
        "overview": "...",
        "problem_statement": "...",
        "solution_approach": "...",
        "ai_techniques": [...],
        "benefits": [...],
        "limitations": [...],
        "best_practices": [...]
      },
      "stats": {...},
      "input_schema": {...},
      "output_schema": {...},
      "pipeline_steps": [...],
      "data_mapping": {...}
    }
  ]
}
```

### 2. Get Specific Use Case Metadata

```http
GET /api/v1/healthcare/use-cases/{use_case_id}
```

**Response:**
```json
{
  "success": true,
  "use_case_metadata": {...},
  "execution_result": {},
  "pipeline_execution": [...],
  "classifications": [],
  "data_source_info": {}
}
```

### 3. Execute Use Case with Metadata

All existing POST endpoints now return comprehensive metadata:

```http
POST /api/v1/healthcare/risk-scoring
```

**Query Parameters:**
- `include_metadata` (bool, default: true): Include use case metadata in response
- `track_pipeline` (bool, default: true): Track AI pipeline execution steps

**Request Body:**
```json
{
  "patient_id": "PAT-12345",
  "vitals": {
    "bp": 140,
    "heart_rate": 85,
    "temperature": 98.6
  },
  "lab_results": [
    {"test": "glucose", "value": 95, "unit": "mg/dL"}
  ],
  "medical_history": [
    {"condition": "diabetes", "diagnosed_date": "2020-01-15"}
  ],
  "current_medications": ["metformin", "aspirin"]
}
```

**Response:**
```json
{
  "success": true,
  "use_case_metadata": {
    "use_case_id": "risk-scoring",
    "display_name": "Patient Risk Scoring",
    "theory": {
      "overview": "Patient risk scoring uses machine learning...",
      "problem_statement": "Healthcare providers need to identify...",
      "solution_approach": "We use ensemble machine learning models...",
      "ai_techniques": [
        "Supervised Learning (Classification)",
        "Ensemble Methods (Random Forest, XGBoost)",
        "Feature Engineering",
        "Risk Stratification",
        "Predictive Analytics"
      ],
      "benefits": [
        "Early identification of high-risk patients",
        "Reduced hospital readmissions",
        "Improved resource allocation"
      ],
      "limitations": [
        "Requires high-quality, complete patient data",
        "Model accuracy depends on training data quality"
      ],
      "best_practices": [
        "Regularly update models with new data",
        "Validate predictions with clinical judgment"
      ]
    },
    "input_schema": {
      "schema_name": "RiskScoringRequest",
      "fields": [
        {
          "field_name": "patient_id",
          "field_type": "string",
          "description": "Unique patient identifier",
          "source": "actual",
          "example_value": "PAT-12345",
          "required": true
        },
        {
          "field_name": "vitals",
          "field_type": "object",
          "description": "Vital signs measurements",
          "source": "actual",
          "example_value": {"bp": 140, "heart_rate": 85},
          "required": false
        }
      ],
      "example": {...}
    },
    "output_schema": {
      "schema_name": "RiskScoringResponse",
      "fields": [...],
      "example": {...},
      "classifications": [
        {
          "category": "Risk Level",
          "label": "high",
          "confidence": 0.85,
          "explanation": "High risk due to elevated BP..."
        }
      ]
    },
    "pipeline_steps": [
      {
        "step_id": "data_validation",
        "step_name": "Data Validation",
        "description": "Validate and normalize input patient data",
        "input_type": "RiskScoringRequest",
        "output_type": "ValidatedData",
        "processing_time_ms": 5.0
      },
      {
        "step_id": "feature_extraction",
        "step_name": "Feature Extraction",
        "description": "Extract relevant features from patient data",
        "input_type": "ValidatedData",
        "output_type": "FeatureVector",
        "model_used": "feature_extractor_v1",
        "processing_time_ms": 15.0
      },
      {
        "step_id": "risk_calculation",
        "step_name": "Risk Score Calculation",
        "description": "Calculate composite risk score using ensemble model",
        "input_type": "FeatureVector",
        "output_type": "RiskScore",
        "model_used": "risk_scoring_model_v2",
        "confidence": 0.85,
        "processing_time_ms": 50.0
      },
      {
        "step_id": "classification",
        "step_name": "Risk Level Classification",
        "description": "Classify risk into low/medium/high categories",
        "input_type": "RiskScore",
        "output_type": "RiskLevel",
        "model_used": "risk_classifier_v1",
        "confidence": 0.85,
        "processing_time_ms": 10.0
      },
      {
        "step_id": "recommendation_generation",
        "step_name": "Recommendation Generation",
        "description": "Generate personalized clinical recommendations",
        "input_type": "RiskLevel",
        "output_type": "Recommendations",
        "model_used": "recommendation_engine_v1",
        "processing_time_ms": 20.0
      }
    ],
    "data_mapping": {
      "patient_id": {
        "field_name": "patient_id",
        "field_type": "string",
        "description": "Unique patient identifier",
        "source": "actual",
        "example_value": "PAT-12345",
        "required": true
      }
    }
  },
  "execution_result": {
    "risk_score": 0.65,
    "risk_level": "high",
    "recommendations": [
      "Regular monitoring",
      "Lifestyle modifications",
      "Consider specialist consultation"
    ]
  },
  "pipeline_execution": [
    {
      "step_id": "data_validation",
      "step_name": "Data Validation",
      "processing_time_ms": 4.2
    },
    {
      "step_id": "feature_extraction",
      "step_name": "Feature Extraction",
      "model_used": "feature_extractor_v1",
      "processing_time_ms": 14.8
    },
    {
      "step_id": "risk_calculation",
      "step_name": "Risk Score Calculation",
      "model_used": "risk_scoring_model_v2",
      "confidence": 0.85,
      "processing_time_ms": 48.5
    },
    {
      "step_id": "classification",
      "step_name": "Risk Level Classification",
      "model_used": "risk_classifier_v1",
      "confidence": 0.85,
      "processing_time_ms": 9.2
    },
    {
      "step_id": "recommendation_generation",
      "step_name": "Recommendation Generation",
      "model_used": "recommendation_engine_v1",
      "processing_time_ms": 18.7
    }
  ],
  "classifications": [
    {
      "category": "Risk Level",
      "label": "high",
      "confidence": 0.85,
      "explanation": "Risk level classified as high based on composite score of 0.65"
    }
  ],
  "data_source_info": {
    "patient_id": "actual",
    "vitals": "actual",
    "lab_results": "actual",
    "medical_history": "actual",
    "current_medications": "actual"
  },
  "confidence": 0.85,
  "recommendations": [
    "Regular monitoring",
    "Lifestyle modifications",
    "Consider specialist consultation"
  ],
  "metadata": {
    "total_processing_time_ms": 95.4,
    "model_version": "risk_scoring_model_v2",
    "data_points_processed": 3
  }
}
```

## Data Source Types

Each field in the input/output schemas includes a `source` field indicating the data type:

- **`actual`**: Real patient/clinical data
- **`test`**: Test/simulated data for development
- **`synthetic`**: AI-generated synthetic data
- **`mock`**: Mock data for demonstrations

## AI Pipeline Processing

Each use case defines a multi-step AI pipeline:

1. **Data Validation/Preprocessing**: Input validation and normalization
2. **Feature Extraction**: Extract relevant features from raw data
3. **Model Inference**: Run AI/ML models for prediction/analysis
4. **Classification**: Categorize results
5. **Post-processing**: Generate recommendations, reports, etc.

Each step includes:
- Step ID and name
- Description
- Input/output types
- Model used (if applicable)
- Processing time
- Confidence score (if applicable)

## Classifications

AI-generated classifications provide:
- **Category**: Classification category (e.g., "Risk Level", "Image Classification")
- **Label**: The classification result (e.g., "high", "normal")
- **Confidence**: Confidence score (0.0 to 1.0)
- **Explanation**: Human-readable explanation

## Use Case Theory

Each use case includes comprehensive educational content:

- **Overview**: High-level description
- **Problem Statement**: The problem being solved
- **Solution Approach**: How AI solves the problem
- **AI Techniques**: List of ML/AI techniques used
- **Benefits**: Expected benefits
- **Limitations**: Known limitations
- **Best Practices**: Recommended practices
- **References**: Related resources

## Statistics

Use case statistics track:
- Total executions
- Success rate
- Average confidence
- Average latency
- Data points processed
- Model versions used

## Example Usage

### Python Client

```python
import requests

# Get all use cases
response = requests.get("http://localhost:5000/api/v1/healthcare/use-cases")
use_cases = response.json()

# Get specific use case metadata
response = requests.get("http://localhost:5000/api/v1/healthcare/use-cases/risk-scoring")
metadata = response.json()

# Execute use case with full metadata
response = requests.post(
    "http://localhost:5000/api/v1/healthcare/risk-scoring",
    json={
        "patient_id": "PAT-12345",
        "vitals": {"bp": 140, "heart_rate": 85},
        "lab_results": [],
        "medical_history": [],
        "current_medications": []
    },
    params={
        "include_metadata": True,
        "track_pipeline": True
    }
)
result = response.json()

# Access different parts of the response
print("Theory:", result["use_case_metadata"]["theory"]["overview"])
print("Pipeline Steps:", len(result["pipeline_execution"]))
print("Classifications:", result["classifications"])
print("Data Sources:", result["data_source_info"])
```

### cURL

```bash
# Get all use cases
curl -X GET "http://localhost:5000/api/v1/healthcare/use-cases"

# Get specific use case
curl -X GET "http://localhost:5000/api/v1/healthcare/use-cases/risk-scoring"

# Execute use case
curl -X POST "http://localhost:5000/api/v1/healthcare/risk-scoring?include_metadata=true&track_pipeline=true" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT-12345",
    "vitals": {"bp": 140, "heart_rate": 85},
    "lab_results": [],
    "medical_history": [],
    "current_medications": []
  }'
```

## Benefits

1. **Educational**: Complete theory and approach for each use case
2. **Transparent**: Clear visibility into AI pipeline processing
3. **Traceable**: Track data sources (test vs actual)
4. **Actionable**: Recommendations and best practices
5. **Comprehensive**: All information in one response
6. **Flexible**: Can disable metadata for lightweight responses

## Future Enhancements

- Integration with database to track actual execution statistics
- Real-time model version tracking
- Performance metrics aggregation
- A/B testing support
- Model explainability features
- Integration with use_case_executions table for historical tracking

