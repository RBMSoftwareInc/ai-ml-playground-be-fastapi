"""
Healthcare Use Case Metadata Service
Provides comprehensive metadata for healthcare use cases including theory, stats, inputs, outputs, and pipeline
"""
from typing import Dict, List, Optional
from app.schemas.healthcare import (
    UseCaseMetadata,
    UseCaseTheory,
    UseCaseStats,
    InputSchema,
    OutputSchema,
    PipelineStep,
    DataMapping,
    Classification,
    DataSourceType
)


class HealthcareMetadataService:
    """Service for healthcare use case metadata"""
    
    @staticmethod
    def get_use_case_metadata(use_case_id: str) -> Optional[UseCaseMetadata]:
        """Get metadata for a specific use case"""
        metadata_map = HealthcareMetadataService._get_metadata_map()
        return metadata_map.get(use_case_id)
    
    @staticmethod
    def get_all_use_cases() -> List[UseCaseMetadata]:
        """Get all healthcare use case metadata"""
        return list(HealthcareMetadataService._get_metadata_map().values())
    
    @staticmethod
    def _get_metadata_map() -> Dict[str, UseCaseMetadata]:
        """Get all healthcare use case metadata"""
        return {
            "risk-scoring": UseCaseMetadata(
                use_case_id="risk-scoring",
                display_name="Patient Risk Scoring",
                short_description="AI-powered risk assessment for patients based on vitals, lab results, and medical history",
                long_description="Comprehensive patient risk scoring system that analyzes multiple data points including vital signs, laboratory results, medical history, and current medications to predict potential health risks and recommend preventive measures.",
                category="Clinical Decision Support",
                theory=UseCaseTheory(
                    overview="Patient risk scoring uses machine learning to analyze patient data and predict the likelihood of adverse health events. It combines clinical data, historical patterns, and predictive modeling to assist healthcare providers in making informed decisions.",
                    problem_statement="Healthcare providers need to identify high-risk patients early to prevent complications, reduce hospital readmissions, and optimize resource allocation. Manual risk assessment is time-consuming and may miss subtle patterns in complex patient data.",
                    solution_approach="We use ensemble machine learning models (Random Forest, Gradient Boosting, Neural Networks) trained on historical patient data to identify risk factors and calculate composite risk scores. The system processes structured data (vitals, labs) and unstructured data (medical notes) to provide comprehensive risk assessment.",
                    ai_techniques=[
                        "Supervised Learning (Classification)",
                        "Ensemble Methods (Random Forest, XGBoost)",
                        "Feature Engineering",
                        "Risk Stratification",
                        "Predictive Analytics"
                    ],
                    benefits=[
                        "Early identification of high-risk patients",
                        "Reduced hospital readmissions",
                        "Improved resource allocation",
                        "Personalized care recommendations",
                        "Cost reduction through preventive care"
                    ],
                    limitations=[
                        "Requires high-quality, complete patient data",
                        "Model accuracy depends on training data quality",
                        "May not capture rare conditions",
                        "Requires regular model retraining",
                        "Ethical considerations around bias"
                    ],
                    best_practices=[
                        "Regularly update models with new data",
                        "Validate predictions with clinical judgment",
                        "Ensure data privacy and HIPAA compliance",
                        "Monitor model performance metrics",
                        "Involve clinicians in model development"
                    ],
                    references=[
                        "Clinical Decision Support Systems in Healthcare",
                        "Machine Learning for Risk Stratification",
                        "Predictive Analytics in Medicine"
                    ]
                ),
                stats=UseCaseStats(
                    total_executions=0,
                    success_rate=0.0,
                    average_confidence=0.0,
                    average_latency_ms=0.0,
                    data_points_processed=0,
                    model_versions_used=[]
                ),
                input_schema=InputSchema(
                    schema_name="RiskScoringRequest",
                    fields=[
                        DataMapping(
                            field_name="patient_id",
                            field_type="string",
                            description="Unique patient identifier",
                            source=DataSourceType.ACTUAL,
                            example_value="PAT-12345",
                            required=True,
                            validation_rules=["non-empty", "alphanumeric"]
                        ),
                        DataMapping(
                            field_name="vitals",
                            field_type="object",
                            description="Vital signs measurements (BP, heart rate, temperature, etc.)",
                            source=DataSourceType.ACTUAL,
                            example_value={"bp": 140, "heart_rate": 85, "temperature": 98.6},
                            required=False
                        ),
                        DataMapping(
                            field_name="lab_results",
                            field_type="array",
                            description="Laboratory test results",
                            source=DataSourceType.ACTUAL,
                            example_value=[{"test": "glucose", "value": 95, "unit": "mg/dL"}],
                            required=False
                        ),
                        DataMapping(
                            field_name="medical_history",
                            field_type="array",
                            description="Historical medical conditions and diagnoses",
                            source=DataSourceType.ACTUAL,
                            example_value=[{"condition": "diabetes", "diagnosed_date": "2020-01-15"}],
                            required=False
                        ),
                        DataMapping(
                            field_name="current_medications",
                            field_type="array",
                            description="List of current medications",
                            source=DataSourceType.ACTUAL,
                            example_value=["metformin", "aspirin"],
                            required=False
                        )
                    ],
                    example={
                        "patient_id": "PAT-12345",
                        "vitals": {"bp": 140, "heart_rate": 85, "temperature": 98.6},
                        "lab_results": [{"test": "glucose", "value": 95, "unit": "mg/dL"}],
                        "medical_history": [{"condition": "diabetes", "diagnosed_date": "2020-01-15"}],
                        "current_medications": ["metformin", "aspirin"]
                    }
                ),
                output_schema=OutputSchema(
                    schema_name="RiskScoringResponse",
                    fields=[
                        DataMapping(
                            field_name="risk_score",
                            field_type="float",
                            description="Composite risk score (0.0 to 1.0)",
                            source=DataSourceType.TEST,
                            example_value=0.65,
                            required=True
                        ),
                        DataMapping(
                            field_name="risk_level",
                            field_type="string",
                            description="Categorical risk level (low, medium, high)",
                            source=DataSourceType.TEST,
                            example_value="high",
                            required=True
                        ),
                        DataMapping(
                            field_name="recommendations",
                            field_type="array",
                            description="Clinical recommendations based on risk assessment",
                            source=DataSourceType.TEST,
                            example_value=["Regular monitoring", "Lifestyle modifications"],
                            required=True
                        )
                    ],
                    example={
                        "risk_score": 0.65,
                        "risk_level": "high",
                        "recommendations": ["Regular monitoring", "Lifestyle modifications"]
                    },
                    classifications=[
                        Classification(
                            category="Risk Level",
                            label="high",
                            confidence=0.85,
                            explanation="High risk due to elevated BP and multiple comorbidities"
                        )
                    ]
                ),
                pipeline_steps=[
                    PipelineStep(
                        step_id="data_validation",
                        step_name="Data Validation",
                        description="Validate and normalize input patient data",
                        input_type="RiskScoringRequest",
                        output_type="ValidatedData",
                        processing_time_ms=5.0
                    ),
                    PipelineStep(
                        step_id="feature_extraction",
                        step_name="Feature Extraction",
                        description="Extract relevant features from patient data",
                        input_type="ValidatedData",
                        output_type="FeatureVector",
                        model_used="feature_extractor_v1",
                        processing_time_ms=15.0
                    ),
                    PipelineStep(
                        step_id="risk_calculation",
                        step_name="Risk Score Calculation",
                        description="Calculate composite risk score using ensemble model",
                        input_type="FeatureVector",
                        output_type="RiskScore",
                        model_used="risk_scoring_model_v2",
                        confidence=0.85,
                        processing_time_ms=50.0
                    ),
                    PipelineStep(
                        step_id="classification",
                        step_name="Risk Level Classification",
                        description="Classify risk into low/medium/high categories",
                        input_type="RiskScore",
                        output_type="RiskLevel",
                        model_used="risk_classifier_v1",
                        confidence=0.85,
                        processing_time_ms=10.0
                    ),
                    PipelineStep(
                        step_id="recommendation_generation",
                        step_name="Recommendation Generation",
                        description="Generate personalized clinical recommendations",
                        input_type="RiskLevel",
                        output_type="Recommendations",
                        model_used="recommendation_engine_v1",
                        processing_time_ms=20.0
                    )
                ],
                data_mapping={
                    "patient_id": DataMapping(
                        field_name="patient_id",
                        field_type="string",
                        description="Unique patient identifier",
                        source=DataSourceType.ACTUAL,
                        example_value="PAT-12345",
                        required=True
                    ),
                    "vitals": DataMapping(
                        field_name="vitals",
                        field_type="object",
                        description="Vital signs measurements",
                        source=DataSourceType.ACTUAL,
                        example_value={"bp": 140, "heart_rate": 85},
                        required=False
                    )
                },
                api_endpoint="/api/v1/healthcare/risk-scoring",
                is_dynamic=False,
                keywords=["risk assessment", "patient safety", "clinical decision support", "predictive analytics"],
                tips=[
                    "Ensure all vital signs are recent (within 24 hours)",
                    "Include complete medical history for accurate assessment",
                    "Regular model updates improve accuracy",
                    "Combine with clinical judgment for best results"
                ],
                icon="🏥"
            ),
            "diagnostic-ai": UseCaseMetadata(
                use_case_id="diagnostic-ai",
                display_name="Diagnostic AI - Image Analysis",
                short_description="AI-powered medical image analysis for diagnostic support",
                long_description="Advanced computer vision system for analyzing medical images (X-rays, CT scans, MRIs, etc.) to assist radiologists in diagnosis and detect abnormalities.",
                category="Medical Imaging",
                theory=UseCaseTheory(
                    overview="Diagnostic AI uses deep learning convolutional neural networks (CNNs) to analyze medical images and identify patterns, abnormalities, and potential diagnoses. It serves as a second opinion tool for radiologists.",
                    problem_statement="Medical image interpretation is time-consuming and subject to human error. Radiologists face high workloads, and subtle abnormalities may be missed. Early detection is critical for patient outcomes.",
                    solution_approach="We use pre-trained CNN models (ResNet, DenseNet, EfficientNet) fine-tuned on medical imaging datasets. The system processes images through multiple layers to extract features and classify findings.",
                    ai_techniques=[
                        "Deep Learning (CNNs)",
                        "Transfer Learning",
                        "Image Segmentation",
                        "Object Detection",
                        "Multi-class Classification"
                    ],
                    benefits=[
                        "Faster image analysis",
                        "Improved detection accuracy",
                        "Consistent interpretation",
                        "24/7 availability",
                        "Reduced radiologist workload"
                    ],
                    limitations=[
                        "Requires high-quality images",
                        "May miss rare conditions not in training data",
                        "Cannot replace radiologist expertise",
                        "Requires regulatory approval (FDA)",
                        "Potential for false positives/negatives"
                    ],
                    best_practices=[
                        "Always use as assistive tool, not replacement",
                        "Validate findings with radiologist review",
                        "Ensure image quality standards",
                        "Regular model updates with new data",
                        "Maintain audit trails for regulatory compliance"
                    ],
                    references=[
                        "Deep Learning for Medical Image Analysis",
                        "AI in Radiology: Current Applications",
                        "FDA Guidelines for AI/ML Medical Devices"
                    ]
                ),
                stats=UseCaseStats(
                    total_executions=0,
                    success_rate=0.0,
                    average_confidence=0.0,
                    average_latency_ms=0.0,
                    data_points_processed=0,
                    model_versions_used=[]
                ),
                input_schema=InputSchema(
                    schema_name="DiagnosticImageRequest",
                    fields=[
                        DataMapping(
                            field_name="file",
                            field_type="file",
                            description="Medical image file (DICOM, PNG, JPEG)",
                            source=DataSourceType.ACTUAL,
                            example_value="image.dcm",
                            required=True,
                            validation_rules=["file_size < 10MB", "supported_format"]
                        )
                    ],
                    example={"file": "chest_xray.dcm"}
                ),
                output_schema=OutputSchema(
                    schema_name="DiagnosticImageResponse",
                    fields=[
                        DataMapping(
                            field_name="findings",
                            field_type="array",
                            description="Detected findings and abnormalities",
                            source=DataSourceType.TEST,
                            example_value=[{"type": "normal", "confidence": 0.95}],
                            required=True
                        ),
                        DataMapping(
                            field_name="confidence",
                            field_type="float",
                            description="Overall confidence score",
                            source=DataSourceType.TEST,
                            example_value=0.92,
                            required=True
                        ),
                        DataMapping(
                            field_name="recommendations",
                            field_type="array",
                            description="Clinical recommendations",
                            source=DataSourceType.TEST,
                            example_value=["Follow-up in 6 months"],
                            required=True
                        )
                    ],
                    example={
                        "findings": [{"type": "normal", "confidence": 0.95}],
                        "confidence": 0.92,
                        "recommendations": ["Follow-up in 6 months"]
                    },
                    classifications=[
                        Classification(
                            category="Image Classification",
                            label="normal",
                            confidence=0.95,
                            explanation="No abnormalities detected in the image"
                        )
                    ]
                ),
                pipeline_steps=[
                    PipelineStep(
                        step_id="image_preprocessing",
                        step_name="Image Preprocessing",
                        description="Normalize, resize, and enhance medical image",
                        input_type="RawImage",
                        output_type="ProcessedImage",
                        processing_time_ms=50.0
                    ),
                    PipelineStep(
                        step_id="feature_extraction",
                        step_name="Feature Extraction",
                        description="Extract visual features using CNN layers",
                        input_type="ProcessedImage",
                        output_type="FeatureMap",
                        model_used="resnet50_medical_v3",
                        processing_time_ms=200.0
                    ),
                    PipelineStep(
                        step_id="abnormality_detection",
                        step_name="Abnormality Detection",
                        description="Detect and localize abnormalities",
                        input_type="FeatureMap",
                        output_type="Detections",
                        model_used="yolo_medical_v2",
                        confidence=0.92,
                        processing_time_ms=150.0
                    ),
                    PipelineStep(
                        step_id="classification",
                        step_name="Image Classification",
                        description="Classify image findings",
                        input_type="Detections",
                        output_type="Classifications",
                        model_used="classifier_v4",
                        confidence=0.95,
                        processing_time_ms=100.0
                    ),
                    PipelineStep(
                        step_id="report_generation",
                        step_name="Report Generation",
                        description="Generate diagnostic report with recommendations",
                        input_type="Classifications",
                        output_type="DiagnosticReport",
                        processing_time_ms=30.0
                    )
                ],
                data_mapping={
                    "file": DataMapping(
                        field_name="file",
                        field_type="file",
                        description="Medical image file",
                        source=DataSourceType.ACTUAL,
                        example_value="image.dcm",
                        required=True
                    )
                },
                api_endpoint="/api/v1/healthcare/diagnostic-ai",
                is_dynamic=False,
                keywords=["medical imaging", "radiology", "diagnosis", "computer vision", "deep learning"],
                tips=[
                    "Ensure DICOM format for best results",
                    "Image quality directly affects accuracy",
                    "Always review with qualified radiologist",
                    "Maintain patient privacy (HIPAA compliance)"
                ],
                icon="🔬"
            ),
            "drug-discovery": UseCaseMetadata(
                use_case_id="drug-discovery",
                display_name="Drug Discovery AI",
                short_description="AI-powered molecular analysis and drug candidate screening",
                long_description="Machine learning system for analyzing molecular structures, predicting drug properties, and identifying potential drug candidates for specific diseases.",
                category="Pharmaceutical Research",
                theory=UseCaseTheory(
                    overview="Drug discovery AI uses graph neural networks and molecular property prediction models to analyze chemical structures and predict drug efficacy, toxicity, and pharmacokinetics.",
                    problem_statement="Traditional drug discovery is expensive ($2-3B per drug) and time-consuming (10-15 years). Most candidates fail in clinical trials. AI can accelerate screening and reduce costs.",
                    solution_approach="We use graph neural networks (GNNs) to model molecular structures as graphs, predict ADMET properties (Absorption, Distribution, Metabolism, Excretion, Toxicity), and screen large compound libraries.",
                    ai_techniques=[
                        "Graph Neural Networks (GNNs)",
                        "Molecular Property Prediction",
                        "Virtual Screening",
                        "Deep Learning",
                        "Reinforcement Learning (for molecular design)"
                    ],
                    benefits=[
                        "Faster candidate screening",
                        "Reduced R&D costs",
                        "Better property prediction",
                        "Identification of novel compounds",
                        "Reduced animal testing"
                    ],
                    limitations=[
                        "Requires large training datasets",
                        "Limited to known chemical space",
                        "Cannot fully replace wet lab experiments",
                        "Regulatory validation needed",
                        "Computational resource intensive"
                    ],
                    best_practices=[
                        "Combine with traditional methods",
                        "Validate predictions experimentally",
                        "Use diverse training datasets",
                        "Consider multi-objective optimization",
                        "Collaborate with pharmaceutical experts"
                    ],
                    references=[
                        "AI in Drug Discovery: A Comprehensive Review",
                        "Graph Neural Networks for Molecular Property Prediction",
                        "Virtual Screening in Pharmaceutical Research"
                    ]
                ),
                stats=UseCaseStats(
                    total_executions=0,
                    success_rate=0.0,
                    average_confidence=0.0,
                    average_latency_ms=0.0,
                    data_points_processed=0,
                    model_versions_used=[]
                ),
                input_schema=InputSchema(
                    schema_name="DrugDiscoveryRequest",
                    fields=[
                        DataMapping(
                            field_name="target_disease",
                            field_type="string",
                            description="Target disease or condition",
                            source=DataSourceType.ACTUAL,
                            example_value="Type 2 Diabetes",
                            required=True
                        ),
                        DataMapping(
                            field_name="molecular_structure",
                            field_type="string",
                            description="Molecular structure (SMILES notation)",
                            source=DataSourceType.ACTUAL,
                            example_value="CCO",
                            required=False
                        ),
                        DataMapping(
                            field_name="screening_criteria",
                            field_type="object",
                            description="Screening criteria and constraints",
                            source=DataSourceType.ACTUAL,
                            example_value={"max_molecular_weight": 500, "min_bioavailability": 0.5},
                            required=False
                        )
                    ],
                    example={
                        "target_disease": "Type 2 Diabetes",
                        "molecular_structure": "CCO",
                        "screening_criteria": {"max_molecular_weight": 500}
                    }
                ),
                output_schema=OutputSchema(
                    schema_name="DrugDiscoveryResponse",
                    fields=[
                        DataMapping(
                            field_name="candidates",
                            field_type="array",
                            description="Potential drug candidates",
                            source=DataSourceType.TEST,
                            example_value=[],
                            required=True
                        ),
                        DataMapping(
                            field_name="properties",
                            field_type="object",
                            description="Predicted molecular properties",
                            source=DataSourceType.TEST,
                            example_value={},
                            required=True
                        ),
                        DataMapping(
                            field_name="confidence",
                            field_type="float",
                            description="Prediction confidence",
                            source=DataSourceType.TEST,
                            example_value=0.75,
                            required=True
                        )
                    ],
                    example={
                        "candidates": [],
                        "properties": {},
                        "confidence": 0.75
                    },
                    classifications=[
                        Classification(
                            category="Drug Likeness",
                            label="moderate",
                            confidence=0.75,
                            explanation="Moderate drug-likeness score based on molecular properties"
                        )
                    ]
                ),
                pipeline_steps=[
                    PipelineStep(
                        step_id="molecular_parsing",
                        step_name="Molecular Structure Parsing",
                        description="Parse and validate molecular structure",
                        input_type="SMILES",
                        output_type="MolecularGraph",
                        processing_time_ms=10.0
                    ),
                    PipelineStep(
                        step_id="property_prediction",
                        step_name="Property Prediction",
                        description="Predict ADMET properties using GNN",
                        input_type="MolecularGraph",
                        output_type="Properties",
                        model_used="gnn_property_predictor_v2",
                        confidence=0.75,
                        processing_time_ms=300.0
                    ),
                    PipelineStep(
                        step_id="screening",
                        step_name="Virtual Screening",
                        description="Screen against target disease criteria",
                        input_type="Properties",
                        output_type="Candidates",
                        model_used="screening_engine_v1",
                        processing_time_ms=200.0
                    ),
                    PipelineStep(
                        step_id="ranking",
                        step_name="Candidate Ranking",
                        description="Rank candidates by likelihood of success",
                        input_type="Candidates",
                        output_type="RankedCandidates",
                        processing_time_ms=50.0
                    )
                ],
                data_mapping={
                    "target_disease": DataMapping(
                        field_name="target_disease",
                        field_type="string",
                        description="Target disease",
                        source=DataSourceType.ACTUAL,
                        example_value="Type 2 Diabetes",
                        required=True
                    )
                },
                api_endpoint="/api/v1/healthcare/drug-discovery",
                is_dynamic=False,
                keywords=["drug discovery", "molecular analysis", "pharmaceutical", "ADMET", "virtual screening"],
                tips=[
                    "Use validated SMILES notation",
                    "Consider multiple property predictions",
                    "Combine with experimental validation",
                    "Screen large compound libraries for best results"
                ],
                icon="💊"
            ),
            "clinical-trials": UseCaseMetadata(
                use_case_id="clinical-trials",
                display_name="Clinical Trial Optimization",
                short_description="AI-powered patient matching and enrollment forecasting for clinical trials",
                long_description="Machine learning system for matching patients to clinical trials based on eligibility criteria and predicting enrollment rates to optimize trial design.",
                category="Clinical Research",
                theory=UseCaseTheory(
                    overview="Clinical trial optimization uses NLP to parse eligibility criteria, match patients to trials, and predict enrollment rates using historical data and patient demographics.",
                    problem_statement="Clinical trials face challenges with patient recruitment (80% of trials delayed), inefficient matching, and inaccurate enrollment forecasts. This leads to increased costs and delayed drug approvals.",
                    solution_approach="We use NLP to extract eligibility criteria from trial descriptions, semantic matching to find suitable patients, and time series forecasting to predict enrollment rates.",
                    ai_techniques=[
                        "Natural Language Processing (NLP)",
                        "Semantic Matching",
                        "Time Series Forecasting",
                        "Classification",
                        "Recommendation Systems"
                    ],
                    benefits=[
                        "Faster patient recruitment",
                        "Better patient-trial matching",
                        "Accurate enrollment forecasts",
                        "Reduced trial costs",
                        "Faster drug development"
                    ],
                    limitations=[
                        "Requires structured patient data",
                        "Eligibility criteria complexity",
                        "Privacy concerns with patient data",
                        "Regulatory compliance needed",
                        "May not capture all exclusion criteria"
                    ],
                    best_practices=[
                        "Maintain up-to-date patient databases",
                        "Regularly update eligibility parsing",
                        "Validate matches with clinicians",
                        "Consider multi-site coordination",
                        "Ensure HIPAA compliance"
                    ],
                    references=[
                        "AI in Clinical Trial Optimization",
                        "Patient Matching Algorithms",
                        "Enrollment Forecasting in Clinical Trials"
                    ]
                ),
                stats=UseCaseStats(
                    total_executions=0,
                    success_rate=0.0,
                    average_confidence=0.0,
                    average_latency_ms=0.0,
                    data_points_processed=0,
                    model_versions_used=[]
                ),
                input_schema=InputSchema(
                    schema_name="ClinicalTrialsRequest",
                    fields=[
                        DataMapping(
                            field_name="trial_id",
                            field_type="string",
                            description="Clinical trial identifier",
                            source=DataSourceType.ACTUAL,
                            example_value="NCT12345678",
                            required=True
                        ),
                        DataMapping(
                            field_name="eligibility_criteria",
                            field_type="string",
                            description="Trial eligibility criteria text",
                            source=DataSourceType.ACTUAL,
                            example_value="Age 18-65, Type 2 Diabetes, HbA1c > 7%",
                            required=True
                        ),
                        DataMapping(
                            field_name="patient_records",
                            field_type="array",
                            description="Patient records for matching",
                            source=DataSourceType.ACTUAL,
                            example_value=[{"patient_id": "P001", "age": 45, "condition": "Type 2 Diabetes"}],
                            required=False
                        )
                    ],
                    example={
                        "trial_id": "NCT12345678",
                        "eligibility_criteria": "Age 18-65, Type 2 Diabetes",
                        "patient_records": []
                    }
                ),
                output_schema=OutputSchema(
                    schema_name="ClinicalTrialsResponse",
                    fields=[
                        DataMapping(
                            field_name="matches",
                            field_type="array",
                            description="Matched patients",
                            source=DataSourceType.TEST,
                            example_value=[],
                            required=True
                        ),
                        DataMapping(
                            field_name="enrollment_forecast",
                            field_type="integer",
                            description="Predicted enrollment count",
                            source=DataSourceType.TEST,
                            example_value=50,
                            required=True
                        ),
                        DataMapping(
                            field_name="recommendations",
                            field_type="array",
                            description="Trial optimization recommendations",
                            source=DataSourceType.TEST,
                            example_value=[],
                            required=True
                        )
                    ],
                    example={
                        "matches": [],
                        "enrollment_forecast": 50,
                        "recommendations": []
                    },
                    classifications=[
                        Classification(
                            category="Enrollment Forecast",
                            label="moderate",
                            confidence=0.80,
                            explanation="Moderate enrollment forecast based on patient pool and criteria"
                        )
                    ]
                ),
                pipeline_steps=[
                    PipelineStep(
                        step_id="criteria_parsing",
                        step_name="Eligibility Criteria Parsing",
                        description="Parse and extract eligibility criteria using NLP",
                        input_type="CriteriaText",
                        output_type="StructuredCriteria",
                        model_used="nlp_criteria_parser_v1",
                        processing_time_ms=100.0
                    ),
                    PipelineStep(
                        step_id="patient_matching",
                        step_name="Patient Matching",
                        description="Match patients to trial criteria",
                        input_type="StructuredCriteria",
                        output_type="Matches",
                        model_used="matching_engine_v2",
                        processing_time_ms=200.0
                    ),
                    PipelineStep(
                        step_id="enrollment_forecasting",
                        step_name="Enrollment Forecasting",
                        description="Predict enrollment rates using time series models",
                        input_type="Matches",
                        output_type="Forecast",
                        model_used="forecasting_model_v1",
                        confidence=0.80,
                        processing_time_ms=150.0
                    ),
                    PipelineStep(
                        step_id="optimization",
                        step_name="Trial Optimization",
                        description="Generate recommendations for trial optimization",
                        input_type="Forecast",
                        output_type="Recommendations",
                        processing_time_ms=50.0
                    )
                ],
                data_mapping={
                    "trial_id": DataMapping(
                        field_name="trial_id",
                        field_type="string",
                        description="Clinical trial ID",
                        source=DataSourceType.ACTUAL,
                        example_value="NCT12345678",
                        required=True
                    )
                },
                api_endpoint="/api/v1/healthcare/clinical-trials",
                is_dynamic=False,
                keywords=["clinical trials", "patient matching", "enrollment", "NLP", "forecasting"],
                tips=[
                    "Provide detailed eligibility criteria",
                    "Use structured patient data for better matching",
                    "Consider multi-site enrollment",
                    "Regularly update patient databases"
                ],
                icon="📊"
            ),
            "patient-flow": UseCaseMetadata(
                use_case_id="patient-flow",
                display_name="Patient Flow Prediction",
                short_description="AI-powered forecasting of patient admissions and bed requirements",
                long_description="Time series forecasting system to predict patient flow, bed occupancy, and resource needs to optimize hospital operations and reduce wait times.",
                category="Hospital Operations",
                theory=UseCaseTheory(
                    overview="Patient flow prediction uses time series forecasting models (ARIMA, LSTM, Prophet) to predict future patient admissions, discharges, and bed requirements based on historical patterns and external factors.",
                    problem_statement="Hospitals struggle with capacity planning, leading to overcrowding, long wait times, and inefficient resource allocation. Unpredictable patient flow makes it difficult to optimize staffing and bed management.",
                    solution_approach="We use ensemble time series models that combine historical patterns, seasonality, trends, and external factors (weather, events, holidays) to forecast patient flow with high accuracy.",
                    ai_techniques=[
                        "Time Series Forecasting",
                        "LSTM Networks",
                        "ARIMA Models",
                        "Prophet",
                        "Ensemble Methods"
                    ],
                    benefits=[
                        "Improved capacity planning",
                        "Reduced wait times",
                        "Better resource allocation",
                        "Cost optimization",
                        "Improved patient satisfaction"
                    ],
                    limitations=[
                        "Requires historical data",
                        "May not predict rare events",
                        "External factors can be unpredictable",
                        "Model accuracy depends on data quality",
                        "Requires regular retraining"
                    ],
                    best_practices=[
                        "Include external factors (weather, events)",
                        "Regularly retrain models with new data",
                        "Combine multiple forecasting methods",
                        "Monitor and adjust for anomalies",
                        "Integrate with hospital systems"
                    ],
                    references=[
                        "Time Series Forecasting in Healthcare",
                        "Patient Flow Optimization",
                        "Hospital Capacity Planning with AI"
                    ]
                ),
                stats=UseCaseStats(
                    total_executions=0,
                    success_rate=0.0,
                    average_confidence=0.0,
                    average_latency_ms=0.0,
                    data_points_processed=0,
                    model_versions_used=[]
                ),
                input_schema=InputSchema(
                    schema_name="PatientFlowRequest",
                    fields=[
                        DataMapping(
                            field_name="hospital_id",
                            field_type="string",
                            description="Hospital identifier",
                            source=DataSourceType.ACTUAL,
                            example_value="HOSP-001",
                            required=True
                        ),
                        DataMapping(
                            field_name="date_range",
                            field_type="object",
                            description="Forecast date range",
                            source=DataSourceType.ACTUAL,
                            example_value={"start": "2024-01-01", "end": "2024-01-07"},
                            required=True
                        ),
                        DataMapping(
                            field_name="external_factors",
                            field_type="object",
                            description="External factors affecting patient flow",
                            source=DataSourceType.ACTUAL,
                            example_value={"weather": "normal", "holidays": []},
                            required=False
                        )
                    ],
                    example={
                        "hospital_id": "HOSP-001",
                        "date_range": {"start": "2024-01-01", "end": "2024-01-07"},
                        "external_factors": {}
                    }
                ),
                output_schema=OutputSchema(
                    schema_name="PatientFlowResponse",
                    fields=[
                        DataMapping(
                            field_name="predicted_admissions",
                            field_type="array",
                            description="Predicted daily admissions",
                            source=DataSourceType.TEST,
                            example_value=[100, 110, 105],
                            required=True
                        ),
                        DataMapping(
                            field_name="bed_requirements",
                            field_type="array",
                            description="Predicted daily bed requirements",
                            source=DataSourceType.TEST,
                            example_value=[80, 85, 82],
                            required=True
                        ),
                        DataMapping(
                            field_name="recommendations",
                            field_type="array",
                            description="Operational recommendations",
                            source=DataSourceType.TEST,
                            example_value=[],
                            required=True
                        )
                    ],
                    example={
                        "predicted_admissions": [100, 110, 105],
                        "bed_requirements": [80, 85, 82],
                        "recommendations": []
                    },
                    classifications=[
                        Classification(
                            category="Capacity Level",
                            label="normal",
                            confidence=0.85,
                            explanation="Normal capacity levels predicted for the forecast period"
                        )
                    ]
                ),
                pipeline_steps=[
                    PipelineStep(
                        step_id="data_preparation",
                        step_name="Data Preparation",
                        description="Prepare historical patient flow data",
                        input_type="RawData",
                        output_type="TimeSeriesData",
                        processing_time_ms=50.0
                    ),
                    PipelineStep(
                        step_id="feature_engineering",
                        step_name="Feature Engineering",
                        description="Extract temporal features and external factors",
                        input_type="TimeSeriesData",
                        output_type="Features",
                        processing_time_ms=30.0
                    ),
                    PipelineStep(
                        step_id="forecasting",
                        step_name="Time Series Forecasting",
                        description="Generate forecasts using ensemble models",
                        input_type="Features",
                        output_type="Forecasts",
                        model_used="lstm_forecaster_v3",
                        confidence=0.85,
                        processing_time_ms=200.0
                    ),
                    PipelineStep(
                        step_id="capacity_planning",
                        step_name="Capacity Planning",
                        description="Calculate bed and resource requirements",
                        input_type="Forecasts",
                        output_type="CapacityPlan",
                        processing_time_ms=50.0
                    ),
                    PipelineStep(
                        step_id="recommendation_generation",
                        step_name="Recommendation Generation",
                        description="Generate operational recommendations",
                        input_type="CapacityPlan",
                        output_type="Recommendations",
                        processing_time_ms=20.0
                    )
                ],
                data_mapping={
                    "hospital_id": DataMapping(
                        field_name="hospital_id",
                        field_type="string",
                        description="Hospital identifier",
                        source=DataSourceType.ACTUAL,
                        example_value="HOSP-001",
                        required=True
                    )
                },
                api_endpoint="/api/v1/healthcare/patient-flow",
                is_dynamic=False,
                keywords=["patient flow", "forecasting", "capacity planning", "hospital operations", "time series"],
                tips=[
                    "Include historical data for at least 1 year",
                    "Consider external factors (weather, events)",
                    "Regularly update models with new data",
                    "Monitor forecast accuracy and adjust"
                ],
                icon="📈"
            ),
            "resource-allocation": UseCaseMetadata(
                use_case_id="resource-allocation",
                display_name="Resource Allocation AI",
                short_description="AI-powered optimization of hospital resource allocation",
                long_description="Optimization system using linear programming and machine learning to allocate hospital resources (staff, equipment, beds) efficiently based on predicted demand.",
                category="Hospital Operations",
                theory=UseCaseTheory(
                    overview="Resource allocation AI uses optimization algorithms (linear programming, genetic algorithms) combined with demand forecasting to allocate hospital resources efficiently while meeting constraints and maximizing utilization.",
                    problem_statement="Hospitals face challenges with resource allocation - overstaffing increases costs, understaffing affects patient care. Manual allocation is suboptimal and doesn't adapt to changing demand patterns.",
                    solution_approach="We combine demand forecasting with constraint optimization to create optimal resource allocation plans that balance cost, quality of care, and operational efficiency.",
                    ai_techniques=[
                        "Linear Programming",
                        "Genetic Algorithms",
                        "Reinforcement Learning",
                        "Demand Forecasting",
                        "Multi-objective Optimization"
                    ],
                    benefits=[
                        "Optimal resource utilization",
                        "Cost reduction",
                        "Improved patient care",
                        "Better staff satisfaction",
                        "Adaptive to demand changes"
                    ],
                    limitations=[
                        "Requires accurate demand forecasts",
                        "Complex constraint modeling",
                        "May not account for all real-world factors",
                        "Requires integration with hospital systems",
                        "Needs regular optimization updates"
                    ],
                    best_practices=[
                        "Define clear objectives and constraints",
                        "Integrate with real-time demand data",
                        "Consider staff preferences and skills",
                        "Regularly review and adjust allocations",
                        "Balance multiple objectives (cost, quality, satisfaction)"
                    ],
                    references=[
                        "Optimization in Healthcare Resource Allocation",
                        "AI for Hospital Operations",
                        "Multi-objective Optimization in Healthcare"
                    ]
                ),
                stats=UseCaseStats(
                    total_executions=0,
                    success_rate=0.0,
                    average_confidence=0.0,
                    average_latency_ms=0.0,
                    data_points_processed=0,
                    model_versions_used=[]
                ),
                input_schema=InputSchema(
                    schema_name="ResourceAllocationRequest",
                    fields=[
                        DataMapping(
                            field_name="department",
                            field_type="string",
                            description="Hospital department",
                            source=DataSourceType.ACTUAL,
                            example_value="Emergency",
                            required=True
                        ),
                        DataMapping(
                            field_name="current_resources",
                            field_type="object",
                            description="Current resource availability",
                            source=DataSourceType.ACTUAL,
                            example_value={"nurses": 10, "beds": 20, "equipment": 5},
                            required=False
                        ),
                        DataMapping(
                            field_name="predicted_demand",
                            field_type="object",
                            description="Predicted resource demand",
                            source=DataSourceType.ACTUAL,
                            example_value={"nurses": 12, "beds": 25},
                            required=False
                        ),
                        DataMapping(
                            field_name="constraints",
                            field_type="object",
                            description="Allocation constraints",
                            source=DataSourceType.ACTUAL,
                            example_value={"max_shift_hours": 12, "min_staff_ratio": 0.5},
                            required=False
                        )
                    ],
                    example={
                        "department": "Emergency",
                        "current_resources": {},
                        "predicted_demand": {},
                        "constraints": {}
                    }
                ),
                output_schema=OutputSchema(
                    schema_name="ResourceAllocationResponse",
                    fields=[
                        DataMapping(
                            field_name="allocation_plan",
                            field_type="object",
                            description="Optimal resource allocation plan",
                            source=DataSourceType.TEST,
                            example_value={},
                            required=True
                        ),
                        DataMapping(
                            field_name="efficiency_score",
                            field_type="float",
                            description="Allocation efficiency score (0-1)",
                            source=DataSourceType.TEST,
                            example_value=0.85,
                            required=True
                        ),
                        DataMapping(
                            field_name="recommendations",
                            field_type="array",
                            description="Optimization recommendations",
                            source=DataSourceType.TEST,
                            example_value=[],
                            required=True
                        )
                    ],
                    example={
                        "allocation_plan": {},
                        "efficiency_score": 0.85,
                        "recommendations": []
                    },
                    classifications=[
                        Classification(
                            category="Efficiency",
                            label="high",
                            confidence=0.85,
                            explanation="High efficiency score indicates optimal resource allocation"
                        )
                    ]
                ),
                pipeline_steps=[
                    PipelineStep(
                        step_id="demand_analysis",
                        step_name="Demand Analysis",
                        description="Analyze predicted demand patterns",
                        input_type="DemandData",
                        output_type="DemandProfile",
                        processing_time_ms=30.0
                    ),
                    PipelineStep(
                        step_id="constraint_modeling",
                        step_name="Constraint Modeling",
                        description="Model allocation constraints",
                        input_type="Constraints",
                        output_type="ConstraintModel",
                        processing_time_ms=20.0
                    ),
                    PipelineStep(
                        step_id="optimization",
                        step_name="Resource Optimization",
                        description="Solve optimization problem",
                        input_type="OptimizationProblem",
                        output_type="AllocationPlan",
                        model_used="optimizer_v2",
                        confidence=0.85,
                        processing_time_ms=300.0
                    ),
                    PipelineStep(
                        step_id="efficiency_calculation",
                        step_name="Efficiency Calculation",
                        description="Calculate allocation efficiency",
                        input_type="AllocationPlan",
                        output_type="EfficiencyScore",
                        processing_time_ms=10.0
                    ),
                    PipelineStep(
                        step_id="recommendation_generation",
                        step_name="Recommendation Generation",
                        description="Generate optimization recommendations",
                        input_type="EfficiencyScore",
                        output_type="Recommendations",
                        processing_time_ms=20.0
                    )
                ],
                data_mapping={
                    "department": DataMapping(
                        field_name="department",
                        field_type="string",
                        description="Hospital department",
                        source=DataSourceType.ACTUAL,
                        example_value="Emergency",
                        required=True
                    )
                },
                api_endpoint="/api/v1/healthcare/resource-allocation",
                is_dynamic=False,
                keywords=["resource allocation", "optimization", "hospital operations", "staffing", "capacity"],
                tips=[
                    "Define clear objectives and constraints",
                    "Use accurate demand forecasts",
                    "Consider staff preferences",
                    "Regularly review and adjust",
                    "Balance multiple objectives"
                ],
                icon="⚖️"
            )
        }
