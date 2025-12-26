"""
Medical Document Processing Service
Handles PDF health reports, OCR, text extraction, and structured data extraction
"""
from typing import List, Dict, Any, Optional
import io
import re
from datetime import datetime
import PyPDF2
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import numpy as np
from app.services.nlp_service import nlp_service


class MedicalDocumentService:
    """Service for processing medical documents and health reports"""
    
    def __init__(self):
        """Initialize medical document processing"""
        self.nlp = nlp_service
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Extract text from PDF document
        
        Args:
            pdf_bytes: PDF file bytes
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Try text extraction first
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text_content = []
            metadata = {}
            
            # Extract metadata
            if pdf_reader.metadata:
                metadata = {
                    "title": pdf_reader.metadata.get("/Title", ""),
                    "author": pdf_reader.metadata.get("/Author", ""),
                    "creator": pdf_reader.metadata.get("/Creator", ""),
                    "creation_date": str(pdf_reader.metadata.get("/CreationDate", ""))
                }
            
            # Extract text from each page
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text_content.append({
                        "page": page_num + 1,
                        "text": page_text
                    })
            
            # If no text found, try OCR
            if not text_content:
                return self._extract_with_ocr(pdf_bytes)
            
            full_text = "\n\n".join([page["text"] for page in text_content])
            
            return {
                "success": True,
                "text": full_text,
                "pages": text_content,
                "metadata": metadata,
                "extraction_method": "text_extraction",
                "total_pages": len(pdf_reader.pages)
            }
            
        except Exception as e:
            # Fallback to OCR if PDF text extraction fails
            return self._extract_with_ocr(pdf_bytes)
    
    def _extract_with_ocr(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Extract text using OCR (for scanned documents)
        
        Args:
            pdf_bytes: PDF file bytes
            
        Returns:
            Dictionary with OCR extracted text
        """
        try:
            # Convert PDF pages to images
            images = convert_from_bytes(pdf_bytes, dpi=300)
            text_content = []
            
            for page_num, image in enumerate(images):
                # Perform OCR
                page_text = pytesseract.image_to_string(image, lang='eng')
                if page_text.strip():
                    text_content.append({
                        "page": page_num + 1,
                        "text": page_text
                    })
            
            full_text = "\n\n".join([page["text"] for page in text_content])
            
            return {
                "success": True,
                "text": full_text,
                "pages": text_content,
                "metadata": {},
                "extraction_method": "ocr",
                "total_pages": len(images)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "pages": [],
                "metadata": {},
                "extraction_method": "ocr",
                "total_pages": 0
            }
    
    def extract_health_metrics(self, text: str) -> Dict[str, Any]:
        """
        Extract health metrics and test results from text
        
        Args:
            text: Extracted text from health report
            
        Returns:
            Dictionary with extracted health metrics
        """
        metrics = {
            "vitals": {},
            "lab_results": [],
            "medications": [],
            "diagnoses": [],
            "recommendations": []
        }
        
        # Extract blood pressure
        bp_pattern = r'blood\s*pressure|BP|bp[:\s]+(\d+)\s*[/-]\s*(\d+)'
        bp_match = re.search(bp_pattern, text, re.IGNORECASE)
        if bp_match:
            metrics["vitals"]["blood_pressure"] = {
                "systolic": int(bp_match.group(1)),
                "diastolic": int(bp_match.group(2))
            }
        
        # Extract heart rate
        hr_pattern = r'heart\s*rate|HR|pulse[:\s]+(\d+)'
        hr_match = re.search(hr_pattern, text, re.IGNORECASE)
        if hr_match:
            metrics["vitals"]["heart_rate"] = int(hr_match.group(1))
        
        # Extract temperature
        temp_pattern = r'temperature|temp[:\s]+(\d+\.?\d*)\s*[°FfCc]'
        temp_match = re.search(temp_pattern, text, re.IGNORECASE)
        if temp_match:
            metrics["vitals"]["temperature"] = float(temp_match.group(1))
        
        # Extract lab results (common patterns)
        lab_patterns = [
            (r'glucose|blood\s*sugar[:\s]+(\d+\.?\d*)', "glucose"),
            (r'cholesterol[:\s]+(\d+\.?\d*)', "cholesterol"),
            (r'hemoglobin|Hb[:\s]+(\d+\.?\d*)', "hemoglobin"),
            (r'creatinine[:\s]+(\d+\.?\d*)', "creatinine"),
            (r'ALT|SGPT[:\s]+(\d+\.?\d*)', "alt"),
            (r'AST|SGOT[:\s]+(\d+\.?\d*)', "ast"),
        ]
        
        for pattern, test_name in lab_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                metrics["lab_results"].append({
                    "test": test_name,
                    "value": float(match.group(1)),
                    "unit": self._infer_unit(test_name, match.group(1))
                })
        
        # Extract medications (look for common medication patterns)
        med_pattern = r'(?:medication|prescription|drug)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        med_matches = re.finditer(med_pattern, text, re.IGNORECASE)
        for match in med_matches:
            med_name = match.group(1).strip()
            if med_name not in metrics["medications"]:
                metrics["medications"].append(med_name)
        
        # Extract diagnoses using NLP
        entities = self.nlp.extract_entities(text)
        for entity in entities:
            if entity["label"] in ["DISEASE", "CONDITION"]:
                if entity["text"] not in metrics["diagnoses"]:
                    metrics["diagnoses"].append(entity["text"])
        
        return metrics
    
    def _infer_unit(self, test_name: str, value: str) -> str:
        """Infer unit for lab test based on test name and value"""
        unit_map = {
            "glucose": "mg/dL",
            "cholesterol": "mg/dL",
            "hemoglobin": "g/dL",
            "creatinine": "mg/dL",
            "alt": "U/L",
            "ast": "U/L"
        }
        return unit_map.get(test_name.lower(), "")
    
    def analyze_health_report(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Complete analysis of health checkup report PDF
        
        Args:
            pdf_bytes: PDF file bytes
            
        Returns:
            Comprehensive analysis including extracted data, risk assessment, and recommendations
        """
        # Step 1: Extract text
        extraction_result = self.extract_text_from_pdf(pdf_bytes)
        
        if not extraction_result["success"]:
            return {
                "success": False,
                "error": extraction_result.get("error", "Failed to extract text"),
                "analysis": {}
            }
        
        text = extraction_result["text"]
        
        # Step 2: Extract health metrics
        metrics = self.extract_health_metrics(text)
        
        # Step 3: Perform risk assessment
        risk_assessment = self._assess_health_risks(metrics)
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(metrics, risk_assessment)
        
        # Step 5: Extract key findings using NLP
        key_findings = self._extract_key_findings(text)
        
        return {
            "success": True,
            "analysis": {
                "extracted_text": {
                    "total_pages": extraction_result["total_pages"],
                    "extraction_method": extraction_result["extraction_method"],
                    "preview": text[:500] + "..." if len(text) > 500 else text
                },
                "health_metrics": metrics,
                "risk_assessment": risk_assessment,
                "key_findings": key_findings,
                "recommendations": recommendations,
                "summary": self._generate_summary(metrics, risk_assessment)
            }
        }
    
    def _assess_health_risks(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess health risks based on extracted metrics"""
        risk_score = 0.0
        risk_factors = []
        
        # Check blood pressure
        if "blood_pressure" in metrics.get("vitals", {}):
            bp = metrics["vitals"]["blood_pressure"]
            if bp["systolic"] > 140 or bp["diastolic"] > 90:
                risk_score += 0.3
                risk_factors.append("High blood pressure detected")
        
        # Check heart rate
        if "heart_rate" in metrics.get("vitals", {}):
            hr = metrics["vitals"]["heart_rate"]
            if hr > 100 or hr < 60:
                risk_score += 0.2
                risk_factors.append(f"Abnormal heart rate: {hr} bpm")
        
        # Check lab results
        for lab in metrics.get("lab_results", []):
            test_name = lab["test"].lower()
            value = lab["value"]
            
            if test_name == "glucose" and value > 100:
                risk_score += 0.2
                risk_factors.append(f"Elevated glucose: {value} mg/dL")
            elif test_name == "cholesterol" and value > 200:
                risk_score += 0.2
                risk_factors.append(f"High cholesterol: {value} mg/dL")
        
        # Determine risk level
        if risk_score >= 0.6:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_score": min(1.0, risk_score),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "assessment_date": datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, metrics: Dict[str, Any], risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate health recommendations based on analysis"""
        recommendations = []
        
        if risk_assessment["risk_level"] == "high":
            recommendations.append("Consult with a healthcare provider immediately")
            recommendations.append("Consider lifestyle modifications")
        
        if "blood_pressure" in metrics.get("vitals", {}):
            bp = metrics["vitals"]["blood_pressure"]
            if bp["systolic"] > 140:
                recommendations.append("Monitor blood pressure regularly")
                recommendations.append("Consider reducing sodium intake")
        
        if len(metrics.get("lab_results", [])) > 0:
            recommendations.append("Follow up on abnormal lab results")
        
        if len(metrics.get("medications", [])) > 0:
            recommendations.append("Review medications with your doctor")
        
        if not recommendations:
            recommendations.append("Continue regular health checkups")
            recommendations.append("Maintain a healthy lifestyle")
        
        return recommendations
    
    def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from report text using NLP"""
        # Use NLP to identify important sentences
        sentences = text.split('.')
        key_findings = []
        
        # Look for sentences with medical keywords
        medical_keywords = [
            "abnormal", "elevated", "high", "low", "normal", "diagnosis",
            "finding", "result", "condition", "disease", "recommendation"
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in medical_keywords):
                if len(sentence.strip()) > 20:  # Filter very short sentences
                    key_findings.append(sentence.strip())
        
        return key_findings[:10]  # Return top 10 findings
    
    def _generate_summary(self, metrics: Dict[str, Any], risk_assessment: Dict[str, Any]) -> str:
        """Generate a summary of the health report analysis"""
        summary_parts = []
        
        summary_parts.append(f"Health Risk Level: {risk_assessment['risk_level'].upper()}")
        summary_parts.append(f"Risk Score: {risk_assessment['risk_score']:.2f}")
        
        if metrics.get("vitals"):
            summary_parts.append(f"Vitals extracted: {len(metrics['vitals'])} measurements")
        
        if metrics.get("lab_results"):
            summary_parts.append(f"Lab results: {len(metrics['lab_results'])} tests")
        
        if metrics.get("diagnoses"):
            summary_parts.append(f"Diagnoses identified: {len(metrics['diagnoses'])}")
        
        return ". ".join(summary_parts)


medical_document_service = MedicalDocumentService()

