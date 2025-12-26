# Fintech Decision Walkthrough API Structure

## Overview

The **Decision Walkthrough** information is **embedded directly in each Fintech use-case API response** - there is **no separate API endpoint**. This ensures all decision data and explanations are returned in a single, atomic response.

## API Response Structure

Every Fintech API response includes an `explanation` field that contains the complete Decision Walkthrough structure (7 sections).

### Example: Credit Risk API Response

**Endpoint**: `POST /api/v1/fintech/credit-risk`

**Response Structure**:
```json
{
  "success": true,
  "borrower_id": "BORROWER_123",
  "risk_score": 0.75,
  "risk_level": "medium",
  "default_probability": 0.25,
  "loss_given_default_estimate": 0.4,
  "recommendation": "Approve with enhanced monitoring",
  
  "explanation": {
    // ========== DECISION WALKTHROUGH (7 SECTIONS) ==========
    
    // Section 1: What Question Was Answered?
    "decision_objective": "This system evaluated the likelihood of loan default within the next 12 months under the current conditions to support a faster, more consistent human decision.",
    
    // Section 2: What Information Was Considered
    "information_categories": [
      "Customer financial behavior",
      "Credit history patterns",
      "Employment and income stability",
      "Market and economic context",
      "Peer comparison with similar cases"
    ],
    
    // Section 3: How the System Reached This Decision
    "decision_flow": [
      "Identified patterns similar to past cases with known outcomes",
      "Compared borrower behavior against expected norms for their profile",
      "Adjusted for current market and economic conditions",
      "Measured deviation from low-risk borrower characteristics",
      "Summarized risk into a single decision signal"
    ],
    
    // Section 4: What Influenced This Result the Most
    "top_influencing_factors": [
      {
        "factor_name": "Credit History Quality",
        "influence_direction": "decreases",
        "short_reason": "Strong credit history (good) significantly reduces default risk"
      },
      {
        "factor_name": "Debt-to-Income Ratio",
        "influence_direction": "increases",
        "short_reason": "High debt-to-income ratio (35.0%) indicates financial stress"
      }
    ],
    
    // Section 5: Confidence & Reliability of This Decision
    "confidence_assessment": {
      "confidence_level": "high",
      "confidence_reason": "Strong historical data patterns and consistent borrower information support this assessment.",
      "known_limitations": "No significant limitations identified."
    },
    
    // Section 6: What Would Change This Outcome?
    "sensitivity_triggers": [
      "Market conditions shift rapidly (interest rates, unemployment, economic stress)",
      "Borrower financial behavior changes significantly (income, employment, payment patterns)",
      "Additional credit history or financial data becomes available"
    ],
    
    // Section 7: Human Review Guidance
    "human_review_guidance": {
      "review_recommended": false,
      "review_reason": "Standard automated processing is appropriate. Borrower profile and conditions align with well-understood patterns."
    },
    
    // ========== LEGACY FIELDS (for backward compatibility) ==========
    "decision_summary": "Medium credit risk. Borrower shows acceptable creditworthiness with some areas of concern.",
    "confidence_score": 0.85,
    "top_contributing_factors": [...],
    "sensitivity_analysis": [...],
    "scenario_impact": {...},
    "uncertainty_notes": null,
    "human_review_recommended": false,
    "model_version": "1.0.0",
    "inference_timestamp": "2024-01-15T10:30:00Z"
  },
  
  "scenario_applied": "stable_economy",
  "metadata": {
    "borrower_profile": {...},
    "credit_history": {...},
    "financial_behavior": {...}
  }
}
```

## All Fintech Endpoints Include Decision Walkthrough

The same `explanation` structure is included in **all 5 Fintech modules**:

### 1. Credit Risk
- **Endpoint**: `POST /api/v1/fintech/credit-risk`
- **Response Model**: `CreditRiskResponse`
- **Explanation Field**: Contains Decision Walkthrough for credit risk assessment

### 2. Fraud Detection
- **Endpoint**: `POST /api/v1/fintech/fraud-detection`
- **Response Model**: `FraudDetectionResponse`
- **Explanation Field**: Contains Decision Walkthrough for fraud detection

### 3. KYC / AML
- **Endpoint**: `POST /api/v1/fintech/kyc-aml`
- **Response Model**: `KYCRiskResponse`
- **Explanation Field**: Contains Decision Walkthrough for compliance risk

### 4. Market Signal Intelligence
- **Endpoint**: `POST /api/v1/fintech/market-signal`
- **Response Model**: `MarketSignalResponse`
- **Explanation Field**: Contains Decision Walkthrough for market stress analysis

### 5. Market Regime Simulation
- **Endpoint**: `POST /api/v1/fintech/regime-simulation`
- **Response Model**: `RegimeSimulationResponse`
- **Explanation Field**: Contains Decision Walkthrough for regime transition analysis

## UI Integration Pattern

### Single API Call Pattern

```javascript
// Frontend code example
async function getCreditRiskAssessment(borrowerData, scenario) {
  const response = await fetch('/api/v1/fintech/credit-risk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      borrower_id: borrowerData.id,
      scenario: scenario,
      borrower_data: borrowerData
    })
  });
  
  const result = await response.json();
  
  // Main decision data
  const riskScore = result.risk_score;
  const riskLevel = result.risk_level;
  const recommendation = result.recommendation;
  
  // Decision Walkthrough data (all 7 sections)
  const walkthrough = result.explanation;
  
  // Section 1: What Question Was Answered?
  const question = walkthrough.decision_objective;
  
  // Section 2: What Information Was Considered
  const categories = walkthrough.information_categories;
  
  // Section 3: How the System Reached This Decision
  const flow = walkthrough.decision_flow;
  
  // Section 4: What Influenced This Result the Most
  const factors = walkthrough.top_influencing_factors;
  
  // Section 5: Confidence & Reliability
  const confidence = walkthrough.confidence_assessment;
  
  // Section 6: What Would Change This Outcome?
  const triggers = walkthrough.sensitivity_triggers;
  
  // Section 7: Human Review Guidance
  const review = walkthrough.human_review_guidance;
  
  return {
    decision: { riskScore, riskLevel, recommendation },
    walkthrough: {
      question,
      categories,
      flow,
      factors,
      confidence,
      triggers,
      review
    }
  };
}
```

## Benefits of Embedded Approach

### ✅ Advantages

1. **Atomic Response**: All decision data and explanation come together
2. **No Extra API Calls**: Single request/response cycle
3. **Consistency**: Explanation always matches the decision
4. **Performance**: Faster UI rendering (no waiting for second API call)
5. **Simplicity**: Frontend doesn't need to manage multiple endpoints

### ❌ Why Not a Separate Endpoint?

- **Data Consistency**: Explanation must match the exact decision - separate calls risk mismatches
- **Performance**: Extra network round-trip adds latency
- **Complexity**: Frontend must coordinate two API calls
- **Atomicity**: Decision and explanation are one logical unit

## Response Schema

The `explanation` field is of type `ExplanationObject` with the following structure:

```python
class ExplanationObject(BaseModel):
    # Decision Walkthrough (7 sections)
    decision_objective: str
    information_categories: List[str]
    decision_flow: List[str]
    top_influencing_factors: List[InfluencingFactor]
    confidence_assessment: ConfidenceAssessment
    sensitivity_triggers: List[str]
    human_review_guidance: HumanReviewGuidance
    
    # Legacy fields (backward compatibility)
    decision_summary: str
    confidence_score: float
    top_contributing_factors: List[ContributingFactor]
    # ... other legacy fields
```

## Testing

You can test the Decision Walkthrough structure using any Fintech endpoint:

```bash
# Example: Credit Risk
curl -X POST http://localhost:8000/api/v1/fintech/credit-risk \
  -H "Content-Type: application/json" \
  -d '{
    "borrower_id": "TEST_123",
    "scenario": "stable_economy",
    "borrower_data": {
      "age": 35,
      "credit_score_band": "good",
      "debt_to_income_ratio": 0.35
    }
  }'

# The response will include the full explanation object with all 7 sections
```

## Summary

- **No separate API**: Decision Walkthrough is embedded in each use-case response
- **Single call**: One API request returns decision + explanation
- **Consistent structure**: All 5 modules use the same 7-section format
- **UI-ready**: Frontend can directly map `response.explanation` to Decision Walkthrough tab

