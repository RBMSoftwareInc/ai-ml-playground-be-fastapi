# Healthcare API - Live Analysis Implementation

## ✅ Status: Live ML Analysis (Not Mock)

The Healthcare API now uses **real ML models** for analysis, not mock data. All calculations are performed using trained machine learning models.

## 🔬 ML Models Used

### Risk Scoring Model
- **Model Type**: RandomForestRegressor (scikit-learn)
- **Features**: 7 input features
  - BP Systolic
  - BP Diastolic  
  - Heart Rate
  - Temperature
  - Medical History Count
  - Medication Count
  - Abnormal Lab Count
- **Output**: Risk score (0.0 to 1.0) with confidence
- **Training**: Model trained on synthetic medical data (can be replaced with real data)

## 📊 API Response Structure for Tabs

### Main Endpoint: `POST /api/v1/healthcare/risk-scoring`

Returns comprehensive data for all tabs:

```json
{
  "success": true,
  "use_case_metadata": {
    "theory": { ... }  // For THEORY tab
  },
  "execution_result": {
    "risk_score": 0.65,
    "risk_score_percentage": 65,  // For RESULT tab display
    "risk_level": "high",
    "recommendations": [...],
    "insights": { ... }  // For INSIGHTS tab
  },
  "pipeline_execution": [...],  // For detailed analysis
  "classifications": [...],
  "metadata": {
    "analysis_type": "live_ml_analysis"  // Indicates live analysis
  }
}
```

### Tab-Specific Endpoints

#### 1. **RESULT Tab**
- **Data Source**: `execution_result` in main response
- **Fields**:
  - `risk_score`: 0.0 to 1.0
  - `risk_score_percentage`: 0 to 100 (for display)
  - `risk_level`: "low", "medium", "high"
  - `recommendations`: List of recommendations
  - `confidence`: Model confidence score

#### 2. **THEORY Tab**
- **Data Source**: `use_case_metadata.theory` in main response
- **Fields**:
  - `overview`: High-level description
  - `problem_statement`: Problem being solved
  - `solution_approach`: How AI solves it
  - `ai_techniques`: List of ML techniques used
  - `benefits`: Expected benefits
  - `limitations`: Known limitations
  - `best_practices`: Recommended practices

#### 3. **DATASET Tab**
- **Endpoint**: `GET /api/v1/healthcare/risk-scoring/dataset`
- **Returns**: Sample/test data for demonstration
- **Fields**:
  - `dataset`: Array of sample patient records
  - `total_samples`: Number of samples
  - `description`: Dataset description
  - `fields`: Field definitions

#### 4. **INSIGHTS Tab**
- **Endpoint**: `POST /api/v1/healthcare/risk-scoring/insights`
- **Also included in**: `execution_result.insights` in main response
- **Returns**:
  - `vital_trends`: Analysis of vital signs
  - `lab_analysis`: Lab result analysis
  - `risk_trends`: Risk trend analysis
  - `comparative_analysis`: Population comparisons
  - `analytics`: Model performance metrics
  - `feature_contributions`: Top contributing factors

## 🔧 Fixed Issues

### 1. Medical History Validation
- **Problem**: `medical_history` was required but could be None
- **Fix**: Made `medical_history` and `current_medications` optional with default empty lists
- **Code**: `Optional[List[Dict[str, Any]]] = []`

### 2. Mock Data → Live Analysis
- **Before**: Simple rule-based calculations
- **After**: Real ML model (RandomForestRegressor) with feature importance
- **Evidence**: `metadata.analysis_type: "live_ml_analysis"`

## 📝 Example Request/Response

### Request
```bash
POST /api/v1/healthcare/risk-scoring
Content-Type: application/json

{
  "patient_id": "PAT-12345",
  "vitals": {
    "bp_systolic": 145,
    "bp_diastolic": 95,
    "heart_rate": 95,
    "temperature": 99.2
  },
  "lab_results": [
    {"test": "glucose", "value": 110, "unit": "mg/dL"},
    {"test": "cholesterol", "value": 220, "unit": "mg/dL"}
  ],
  "medical_history": [
    {"condition": "Type 2 Diabetes", "diagnosed_date": "2019-05-20"}
  ],
  "current_medications": ["metformin", "lisinopril"]
}
```

### Response (Key Fields for Tabs)

```json
{
  "success": true,
  "execution_result": {
    "risk_score": 0.68,
    "risk_score_percentage": 68,
    "risk_level": "high",
    "confidence": 0.92,
    "recommendations": [
      "Regular monitoring",
      "Lifestyle modifications",
      "Consider specialist consultation"
    ],
    "top_contributing_factors": [
      {
        "factor": "BP Systolic",
        "value": 145.0,
        "importance": 0.28
      },
      {
        "factor": "History Count",
        "value": 1.0,
        "importance": 0.22
      }
    ],
    "insights": {
      "vital_trends": {
        "blood_pressure": {
          "status": "high",
          "systolic": 145,
          "diastolic": 95,
          "category": "High Stage 2"
        },
        "heart_rate": {
          "status": "normal",
          "value": 95,
          "normal_range": {"min": 60, "max": 100}
        }
      },
      "lab_analysis": {
        "tests": {
          "glucose": {
            "value": 110,
            "unit": "mg/dL",
            "status": "high"
          },
          "cholesterol": {
            "value": 220,
            "unit": "mg/dL",
            "status": "high"
          }
        },
        "abnormal_count": 2,
        "total_tests": 2
      },
      "risk_trends": {
        "current_risk": 0.68,
        "risk_category": "high",
        "trend": "increasing"
      }
    }
  },
  "use_case_metadata": {
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
      "benefits": [...],
      "limitations": [...],
      "best_practices": [...]
    }
  },
  "metadata": {
    "analysis_type": "live_ml_analysis",
    "model_version": "RandomForestRegressor"
  }
}
```

## 🎯 Frontend Integration

### Tab Data Mapping

1. **RESULT Tab**:
   ```javascript
   const resultData = response.execution_result;
   // Display: risk_score_percentage, risk_level, recommendations
   ```

2. **THEORY Tab**:
   ```javascript
   const theoryData = response.use_case_metadata?.theory;
   // Display: overview, problem_statement, solution_approach, etc.
   ```

3. **DATASET Tab**:
   ```javascript
   // Fetch separately
   const datasetResponse = await fetch('/api/v1/healthcare/risk-scoring/dataset');
   const datasetData = datasetResponse.data;
   // Display: sample patient records
   ```

4. **INSIGHTS Tab**:
   ```javascript
   // Option 1: From main response
   const insights = response.execution_result.insights;
   
   // Option 2: Fetch detailed insights
   const insightsResponse = await fetch('/api/v1/healthcare/risk-scoring/insights', {
     method: 'POST',
     body: JSON.stringify(requestData)
   });
   // Display: vital_trends, lab_analysis, risk_trends, analytics
   ```

## 🚀 Next Steps

1. **Remove Copilot Tab**: Not included in API responses
2. **Use Dynamic Data**: All tabs now use API data, not static/mock
3. **Live Analysis**: All calculations use real ML models
4. **Feature Importance**: Model provides feature importance for explainability

## 📊 Model Training

The current model is trained on synthetic data. To use real medical data:

1. Collect labeled patient data
2. Train RandomForestRegressor on real dataset
3. Save model to `trained_models/healthcare_risk_model.pkl`
4. Model will auto-load on service initialization

## ✅ Verification

To verify live analysis:
- Check `metadata.analysis_type` = `"live_ml_analysis"`
- Check `model_used` = `"RandomForestRegressor"`
- Check `feature_importance` exists in response
- Risk scores vary based on actual input features (not fixed rules)

