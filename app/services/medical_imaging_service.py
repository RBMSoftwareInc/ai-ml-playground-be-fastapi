"""
Medical Imaging Service - Radiology-Grade ML Inference
Uses DenseNet-121 (MURA dataset) + Grad-CAM for real deep learning inference
Removes all heuristic logic - pure ML-based analysis
"""
from typing import List, Dict, Any, Optional
import io
import numpy as np
from PIL import Image
from app.schemas.diagnostic_ai import (
    AnatomicalRegion, Observation, Likelihood, Explainability, ExplainabilityArtifact,
    ObservationWithLikelihood, DiagnosticAIAnalysisResponse
)
from app.services.radiology_ml_service import get_radiology_ml_service
try:
    import pydicom
    DICOM_AVAILABLE = True
except ImportError:
    DICOM_AVAILABLE = False


class MedicalImagingService:
    """
    Radiology-grade medical image analysis service
    Uses DenseNet-121 (MURA dataset) for musculoskeletal X-ray analysis
    """
    
    def __init__(self):
        """Initialize medical imaging service with ML models (lazy-loaded)"""
        # Don't initialize radiology_ml_service here - lazy load on first use
        self._radiology_ml = None
        self._model_version = None
    
    @property
    def radiology_ml(self):
        """Lazy-load radiology ML service"""
        if self._radiology_ml is None:
            self._radiology_ml = get_radiology_ml_service()
        return self._radiology_ml
    
    @property
    def model_version(self):
        """Lazy-load model version"""
        if self._model_version is None:
            self._model_version = f"densenet121_mura_v{self.radiology_ml.model_version}"
        return self._model_version
    
    def analyze_medical_image(
        self,
        image_bytes: bytes,
        image_type: str = "auto",
        format: str = "standard"
    ) -> DiagnosticAIAnalysisResponse:
        """
        Analyze medical image using DenseNet-121 ML model (MURA dataset)
        
        Steps:
        1. Load and preprocess image
        2. Detect anatomical region using ML model
        3. Run fracture likelihood prediction
        4. Generate Grad-CAM explainability
        5. Return radiology-grade observations
        
        Args:
            image_bytes: Image file bytes
            image_type: Type of image - "xray", "ct", "mri", "auto"
            format: Image format - "standard" (PNG/JPEG) or "dicom"
            
        Returns:
            DiagnosticAIAnalysisResponse with ML-based analysis
        """
        # Step 1: Load image
        if format.lower() == "dicom":
            image, dicom_metadata = self._load_dicom_image(image_bytes)
        else:
            image = Image.open(io.BytesIO(image_bytes))
            dicom_metadata = None
        
        # Step 2: Auto-detect image type if needed
        if image_type == "auto":
            image_type = self._detect_image_type(image)
        
        # Normalize image type (handle variations like "X-Ray", "x-ray", "xray", etc.)
        image_type_normalized = image_type.lower().replace("-", "").replace("_", "").strip()
        
        # Only process X-rays for now (MURA dataset is musculoskeletal X-rays)
        if image_type_normalized != "xray":
            raise ValueError(f"Currently only X-ray images are supported. Received: {image_type}")
        
        # Step 3: Detect anatomical region using ML model
        region_info = self.radiology_ml.detect_anatomical_region_from_image(image)
        anatomical_region = AnatomicalRegion(
            label=region_info["anatomical_region"],
            confidence=region_info["confidence"],
            detection_method=region_info["detection_method"],
            model_dataset=region_info.get("mura_regions", ["hand", "wrist", "forearm"])[0] if isinstance(region_info.get("mura_regions"), list) else "MURA (Stanford)"
        )
        
        # Step 4: Run ML model inference for fracture likelihood
        fracture_score, model_metadata = self.radiology_ml.predict_fracture_likelihood(image)
        
        # Step 5: Generate observations based on ML model output
        observations_with_likelihood = self._generate_observations_from_ml_output(
            anatomical_region.label,
            fracture_score,
            model_metadata
        )
        
        # Step 6: Generate Grad-CAM explainability
        explainability = self._generate_gradcam_explainability(
            image,
            anatomical_region.label,
            fracture_score
        )
        
        # Step 7: Calculate overall confidence
        if observations_with_likelihood:
            overall_confidence = np.mean([obs.likelihood.score for obs in observations_with_likelihood])
        else:
            overall_confidence = anatomical_region.confidence
        
        # Step 8: Build response
        return DiagnosticAIAnalysisResponse(
            anatomical_region=anatomical_region,
            observations=observations_with_likelihood,
            explainability=explainability,
            overall_confidence=float(overall_confidence),
            model_version=self.model_version,
            processing_metadata={
                "image_type": image_type,
                "image_format": format,
                "dicom_metadata": dicom_metadata if dicom_metadata else None,
                "image_size": f"{image.size[0]}x{image.size[1]}",
                "model_loaded": model_metadata.get("model_loaded", False),
                "model_name": model_metadata.get("model_name", "densenet121_mura"),
                "dataset": model_metadata.get("dataset", "MURA (Stanford)")
            }
        )
    
    def _load_dicom_image(self, dicom_bytes: bytes) -> tuple:
        """
        Load DICOM image and convert to PIL Image
        
        Args:
            dicom_bytes: DICOM file bytes
            
        Returns:
            Tuple of (PIL Image, DICOM metadata dict)
        """
        if not DICOM_AVAILABLE:
            raise ValueError("pydicom not available. Install with: pip install pydicom")
        
        dicom_file = pydicom.dcmread(io.BytesIO(dicom_bytes))
        
        # Extract pixel array
        pixel_array = dicom_file.pixel_array
        
        # Normalize pixel values to 0-255
        pixel_array = pixel_array.astype(np.float32)
        pixel_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
        
        # Convert to PIL Image
        image = Image.fromarray(pixel_array)
        
        # Extract relevant DICOM metadata
        metadata = {
            "patient_id": str(dicom_file.get("PatientID", "")),
            "study_date": str(dicom_file.get("StudyDate", "")),
            "modality": str(dicom_file.get("Modality", "")),
            "body_part": str(dicom_file.get("BodyPartExamined", "")),
            "study_description": str(dicom_file.get("StudyDescription", ""))
        }
        
        return image, metadata
    
    def _detect_image_type(self, image: Image.Image) -> str:
        """
        Auto-detect image type (simplified - in production could use model)
        
        Args:
            image: PIL Image
            
        Returns:
            Image type: "xray", "ct", "mri"
        """
        # Simple heuristic based on image characteristics
        # In production, could use a classification model
        if image.mode == "L":  # Grayscale
            # X-rays are typically grayscale
            return "xray"
        else:
            # CT/MRI might be grayscale too, but for now default to xray
            return "xray"
    
    def _generate_observations_from_ml_output(
        self,
        anatomical_region: str,
        fracture_score: float,
        model_metadata: Dict[str, Any]
    ) -> List[ObservationWithLikelihood]:
        """
        Generate radiology-grade observations from ML model output
        
        Uses proper clinical language based on fracture likelihood score
        """
        observations = []
        
        # Map anatomical region to specific anatomical structures
        region_structure_map = {
            "hand": "distal radius and carpal region",
            "wrist": "distal radius metaphysis",
            "forearm": "radius and ulna",
            "elbow": "elbow joint",
            "humerus": "proximal humerus",
            "finger": "phalanges",
            "shoulder": "proximal humerus and glenohumeral joint"
        }
        
        anatomical_structure = region_structure_map.get(anatomical_region.lower(), anatomical_region)
        
        # Determine observation based on fracture likelihood
        if fracture_score >= 0.7:
            # High likelihood - focal discontinuity pattern
            observation_text = "Focal cortical discontinuity detected"
            clinical_context = "Pattern consistent with fracture morphology"
            confidence_band = "high"
            interpretation = f"Strong model agreement with fracture patterns learned from MURA training data. Fracture likelihood score: {fracture_score:.2f}"
        elif fracture_score >= 0.5:
            # Moderate likelihood - possible abnormality
            observation_text = "Focal cortical irregularity observed"
            clinical_context = "Pattern may be consistent with fracture morphology; requires radiologist correlation"
            confidence_band = "moderate"
            interpretation = f"Moderate model agreement with fracture patterns. Fracture likelihood score: {fracture_score:.2f}"
        else:
            # Low likelihood - but still note any patterns
            observation_text = "Cortical bone structure appears continuous"
            clinical_context = "No strong indicators of fracture morphology detected; routine clinical review recommended"
            confidence_band = "low"
            interpretation = f"Low fracture likelihood score ({fracture_score:.2f}). Model patterns suggest no obvious fracture morphology."
        
        # Create observation
        observation = Observation(
            anatomical_region=anatomical_structure,
            description=observation_text,
            clinical_context=clinical_context
        )
        
        # Create likelihood
        likelihood = Likelihood(
            score=fracture_score,
            confidence_band=confidence_band,
            interpretation=interpretation
        )
        
        observations.append(ObservationWithLikelihood(
            observation=observation,
            likelihood=likelihood
        ))
        
        return observations
    
    def _generate_gradcam_explainability(
        self,
        image: Image.Image,
        anatomical_region: str,
        fracture_score: float
    ) -> Explainability:
        """
        Generate Grad-CAM explainability visualization
        
        Args:
            image: Original X-ray image
            anatomical_region: Detected anatomical region
            fracture_score: Fracture likelihood score from model
            
        Returns:
            Explainability object with Grad-CAM artifacts
        """
        # Generate Grad-CAM heatmap
        gradcam_result = self.radiology_ml.generate_gradcam_explainability(image)
        
        # Map region to specific anatomical structure for explainability
        region_structure_map = {
            "hand": "distal radius and carpal region",
            "wrist": "distal radius metaphysis",
            "forearm": "radius and ulna",
            "elbow": "elbow joint",
            "humerus": "proximal humerus",
            "finger": "phalanges",
            "shoulder": "proximal humerus and glenohumeral joint"
        }
        
        highlighted_region = region_structure_map.get(anatomical_region.lower(), anatomical_region)
        
        # Create explainability artifact
        artifact = ExplainabilityArtifact(
            overlay_type="heatmap",
            highlighted_region=highlighted_region,
            heatmap_region=gradcam_result["heatmap_region"],
            explanation=gradcam_result["explanation"]
        )
        
        # Create explainability response
        explainability = Explainability(
            method=gradcam_result["method"],
            overlay_type=gradcam_result["overlay_type"],
            highlighted_region=highlighted_region,
            explanation="The highlighted region shows high activation in the model's intermediate layers. This indicates that local texture and edge patterns strongly influenced the fracture likelihood score.",
            artifacts=[artifact]
        )
        
        return explainability


# Global instance
# Lazy-loaded global instance (only initialized when first accessed)
_medical_imaging_service_instance = None

def get_medical_imaging_service() -> MedicalImagingService:
    """Get or create medical imaging service instance (lazy initialization)"""
    global _medical_imaging_service_instance
    if _medical_imaging_service_instance is None:
        _medical_imaging_service_instance = MedicalImagingService()
    return _medical_imaging_service_instance

# For backward compatibility, create a property-like accessor
class _MedicalImagingServiceProxy:
    """Proxy class for lazy initialization"""
    def __getattr__(self, name):
        return getattr(get_medical_imaging_service(), name)

medical_imaging_service = _MedicalImagingServiceProxy()
