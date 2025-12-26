"""
Seed script to populate workflow comparison data for Diagnostic AI use case
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.intelligence import WorkflowComparison
from sqlalchemy.exc import IntegrityError


def seed_diagnostic_ai_workflow_comparison():
    """Seed workflow comparison for healthcare/diagnostic-ai"""
    db = SessionLocal()
    
    try:
        # Check if already exists
        existing = db.query(WorkflowComparison).filter(
            WorkflowComparison.industry_id == "healthcare",
            WorkflowComparison.use_case_id == "diagnostic-ai",
            WorkflowComparison.is_active == True
        ).first()
        
        if existing:
            print("✓ Workflow comparison for healthcare/diagnostic-ai already exists")
            return existing
        
        # Create workflow comparison
        comparison = WorkflowComparison(
            comparison_key="healthcare_diagnostic_ai_workflow",
            industry_id="healthcare",
            use_case_id="diagnostic-ai",
            conventional_steps=[
                {
                    "step_name": "Image Capture",
                    "description": "Medical image captured (X-ray, CT, MRI) using imaging equipment",
                    "time_hours": 0.083,  # 5 minutes
                    "error_probability": 0.02,
                    "human_dependencies": ["Radiologic technologist", "Patient positioning"]
                },
                {
                    "step_name": "Image Queueing",
                    "description": "Image added to radiologist reading queue with priority assignment",
                    "time_hours": 0.083,  # 5 minutes (can be longer during peak hours)
                    "error_probability": 0.05,
                    "human_dependencies": ["Radiology scheduler", "Priority assignment"]
                },
                {
                    "step_name": "Manual Visual Inspection",
                    "description": "Radiologist performs initial visual inspection of image, compares with anatomical knowledge",
                    "time_hours": 0.25,  # 15 minutes per study
                    "error_probability": 0.10,  # Fatigue and cognitive load increase error probability
                    "human_dependencies": ["Board-certified radiologist", "Clinical knowledge", "Prior case memory"]
                },
                {
                    "step_name": "Prior Comparison",
                    "description": "Manual search and comparison with prior imaging studies (if available)",
                    "time_hours": 0.17,  # 10 minutes
                    "error_probability": 0.08,
                    "human_dependencies": ["PACS system access", "Memory-based comparison"]
                },
                {
                    "step_name": "Pattern Recognition",
                    "description": "Radiologist identifies patterns, abnormalities, and areas of concern using visual analysis",
                    "time_hours": 0.33,  # 20 minutes (varies by complexity)
                    "error_probability": 0.12,  # Higher under fatigue
                    "human_dependencies": ["Experience", "Cognitive load management"]
                },
                {
                    "step_name": "Dictation & Reporting",
                    "description": "Radiologist dictates findings, creates structured report with recommendations",
                    "time_hours": 0.25,  # 15 minutes
                    "error_probability": 0.05,
                    "human_dependencies": ["Dictation system", "Report template"]
                },
                {
                    "step_name": "Report Review & Sign-off",
                    "description": "Final review of report for accuracy, completeness, and clinical appropriateness",
                    "time_hours": 0.17,  # 10 minutes
                    "error_probability": 0.03,
                    "human_dependencies": ["Quality check", "Clinical validation"]
                }
            ],
            ai_driven_steps=[
                {
                    "step_name": "Image Ingestion",
                    "description": "Medical image automatically ingested into AI system (DICOM or standard format)",
                    "time_seconds": 2.0,
                    "confidence_score": 0.98,
                    "learning_loop": False
                },
                {
                    "step_name": "Anatomical Region Detection",
                    "description": "AI automatically detects anatomical region using segmentation-based bone structure analysis",
                    "time_seconds": 0.5,
                    "confidence_score": 0.94,
                    "learning_loop": True
                },
                {
                    "step_name": "Pattern Analysis",
                    "description": "AI models analyze image patterns, compare against learned anatomical structures",
                    "time_seconds": 3.0,
                    "confidence_score": 0.91,
                    "learning_loop": True
                },
                {
                    "step_name": "Observation Generation",
                    "description": "AI generates structured observations (not diagnoses) with likelihood assessments",
                    "time_seconds": 1.5,
                    "confidence_score": 0.88,
                    "learning_loop": True
                },
                {
                    "step_name": "Explainability Generation",
                    "description": "AI generates visual artifacts (heatmaps, bone outlines) mapped to detected structures",
                    "time_seconds": 2.0,
                    "confidence_score": 0.92,
                    "learning_loop": False
                },
                {
                    "step_name": "Radiologist Review with Context",
                    "description": "Radiologist reviews AI-generated observations and explainability artifacts, makes final assessment",
                    "time_seconds": 180.0,  # 3 minutes (reduced from 15 minutes)
                    "confidence_score": 0.95,
                    "learning_loop": True
                },
                {
                    "step_name": "Report Finalization",
                    "description": "Radiologist finalizes report incorporating AI insights, adds clinical context",
                    "time_seconds": 300.0,  # 5 minutes (reduced from 15 minutes)
                    "confidence_score": 0.96,
                    "learning_loop": False
                }
            ],
            time_reduction_percent=85.0,  # ~85% reduction (1.33 hours → ~10 minutes total)
            error_reduction_percent=65.0,  # Significant reduction due to consistent pattern recognition
            human_intervention_points={
                "before": [
                    "Every step requires human action",
                    "Manual pattern recognition",
                    "Memory-based prior comparison",
                    "Full visual inspection burden"
                ],
                "after": [
                    "Radiologist reviews AI pre-analysis",
                    "Radiologist validates AI observations",
                    "Radiologist adds clinical context",
                    "Final decision remains with radiologist"
                ],
                "key_improvements": [
                    "AI handles time-consuming pattern analysis",
                    "AI provides consistent observations",
                    "AI highlights areas of interest",
                    "Reduced cognitive fatigue"
                ]
            },
            timeline_animation_config={
                "duration_ms": 8000,
                "steps_per_second": 1.5,
                "highlight_conventional": True,
                "highlight_ai": True,
                "show_time_comparison": True
            },
            is_active=True
        )
        
        db.add(comparison)
        db.commit()
        db.refresh(comparison)
        
        print(f"✓ Created workflow comparison for healthcare/diagnostic-ai (ID: {comparison.id})")
        return comparison
        
    except IntegrityError as e:
        db.rollback()
        print(f"✗ Integrity error: {e}")
        raise
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding workflow comparison: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding workflow comparison data for Diagnostic AI...")
    seed_diagnostic_ai_workflow_comparison()
    print("✓ Seeding complete!")

