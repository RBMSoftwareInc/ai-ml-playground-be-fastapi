"""
Diagnostic AI Schemas - Radiology-Grade ML Contracts
Real deep learning inference using DenseNet-121 (MURA dataset) + Grad-CAM explainability
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


class AnatomicalRegion(BaseModel):
    """Anatomical region detection from ML model (MURA dataset regions)"""
    label: str = Field(..., description="Detected anatomical region from MURA: 'hand', 'wrist', 'forearm', 'elbow', 'humerus', 'finger', 'shoulder'")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence for anatomical region detection")
    detection_method: str = Field(..., description="Detection method: 'densenet121_mura' or 'placeholder' if model not loaded")
    model_dataset: str = Field(default="MURA (Stanford)", description="Dataset used for training")


class Observation(BaseModel):
    """Radiology-grade observation (NOT a diagnosis) - Based on ML model inference"""
    anatomical_region: str = Field(..., description="Specific anatomical region (e.g., 'distal radius', 'carpal bones')")
    description: str = Field(..., description="Clinical description of observed pattern (e.g., 'Focal cortical discontinuity detected')")
    clinical_context: str = Field(..., description="Clinical context statement (e.g., 'Pattern consistent with fracture morphology')")


class Likelihood(BaseModel):
    """Probabilistic likelihood from ML model (NOT absolute certainty)"""
    score: float = Field(..., ge=0.0, le=1.0, description="Fracture likelihood score from DenseNet-121 model")
    confidence_band: Literal["low", "moderate", "high"] = Field(..., description="Confidence band based on model certainty")
    interpretation: str = Field(..., description="Interpretation of likelihood (e.g., 'Strong model agreement with fracture patterns learned from training data')")


class ExplainabilityArtifact(BaseModel):
    """Grad-CAM explainability artifact - Real localized heatmap"""
    overlay_type: Literal["heatmap"] = Field(..., description="Type of overlay: 'heatmap' (Grad-CAM)")
    highlighted_region: str = Field(..., description="Anatomical region highlighted (e.g., 'distal radius metaphysis')")
    heatmap_region: Dict[str, float] = Field(..., description="Normalized coordinates [x, y, width, height] for heatmap region")
    explanation: str = Field(..., description="Explanation of why this region was flagged (e.g., 'This region contributed most strongly to the model's prediction')")


class Explainability(BaseModel):
    """Grad-CAM explainability - Real visual localization of model attention"""
    method: str = Field(default="Grad-CAM", description="Explainability method: 'Grad-CAM' or 'Grad-CAM++'")
    overlay_type: str = Field(default="heatmap", description="Type of visual overlay")
    highlighted_region: str = Field(..., description="Primary anatomical region highlighted by Grad-CAM")
    explanation: str = Field(..., description="Explanation of Grad-CAM visualization (e.g., 'The highlighted region shows high activation in the model's intermediate layers')")
    artifacts: List[ExplainabilityArtifact] = Field(default_factory=list, description="Grad-CAM artifacts")


class ObservationWithLikelihood(BaseModel):
    """Observation combined with likelihood assessment"""
    observation: Observation
    likelihood: Likelihood


class DiagnosticAIAnalysisResponse(BaseModel):
    """Complete diagnostic AI analysis response"""
    anatomical_region: AnatomicalRegion
    observations: List[ObservationWithLikelihood] = Field(default_factory=list)
    explainability: Explainability
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence in analysis")
    model_version: str = Field(..., description="Model version used")
    processing_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional processing metadata")

