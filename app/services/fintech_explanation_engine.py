"""
Fintech Explanation Engine
Generates mandatory explanation objects for all API responses
"""
from typing import Dict, List, Any, Optional
from app.schemas.fintech import (
    ExplanationObject, ContributingFactor, SensitivityAnalysis, ScenarioImpact,
    InfluencingFactor, ConfidenceAssessment, HumanReviewGuidance
)
from datetime import datetime


class FintechExplanationEngine:
    """
    Explanation engine for Fintech APIs
    Generates explainable, human-readable reasoning for all decisions
    """
    
    def __init__(self):
        """Initialize explanation engine"""
        pass
    
    def generate_credit_risk_explanation(
        self,
        risk_score: float,
        default_probability: float,
        borrower_features: Dict[str, Any],
        scenario_params: Dict[str, Any],
        model_metadata: Dict[str, Any]
    ) -> ExplanationObject:
        """Generate explanation for credit risk assessment"""
        
        # Decision summary
        if risk_score >= 0.8:
            risk_level = "low"
            decision_summary = "Low credit risk. Borrower demonstrates strong financial stability and repayment capacity."
        elif risk_score >= 0.6:
            risk_level = "medium"
            decision_summary = "Medium credit risk. Borrower shows acceptable creditworthiness with some areas of concern."
        elif risk_score >= 0.4:
            risk_level = "high"
            decision_summary = "High credit risk. Borrower exhibits significant risk factors requiring careful evaluation."
        else:
            risk_level = "very_high"
            decision_summary = "Very high credit risk. Borrower presents substantial default risk."
        
        # Confidence score
        confidence_score = 0.85
        if default_probability < 0.1 or default_probability > 0.5:
            confidence_score = 0.90  # More confident at extremes
        elif scenario_params.get("confidence_degradation", 0) > 0:
            confidence_score -= scenario_params["confidence_degradation"]
        
        # Top contributing factors
        contributing_factors = []
        
        # Credit score band
        credit_score_band = borrower_features.get("credit_score_band", "fair")
        if credit_score_band in ["excellent", "good"]:
            contributing_factors.append(ContributingFactor(
                factor_name="Credit History Quality",
                impact_score=0.25,
                direction="decreases",
                explanation=f"Strong credit history ({credit_score_band}) significantly reduces default risk"
            ))
        elif credit_score_band == "poor":
            contributing_factors.append(ContributingFactor(
                factor_name="Credit History Quality",
                impact_score=0.30,
                direction="increases",
                explanation=f"Poor credit history significantly increases default risk"
            ))
        
        # Debt-to-income ratio
        dti = borrower_features.get("debt_to_income_ratio", 0.3)
        if dti > 0.4:
            contributing_factors.append(ContributingFactor(
                factor_name="Debt-to-Income Ratio",
                impact_score=0.20,
                direction="increases",
                explanation=f"High debt-to-income ratio ({dti:.1%}) indicates financial stress"
            ))
        elif dti < 0.25:
            contributing_factors.append(ContributingFactor(
                factor_name="Debt-to-Income Ratio",
                impact_score=0.15,
                direction="decreases",
                explanation=f"Low debt-to-income ratio ({dti:.1%}) indicates strong financial capacity"
            ))
        
        # Employment stability
        emp_stability = borrower_features.get("employment_stability_score", 0.5)
        if emp_stability < 0.4:
            contributing_factors.append(ContributingFactor(
                factor_name="Employment Stability",
                impact_score=0.18,
                direction="increases",
                explanation=f"Low employment stability ({emp_stability:.1%}) increases income uncertainty"
            ))
        
        # Economic context
        economic_stress = scenario_params.get("macro_context", {}).get("economic_stress_level", 0.2)
        if economic_stress > 0.5:
            contributing_factors.append(ContributingFactor(
                factor_name="Economic Environment",
                impact_score=0.22,
                direction="increases",
                explanation=f"Elevated economic stress ({economic_stress:.1%}) increases systemic default risk"
            ))
        
        # Sort by impact
        contributing_factors.sort(key=lambda x: x.impact_score, reverse=True)
        contributing_factors = contributing_factors[:5]  # Top 5
        
        # Sensitivity analysis
        sensitivity_analysis = [
            SensitivityAnalysis(
                parameter="Interest Rate",
                baseline_value=scenario_params.get("macro_context", {}).get("interest_rate_level", 2.5),
                sensitivity_range={
                    "low": scenario_params.get("macro_context", {}).get("interest_rate_level", 2.5) - 1.0,
                    "high": scenario_params.get("macro_context", {}).get("interest_rate_level", 2.5) + 2.0
                },
                impact_description=f"Risk increases by approximately {scenario_params.get('default_probability_sensitivity', 1.0) * 0.3:.1%} for each 1% increase in interest rates"
            ),
            SensitivityAnalysis(
                parameter="Debt-to-Income Ratio",
                baseline_value=dti,
                sensitivity_range={"low": max(0.0, dti - 0.1), "high": min(1.0, dti + 0.1)},
                impact_description="Risk increases non-linearly as DTI exceeds 40%"
            )
        ]
        
        # Scenario impact
        scenario_impact = ScenarioImpact(
            scenario_name=scenario_params.get("name", "Unknown"),
            scenario_adjustment={
                "default_probability_multiplier": scenario_params.get("default_probability_sensitivity", 1.0),
                "confidence_adjustment": scenario_params.get("confidence_degradation", 0.0)
            },
            decision_change=f"Scenario '{scenario_params.get('name', 'Unknown')}' adjusts default probability by {((scenario_params.get('default_probability_sensitivity', 1.0) - 1.0) * 100):.0f}%",
            confidence_impact=-scenario_params.get("confidence_degradation", 0.0)
        )
        
        # Uncertainty notes
        uncertainty_notes = None
        if default_probability > 0.3 and default_probability < 0.7:
            uncertainty_notes = "Risk assessment in moderate range - limited historical data in similar conditions. Consider additional verification."
        elif scenario_params.get("confidence_degradation", 0) > 0.1:
            uncertainty_notes = f"Scenario uncertainty reduces confidence. Economic conditions ({scenario_params.get('name', 'Unknown')}) may deviate from historical patterns."
        
        # Human review recommendation
        human_review_recommended = (
            risk_score < 0.5 or
            default_probability > 0.3 or
            economic_stress > 0.6 or
            dti > 0.45
        )
        
        # ========== DECISION WALKTHROUGH STRUCTURE ==========
        
        # Section 1: What Question Was Answered?
        decision_objective = "This system evaluated the likelihood of loan default within the next 12 months under the current conditions to support a faster, more consistent human decision."
        
        # Section 2: What Information Was Considered
        information_categories = [
            "Customer financial behavior",
            "Credit history patterns",
            "Employment and income stability",
            "Market and economic context",
            "Peer comparison with similar cases"
        ]
        
        # Section 3: How the System Reached This Decision
        decision_flow = [
            "Identified patterns similar to past cases with known outcomes",
            "Compared borrower behavior against expected norms for their profile",
            "Adjusted for current market and economic conditions",
            "Measured deviation from low-risk borrower characteristics",
            "Summarized risk into a single decision signal"
        ]
        
        # Section 4: What Influenced This Result the Most
        top_influencing_factors_list = []
        for factor in contributing_factors[:5]:  # Top 5
            top_influencing_factors_list.append(InfluencingFactor(
                factor_name=factor.factor_name,
                influence_direction=factor.direction,
                short_reason=factor.explanation
            ))
        
        # Section 5: Confidence & Reliability
        if confidence_score >= 0.85:
            conf_level = "high"
            conf_reason = "Strong historical data patterns and consistent borrower information support this assessment."
        elif confidence_score >= 0.70:
            conf_level = "medium"
            conf_reason = "Good information quality, but some factors have limited historical precedent in similar conditions."
        else:
            conf_level = "low"
            conf_reason = "Limited or inconsistent information, or conditions that deviate significantly from historical patterns."
        
        confidence_assessment = ConfidenceAssessment(
            confidence_level=conf_level,
            confidence_reason=conf_reason,
            known_limitations=uncertainty_notes or "No significant limitations identified."
        )
        
        # Section 6: What Would Change This Outcome?
        sensitivity_triggers = [
            "Market conditions shift rapidly (interest rates, unemployment, economic stress)",
            "Borrower financial behavior changes significantly (income, employment, payment patterns)",
            "Additional credit history or financial data becomes available"
        ]
        
        # Section 7: Human Review Guidance
        if human_review_recommended:
            review_reason = "Human review is recommended because this decision is borderline, economic conditions are unstable, or the borrower profile is unusual."
        else:
            review_reason = "Standard automated processing is appropriate. Borrower profile and conditions align with well-understood patterns."
        
        human_review_guidance = HumanReviewGuidance(
            review_recommended=human_review_recommended,
            review_reason=review_reason
        )
        
        return ExplanationObject(
            # Decision Walkthrough fields
            decision_objective=decision_objective,
            information_categories=information_categories,
            decision_flow=decision_flow,
            top_influencing_factors=top_influencing_factors_list,
            confidence_assessment=confidence_assessment,
            sensitivity_triggers=sensitivity_triggers,
            human_review_guidance=human_review_guidance,
            # Legacy fields
            decision_summary=decision_summary,
            confidence_score=confidence_score,
            top_contributing_factors=contributing_factors,
            sensitivity_analysis=sensitivity_analysis,
            scenario_impact=scenario_impact,
            uncertainty_notes=uncertainty_notes,
            human_review_recommended=human_review_recommended,
            model_version=model_metadata.get("model_version", "1.0.0"),
            inference_timestamp=datetime.now()
        )
    
    def generate_fraud_detection_explanation(
        self,
        fraud_probability: float,
        fraud_flag: bool,
        transaction_features: Dict[str, Any],
        scenario_params: Dict[str, Any],
        model_metadata: Dict[str, Any]
    ) -> ExplanationObject:
        """Generate explanation for fraud detection"""
        
        # Decision summary
        if fraud_flag:
            if fraud_probability > 0.8:
                decision_summary = "High-confidence fraud detection. Transaction exhibits multiple fraud indicators."
            else:
                decision_summary = "Suspicious transaction detected. Fraud indicators present but require verification."
        else:
            decision_summary = "Transaction appears legitimate. No significant fraud indicators detected."
        
        # Confidence score
        confidence_score = min(0.95, 0.7 + abs(fraud_probability - 0.5) * 0.5)
        
        # Top contributing factors
        contributing_factors = []
        
        # Amount deviation
        amount_deviation = transaction_features.get("amount_deviation", 0.0)
        if amount_deviation > 0.5:
            contributing_factors.append(ContributingFactor(
                factor_name="Transaction Amount Anomaly",
                impact_score=0.25,
                direction="increases",
                explanation=f"Transaction amount significantly deviates from typical patterns ({amount_deviation:.1%} deviation)"
            ))
        
        # Geo deviation
        geo_deviation = transaction_features.get("geo_deviation", False)
        if geo_deviation:
            contributing_factors.append(ContributingFactor(
                factor_name="Geographic Anomaly",
                impact_score=0.30,
                direction="increases",
                explanation="Transaction from unusual geographic location compared to account history"
            ))
        
        # Velocity
        velocity_anomaly = transaction_features.get("velocity_anomaly", False)
        if velocity_anomaly:
            contributing_factors.append(ContributingFactor(
                factor_name="Transaction Velocity",
                impact_score=0.20,
                direction="increases",
                explanation="Unusual transaction velocity detected - potential card testing or account takeover"
            ))
        
        # Channel type
        channel_type = transaction_features.get("channel_type", "online")
        if channel_type in ["online", "mobile"]:
            contributing_factors.append(ContributingFactor(
                factor_name="Transaction Channel",
                impact_score=0.15,
                direction="increases",
                explanation="Online/mobile channels have higher fraud risk due to reduced authentication"
            ))
        
        # Sort by impact
        contributing_factors.sort(key=lambda x: x.impact_score, reverse=True)
        contributing_factors = contributing_factors[:5]
        
        # Sensitivity analysis
        sensitivity_analysis = [
            SensitivityAnalysis(
                parameter="Transaction Amount",
                baseline_value=transaction_features.get("amount", 0.0),
                sensitivity_range={
                    "low": transaction_features.get("amount", 0.0) * 0.5,
                    "high": transaction_features.get("amount", 0.0) * 2.0
                },
                impact_description="Fraud probability increases non-linearly with transaction amount, especially for unusual amounts"
            )
        ]
        
        # Scenario impact
        scenario_impact = ScenarioImpact(
            scenario_name=scenario_params.get("name", "Unknown"),
            scenario_adjustment={
                "fraud_probability_bias": scenario_params.get("fraud_probability_bias", 0.0),
                "velocity_threshold": scenario_params.get("velocity_threshold_multiplier", 1.0)
            },
            decision_change=f"Scenario '{scenario_params.get('name', 'Unknown')}' adjusts fraud detection sensitivity",
            confidence_impact=0.0
        )
        
        # Uncertainty notes
        uncertainty_notes = None
        if 0.4 < fraud_probability < 0.6:
            uncertainty_notes = "Fraud probability in ambiguous range. Additional verification recommended."
        
        # Human review recommendation
        human_review_recommended = fraud_flag or fraud_probability > 0.4
        
        # ========== DECISION WALKTHROUGH STRUCTURE ==========
        
        # Section 1: What Question Was Answered?
        decision_objective = "This system evaluated whether this transaction behaves like legitimate customer activity or potential fraud to support real-time transaction security decisions."
        
        # Section 2: What Information Was Considered
        information_categories = [
            "Transaction patterns and history",
            "Account behavior and typical activity",
            "Geographic and device context",
            "Transaction velocity and timing",
            "Comparison with known fraud patterns"
        ]
        
        # Section 3: How the System Reached This Decision
        decision_flow = [
            "Identified patterns similar to past fraudulent or legitimate transactions",
            "Compared transaction behavior against account's typical patterns",
            "Evaluated deviation from expected customer behavior",
            "Assessed multiple risk signals simultaneously",
            "Summarized fraud probability into a decision signal"
        ]
        
        # Section 4: What Influenced This Result the Most
        top_influencing_factors_list = []
        for factor in contributing_factors[:5]:
            top_influencing_factors_list.append(InfluencingFactor(
                factor_name=factor.factor_name,
                influence_direction=factor.direction,
                short_reason=factor.explanation
            ))
        
        # Section 5: Confidence & Reliability
        if confidence_score >= 0.85:
            conf_level = "high"
            conf_reason = "Strong behavioral patterns and clear transaction context support this assessment."
        elif confidence_score >= 0.70:
            conf_level = "medium"
            conf_reason = "Good transaction data, but some patterns are ambiguous or have limited historical precedent."
        else:
            conf_level = "low"
            conf_reason = "Limited transaction history or conflicting behavioral signals reduce confidence."
        
        confidence_assessment = ConfidenceAssessment(
            confidence_level=conf_level,
            confidence_reason=conf_reason,
            known_limitations=uncertainty_notes or "No significant limitations identified."
        )
        
        # Section 6: What Would Change This Outcome?
        sensitivity_triggers = [
            "Customer behavior changes significantly (new spending patterns, location, device)",
            "Transaction context shifts (merchant category, amount patterns, timing)",
            "Additional account history or verification data becomes available"
        ]
        
        # Section 7: Human Review Guidance
        if human_review_recommended:
            review_reason = "Human review is recommended because fraud probability is elevated, transaction patterns are unusual, or the decision is borderline."
        else:
            review_reason = "Standard automated processing is appropriate. Transaction aligns with expected customer behavior patterns."
        
        human_review_guidance = HumanReviewGuidance(
            review_recommended=human_review_recommended,
            review_reason=review_reason
        )
        
        return ExplanationObject(
            # Decision Walkthrough fields
            decision_objective=decision_objective,
            information_categories=information_categories,
            decision_flow=decision_flow,
            top_influencing_factors=top_influencing_factors_list,
            confidence_assessment=confidence_assessment,
            sensitivity_triggers=sensitivity_triggers,
            human_review_guidance=human_review_guidance,
            # Legacy fields
            decision_summary=decision_summary,
            confidence_score=confidence_score,
            top_contributing_factors=contributing_factors,
            sensitivity_analysis=sensitivity_analysis,
            scenario_impact=scenario_impact,
            uncertainty_notes=uncertainty_notes,
            human_review_recommended=human_review_recommended,
            model_version=model_metadata.get("model_version", "1.0.0"),
            inference_timestamp=datetime.now()
        )
    
    def generate_kyc_aml_explanation(
        self,
        aml_risk_score: float,
        aml_risk_level: str,
        escalation_required: bool,
        customer_features: Dict[str, Any],
        scenario_params: Dict[str, Any],
        model_metadata: Dict[str, Any]
    ) -> ExplanationObject:
        """Generate explanation for KYC/AML risk assessment"""
        
        # Decision summary
        if aml_risk_level == "low":
            decision_summary = "Low AML risk. Customer profile indicates standard retail customer with minimal risk factors."
        elif aml_risk_level == "medium":
            decision_summary = "Medium AML risk. Some risk factors present but within acceptable parameters."
        elif aml_risk_level == "high":
            decision_summary = "High AML risk. Multiple risk factors detected requiring enhanced due diligence."
        else:
            decision_summary = "Very high AML risk. Customer profile exhibits significant red flags requiring immediate escalation."
        
        # Confidence score
        confidence_score = 0.80
        if aml_risk_level in ["low", "very_high"]:
            confidence_score = 0.90
        
        # Top contributing factors
        contributing_factors = []
        
        # Jurisdiction risk
        jurisdiction_risk = customer_features.get("jurisdiction_risk", "low")
        if jurisdiction_risk in ["high", "very_high"]:
            contributing_factors.append(ContributingFactor(
                factor_name="Jurisdiction Risk",
                impact_score=0.30,
                direction="increases",
                explanation=f"High-risk jurisdiction with potential sanctions exposure"
            ))
        elif jurisdiction_risk == "low":
            contributing_factors.append(ContributingFactor(
                factor_name="Jurisdiction Risk",
                impact_score=0.15,
                direction="decreases",
                explanation="Low-risk jurisdiction reduces AML concerns"
            ))
        
        # Occupation risk
        occupation_risk = customer_features.get("occupation_risk_level", "low")
        if occupation_risk == "high":
            contributing_factors.append(ContributingFactor(
                factor_name="Occupation Risk",
                impact_score=0.25,
                direction="increases",
                explanation="High-risk occupation (e.g., PEP, cash-intensive business) increases AML risk"
            ))
        
        # Network complexity
        network_complexity = customer_features.get("network_complexity_score", 0.3)
        if network_complexity > 0.6:
            contributing_factors.append(ContributingFactor(
                factor_name="Relationship Network",
                impact_score=0.20,
                direction="increases",
                explanation=f"Complex relationship network ({network_complexity:.1%}) with potential high-risk links"
            ))
        
        # Identity verification
        identity_scores = customer_features.get("identity_verification_scores", {})
        avg_identity_score = sum(identity_scores.values()) / len(identity_scores) if identity_scores else 0.9
        if avg_identity_score < 0.7:
            contributing_factors.append(ContributingFactor(
                factor_name="Identity Verification",
                impact_score=0.18,
                direction="increases",
                explanation="Lower identity verification scores indicate potential identity concerns"
            ))
        
        # Sort by impact
        contributing_factors.sort(key=lambda x: x.impact_score, reverse=True)
        contributing_factors = contributing_factors[:5]
        
        # Sensitivity analysis
        sensitivity_analysis = [
            SensitivityAnalysis(
                parameter="Network Complexity",
                baseline_value=network_complexity,
                sensitivity_range={"low": max(0.0, network_complexity - 0.2), "high": min(1.0, network_complexity + 0.2)},
                impact_description="AML risk increases significantly as network complexity exceeds 0.6"
            )
        ]
        
        # Scenario impact
        scenario_impact = ScenarioImpact(
            scenario_name=scenario_params.get("name", "Unknown"),
            scenario_adjustment={
                "aml_risk_multiplier": scenario_params.get("aml_risk_bias", 0.0),
                "jurisdiction_weight": scenario_params.get("jurisdiction_risk_multiplier", 1.0)
            },
            decision_change=f"Scenario '{scenario_params.get('name', 'Unknown')}' adjusts AML risk assessment",
            confidence_impact=0.0
        )
        
        # Uncertainty notes
        uncertainty_notes = None
        if aml_risk_level == "medium":
            uncertainty_notes = "Risk assessment in moderate range. Additional information may clarify risk profile."
        
        # Human review recommendation
        human_review_recommended = escalation_required or aml_risk_level in ["high", "very_high"]
        
        # ========== DECISION WALKTHROUGH STRUCTURE ==========
        
        # Section 1: What Question Was Answered?
        decision_objective = "This system evaluated the customer's compliance risk and potential exposure to money laundering or sanctions violations to support regulatory compliance decisions."
        
        # Section 2: What Information Was Considered
        information_categories = [
            "Customer identity and verification signals",
            "Jurisdiction and country risk profiles",
            "Occupation and business relationships",
            "Network connections and entity links",
            "Comparison with known high-risk profiles"
        ]
        
        # Section 3: How the System Reached This Decision
        decision_flow = [
            "Identified patterns similar to past compliance cases",
            "Compared customer profile against known risk indicators",
            "Evaluated jurisdiction and network complexity factors",
            "Assessed identity verification quality and consistency",
            "Summarized AML risk into a compliance decision signal"
        ]
        
        # Section 4: What Influenced This Result the Most
        top_influencing_factors_list = []
        for factor in contributing_factors[:5]:
            top_influencing_factors_list.append(InfluencingFactor(
                factor_name=factor.factor_name,
                influence_direction=factor.direction,
                short_reason=factor.explanation
            ))
        
        # Section 5: Confidence & Reliability
        if confidence_score >= 0.85:
            conf_level = "high"
            conf_reason = "Strong identity verification and clear risk profile patterns support this assessment."
        elif confidence_score >= 0.70:
            conf_level = "medium"
            conf_reason = "Good customer data, but some risk factors have limited historical precedent or are ambiguous."
        else:
            conf_level = "low"
            conf_reason = "Limited customer information or conflicting risk signals reduce confidence."
        
        confidence_assessment = ConfidenceAssessment(
            confidence_level=conf_level,
            confidence_reason=conf_reason,
            known_limitations=uncertainty_notes or "No significant limitations identified."
        )
        
        # Section 6: What Would Change This Outcome?
        sensitivity_triggers = [
            "Customer profile changes (new relationships, occupation, jurisdiction exposure)",
            "Regulatory environment shifts (sanctions updates, jurisdiction risk changes)",
            "Additional identity verification or relationship network data becomes available"
        ]
        
        # Section 7: Human Review Guidance
        if human_review_recommended:
            review_reason = "Human review is recommended because AML risk is elevated, customer profile is unusual, or compliance requirements are complex."
        else:
            review_reason = "Standard automated processing is appropriate. Customer profile aligns with low-risk patterns and standard compliance requirements."
        
        human_review_guidance = HumanReviewGuidance(
            review_recommended=human_review_recommended,
            review_reason=review_reason
        )
        
        return ExplanationObject(
            # Decision Walkthrough fields
            decision_objective=decision_objective,
            information_categories=information_categories,
            decision_flow=decision_flow,
            top_influencing_factors=top_influencing_factors_list,
            confidence_assessment=confidence_assessment,
            sensitivity_triggers=sensitivity_triggers,
            human_review_guidance=human_review_guidance,
            # Legacy fields
            decision_summary=decision_summary,
            confidence_score=confidence_score,
            top_contributing_factors=contributing_factors,
            sensitivity_analysis=sensitivity_analysis,
            scenario_impact=scenario_impact,
            uncertainty_notes=uncertainty_notes,
            human_review_recommended=human_review_recommended,
            model_version=model_metadata.get("model_version", "1.0.0"),
            inference_timestamp=datetime.now()
        )
    
    def generate_market_signal_explanation(
        self,
        stress_state: str,
        stress_score: float,
        sentiment_index: float,
        market_features: Dict[str, Any],
        scenario_params: Dict[str, Any],
        model_metadata: Dict[str, Any]
    ) -> ExplanationObject:
        """Generate explanation for market signal intelligence"""
        
        # Decision summary
        if stress_state == "calm":
            decision_summary = "Market in calm state. Low volatility and stable conditions observed."
        elif stress_state == "stressed":
            decision_summary = "Market experiencing stress. Elevated volatility and uncertainty detected."
        else:
            decision_summary = "Market in volatile state. High volatility and rapid changes observed."
        
        # Confidence score
        confidence_score = 0.75
        if stress_score < 0.2 or stress_score > 0.8:
            confidence_score = 0.85
        
        # Top contributing factors
        contributing_factors = []
        
        # Volatility
        volatility = market_features.get("volatility_index", 0.2)
        if volatility > 0.5:
            contributing_factors.append(ContributingFactor(
                factor_name="Market Volatility",
                impact_score=0.30,
                direction="increases",
                explanation=f"Elevated volatility ({volatility:.1%}) indicates market stress"
            ))
        
        # Liquidity
        liquidity = market_features.get("liquidity_index", 0.7)
        if liquidity < 0.4:
            contributing_factors.append(ContributingFactor(
                factor_name="Liquidity Conditions",
                impact_score=0.25,
                direction="increases",
                explanation=f"Reduced liquidity ({liquidity:.1%}) increases market stress"
            ))
        
        # Sentiment
        if sentiment_index < -0.3:
            contributing_factors.append(ContributingFactor(
                factor_name="Market Sentiment",
                impact_score=0.20,
                direction="increases",
                explanation=f"Negative sentiment ({sentiment_index:.2f}) contributes to market stress"
            ))
        
        # Sort by impact
        contributing_factors.sort(key=lambda x: x.impact_score, reverse=True)
        contributing_factors = contributing_factors[:5]
        
        # Sensitivity analysis
        sensitivity_analysis = [
            SensitivityAnalysis(
                parameter="Volatility Index",
                baseline_value=volatility,
                sensitivity_range={"low": max(0.0, volatility - 0.2), "high": min(1.0, volatility + 0.2)},
                impact_description="Stress state transitions occur around volatility thresholds of 0.3 (calm to stressed) and 0.6 (stressed to volatile)"
            )
        ]
        
        # Scenario impact
        scenario_impact = ScenarioImpact(
            scenario_name=scenario_params.get("name", "Unknown"),
            scenario_adjustment={
                "volatility_bias": scenario_params.get("volatility_bias", 0.0),
                "sentiment_bias": scenario_params.get("sentiment_bias", 0.0)
            },
            decision_change=f"Scenario '{scenario_params.get('name', 'Unknown')}' adjusts market stress assessment",
            confidence_impact=0.0
        )
        
        # Uncertainty notes
        uncertainty_notes = "Market conditions can change rapidly. Continuous monitoring recommended."
        
        # Human review recommendation
        human_review_recommended = stress_state in ["stressed", "volatile"]
        
        # ========== DECISION WALKTHROUGH STRUCTURE ==========
        
        # Section 1: What Question Was Answered?
        decision_objective = "This system evaluated current market stress levels and sentiment conditions to support trading and risk management decisions."
        
        # Section 2: What Information Was Considered
        information_categories = [
            "Market volatility and price movements",
            "Liquidity conditions and trading activity",
            "News sentiment and market signals",
            "Historical market stress patterns",
            "Comparison with similar market environments"
        ]
        
        # Section 3: How the System Reached This Decision
        decision_flow = [
            "Identified patterns similar to past market stress periods",
            "Compared current market conditions against expected norms",
            "Evaluated volatility, liquidity, and sentiment signals",
            "Assessed deviation from calm market characteristics",
            "Summarized market stress into a decision signal"
        ]
        
        # Section 4: What Influenced This Result the Most
        top_influencing_factors_list = []
        for factor in contributing_factors[:5]:
            top_influencing_factors_list.append(InfluencingFactor(
                factor_name=factor.factor_name,
                influence_direction=factor.direction,
                short_reason=factor.explanation
            ))
        
        # Section 5: Confidence & Reliability
        if confidence_score >= 0.85:
            conf_level = "high"
            conf_reason = "Strong market data patterns and clear stress indicators support this assessment."
        elif confidence_score >= 0.70:
            conf_level = "medium"
            conf_reason = "Good market data, but some conditions have limited historical precedent or are rapidly changing."
        else:
            conf_level = "low"
            conf_reason = "Limited market data or rapidly changing conditions reduce confidence."
        
        confidence_assessment = ConfidenceAssessment(
            confidence_level=conf_level,
            confidence_reason=conf_reason,
            known_limitations=uncertainty_notes or "No significant limitations identified."
        )
        
        # Section 6: What Would Change This Outcome?
        sensitivity_triggers = [
            "Market conditions shift rapidly (volatility spikes, liquidity changes, news events)",
            "Sentiment indicators change significantly (news flow, economic data releases)",
            "Additional market data or longer time horizon becomes available"
        ]
        
        # Section 7: Human Review Guidance
        if human_review_recommended:
            review_reason = "Human review is recommended because market stress is elevated, conditions are volatile, or the assessment is borderline."
        else:
            review_reason = "Standard automated monitoring is appropriate. Market conditions align with stable patterns."
        
        human_review_guidance = HumanReviewGuidance(
            review_recommended=human_review_recommended,
            review_reason=review_reason
        )
        
        return ExplanationObject(
            # Decision Walkthrough fields
            decision_objective=decision_objective,
            information_categories=information_categories,
            decision_flow=decision_flow,
            top_influencing_factors=top_influencing_factors_list,
            confidence_assessment=confidence_assessment,
            sensitivity_triggers=sensitivity_triggers,
            human_review_guidance=human_review_guidance,
            # Legacy fields
            decision_summary=decision_summary,
            confidence_score=confidence_score,
            top_contributing_factors=contributing_factors,
            sensitivity_analysis=sensitivity_analysis,
            scenario_impact=scenario_impact,
            uncertainty_notes=uncertainty_notes,
            human_review_recommended=human_review_recommended,
            model_version=model_metadata.get("model_version", "1.0.0"),
            inference_timestamp=datetime.now()
        )
    
    def generate_regime_simulation_explanation(
        self,
        current_regime: str,
        regime_confidence: float,
        projected_regime: str,
        transition_probability: float,
        stress_indicators: Dict[str, float],
        scenario_params: Dict[str, Any],
        model_metadata: Dict[str, Any]
    ) -> ExplanationObject:
        """Generate explanation for regime simulation"""
        
        # Decision summary
        if current_regime == projected_regime:
            decision_summary = f"Market regime stable at '{current_regime}'. Low probability of regime transition."
        else:
            decision_summary = f"Market regime transition expected from '{current_regime}' to '{projected_regime}'. Transition probability: {transition_probability:.1%}."
        
        # Confidence score
        confidence_score = regime_confidence
        
        # Top contributing factors
        contributing_factors = []
        
        # Volatility shock
        vol_shock = stress_indicators.get("volatility_shock", 0.0)
        if vol_shock > 0.5:
            contributing_factors.append(ContributingFactor(
                factor_name="Volatility Shock",
                impact_score=0.30,
                direction="increases",
                explanation=f"Significant volatility shock ({vol_shock:.1%}) drives regime transition"
            ))
        
        # Correlation breakdown
        corr_breakdown = stress_indicators.get("correlation_breakdown", 0.0)
        if corr_breakdown > 0.6:
            contributing_factors.append(ContributingFactor(
                factor_name="Correlation Breakdown",
                impact_score=0.25,
                direction="increases",
                explanation=f"Asset correlation breakdown ({corr_breakdown:.1%}) indicates regime shift"
            ))
        
        # Liquidity crisis
        liq_crisis = stress_indicators.get("liquidity_crisis", 0.0)
        if liq_crisis > 0.5:
            contributing_factors.append(ContributingFactor(
                factor_name="Liquidity Crisis",
                impact_score=0.28,
                direction="increases",
                explanation=f"Liquidity crisis conditions ({liq_crisis:.1%}) force regime transition"
            ))
        
        # Sort by impact
        contributing_factors.sort(key=lambda x: x.impact_score, reverse=True)
        contributing_factors = contributing_factors[:5]
        
        # Sensitivity analysis
        sensitivity_analysis = [
            SensitivityAnalysis(
                parameter="Volatility Shock Level",
                baseline_value=vol_shock,
                sensitivity_range={"low": max(0.0, vol_shock - 0.2), "high": min(1.0, vol_shock + 0.2)},
                impact_description="Regime transition probability increases sharply as volatility shock exceeds 0.6"
            )
        ]
        
        # Scenario impact
        scenario_impact = ScenarioImpact(
            scenario_name=scenario_params.get("name", "Unknown"),
            scenario_adjustment={
                "volatility_shock_level": scenario_params.get("volatility_shock_level", 0.0),
                "correlation_breakdown_score": scenario_params.get("correlation_breakdown_score", 0.0)
            },
            decision_change=f"Scenario '{scenario_params.get('name', 'Unknown')}' simulates regime transition conditions",
            confidence_impact=0.0
        )
        
        # Uncertainty notes
        uncertainty_notes = "Regime transitions are probabilistic. Multiple scenarios should be considered."
        
        # Human review recommendation
        human_review_recommended = transition_probability > 0.5 or current_regime != projected_regime
        
        # ========== DECISION WALKTHROUGH STRUCTURE ==========
        
        # Section 1: What Question Was Answered?
        decision_objective = "This system evaluated current market regime and likelihood of regime transition to support portfolio risk management and trading strategy decisions."
        
        # Section 2: What Information Was Considered
        information_categories = [
            "Market volatility and return patterns",
            "Liquidity conditions and market depth",
            "Asset correlation patterns",
            "Historical regime transition patterns",
            "Stress scenario indicators"
        ]
        
        # Section 3: How the System Reached This Decision
        decision_flow = [
            "Identified patterns similar to past regime transitions",
            "Compared current market conditions against regime characteristics",
            "Evaluated volatility, correlation, and liquidity stress indicators",
            "Assessed probability of regime change based on stress levels",
            "Summarized regime state and transition likelihood into a decision signal"
        ]
        
        # Section 4: What Influenced This Result the Most
        top_influencing_factors_list = []
        for factor in contributing_factors[:5]:
            top_influencing_factors_list.append(InfluencingFactor(
                factor_name=factor.factor_name,
                influence_direction=factor.direction,
                short_reason=factor.explanation
            ))
        
        # Section 5: Confidence & Reliability
        if confidence_score >= 0.85:
            conf_level = "high"
            conf_reason = "Strong regime patterns and clear stress indicators support this assessment."
        elif confidence_score >= 0.70:
            conf_level = "medium"
            conf_reason = "Good market data, but regime transitions are probabilistic and conditions may change."
        else:
            conf_level = "low"
            conf_reason = "Limited historical precedent or rapidly changing conditions reduce confidence in regime assessment."
        
        confidence_assessment = ConfidenceAssessment(
            confidence_level=conf_level,
            confidence_reason=conf_reason,
            known_limitations=uncertainty_notes or "No significant limitations identified."
        )
        
        # Section 6: What Would Change This Outcome?
        sensitivity_triggers = [
            "Market stress indicators change rapidly (volatility shocks, liquidity crises, correlation breakdowns)",
            "Regime transition conditions evolve (stress levels, market structure changes)",
            "Additional market data or longer simulation horizon becomes available"
        ]
        
        # Section 7: Human Review Guidance
        if human_review_recommended:
            review_reason = "Human review is recommended because regime transition probability is elevated, stress indicators are significant, or the regime assessment is uncertain."
        else:
            review_reason = "Standard automated monitoring is appropriate. Regime appears stable with low transition probability."
        
        human_review_guidance = HumanReviewGuidance(
            review_recommended=human_review_recommended,
            review_reason=review_reason
        )
        
        return ExplanationObject(
            # Decision Walkthrough fields
            decision_objective=decision_objective,
            information_categories=information_categories,
            decision_flow=decision_flow,
            top_influencing_factors=top_influencing_factors_list,
            confidence_assessment=confidence_assessment,
            sensitivity_triggers=sensitivity_triggers,
            human_review_guidance=human_review_guidance,
            # Legacy fields
            decision_summary=decision_summary,
            confidence_score=confidence_score,
            top_contributing_factors=contributing_factors,
            sensitivity_analysis=sensitivity_analysis,
            scenario_impact=scenario_impact,
            uncertainty_notes=uncertainty_notes,
            human_review_recommended=human_review_recommended,
            model_version=model_metadata.get("model_version", "1.0.0"),
            inference_timestamp=datetime.now()
        )


# Global instance
fintech_explanation_engine = FintechExplanationEngine()

