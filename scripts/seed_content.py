"""
Seed script to migrate hardcoded industry and use case data to database
Run this after migrations to populate the database with existing content
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.industry import Industry
from app.models.use_case import UseCase, UseCaseCategory
from app.models.admin import Theme, ContentBlock, ContentAsset
from app.core.database import Base

# Industry data extracted from frontend (without JSX icons)
INDUSTRIES_DATA = {
    "healthcare": {
        "id": "healthcare",
        "name": "Healthcare AI",
        "tagline": "Transforming patient care with intelligent solutions",
        "description": "8 AI use cases for modern healthcare delivery",
        "icon": "LocalHospital",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "Clinical Intelligence",
                "icon": "MonitorHeart",
                "color": "#6b7280",
                "description": "AI-powered clinical decision support",
                "use_cases": [
                    {
                        "key": "risk-scoring",
                        "label": "Patient Risk Scoring",
                        "description": "Predict patient deterioration and readmission risk",
                        "icon": "HealthAndSafety",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Early intervention", "Reduce readmissions", "Resource allocation"],
                            "how_it_works": "ML models analyze vitals, lab results, and medical history to predict patient risk scores.",
                            "tech_stack": ["XGBoost", "FHIR", "Python", "React"],
                        },
                    },
                    {
                        "key": "diagnostic-ai",
                        "label": "Diagnostic Image Analysis",
                        "description": "AI-assisted radiology and pathology",
                        "icon": "Biotech",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Faster diagnosis", "Consistency", "Second opinion"],
                            "how_it_works": "CNN models trained on medical images detect anomalies in X-rays, CT scans, and pathology slides.",
                            "tech_stack": ["ResNet", "U-Net", "DICOM", "PyTorch"],
                        },
                    },
                ],
            },
            {
                "title": "Drug & Research Intelligence",
                "icon": "Medication",
                "color": "#6b7280",
                "description": "Accelerate pharmaceutical research and discovery",
                "use_cases": [
                    {
                        "key": "drug-discovery",
                        "label": "Drug Discovery AI",
                        "description": "Accelerate molecule screening and drug candidates",
                        "icon": "LocalPharmacy",
                        "route": "#",
                        "details": {
                            "duration": "12-15 min",
                            "difficulty": "Advanced",
                            "benefits": ["Faster R&D", "Cost reduction", "Novel compounds"],
                            "how_it_works": "Graph neural networks predict molecular properties and drug-target interactions.",
                            "tech_stack": ["Graph Neural Networks", "RDKit", "PyTorch", "Molecular DB"],
                        },
                    },
                    {
                        "key": "clinical-trials",
                        "label": "Clinical Trial Optimization",
                        "description": "Patient matching and trial design",
                        "icon": "PersonSearch",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Better recruitment", "Diverse cohorts", "Faster enrollment"],
                            "how_it_works": "NLP extracts eligibility criteria and matches against patient records.",
                            "tech_stack": ["NLP", "EHR Integration", "Python"],
                        },
                    },
                ],
            },
            {
                "title": "Operational Intelligence",
                "icon": "Assessment",
                "color": "#ef4444",
                "description": "AI-driven healthcare operations optimization",
                "use_cases": [
                    {
                        "key": "patient-flow",
                        "label": "Patient Flow Prediction",
                        "description": "Forecast admissions and optimize bed management",
                        "icon": "Psychology",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Capacity planning", "Reduce wait times", "Staff scheduling"],
                            "how_it_works": "Time series models predict patient volumes based on historical patterns and external factors.",
                            "tech_stack": ["Prophet", "LSTM", "Python"],
                        },
                    },
                    {
                        "key": "resource-allocation",
                        "label": "Resource Allocation AI",
                        "description": "Optimize staff and equipment utilization",
                        "icon": "Assessment",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Advanced",
                            "benefits": ["Cost efficiency", "Better care", "Reduced burnout"],
                            "how_it_works": "Optimization algorithms allocate resources based on predicted demand and constraints.",
                            "tech_stack": ["Operations Research", "Constraint Programming", "Python"],
                        },
                    },
                ],
            },
        ],
    },
    "manufacturing": {
        "id": "manufacturing",
        "name": "Manufacturing AI",
        "tagline": "Industry 4.0 Decision Intelligence Platform",
        "description": "6 AI use cases across Equipment, Quality & Supply Chain",
        "icon": "Factory",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "⚙️ EQUIPMENT",
                "icon": "Settings",
                "color": "#6b7280",
                "description": "Prevent downtime, optimize energy",
                "use_cases": [
                    {
                        "key": "predictive-maintenance",
                        "label": "Predictive Maintenance",
                        "description": "Which machine is going to fail next — and when?",
                        "icon": "Engineering",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["20-40% downtime reduction", "Predict failures early", "Safety improvement"],
                            "how_it_works": "Continuous sensor-based health monitoring with LSTM/Temporal CNN models predict failure probability and remaining useful life.",
                            "tech_stack": ["Time Series", "LSTM/Temporal CNN", "Survival Analysis", "IoT"],
                        },
                    },
                    {
                        "key": "energy-optimization",
                        "label": "Energy Optimization",
                        "description": "Where are we wasting energy without knowing?",
                        "icon": "ElectricalServices",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["10-25% energy savings", "Real-time visibility", "Cost leakage detection"],
                            "how_it_works": "Real-time energy pattern modeling with anomaly detection identifies waste and optimizes load vs output.",
                            "tech_stack": ["Regression", "Clustering", "Anomaly Detection", "IoT"],
                        },
                    },
                ],
            },
            {
                "title": "🧪 QUALITY",
                "icon": "PrecisionManufacturing",
                "color": "#6b7280",
                "description": "100% inspection, zero defects",
                "use_cases": [
                    {
                        "key": "quality-vision",
                        "label": "Visual Quality Inspection",
                        "description": "Which products are defective — before shipping?",
                        "icon": "PrecisionManufacturing",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["30-60% defect escape reduction", "100% inspection", "Consistent judgment"],
                            "how_it_works": "Camera-based defect detection using CNN (ResNet/EfficientNet) and object detection (YOLO/DETR) for 100% inspection.",
                            "tech_stack": ["CNN", "ResNet/EfficientNet", "YOLO/DETR", "Segmentation"],
                        },
                    },
                    {
                        "key": "process-optimization",
                        "label": "Process Optimization",
                        "description": "Which parameters actually control yield?",
                        "icon": "Memory",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Advanced",
                            "benefits": ["Yield improvement", "Parameter sensitivity", "Safe operating ranges"],
                            "how_it_works": "Parameter sensitivity modeling with Bayesian optimization and SHAP feature importance analysis.",
                            "tech_stack": ["Bayesian Optimization", "SHAP", "Regression", "Feature Importance"],
                        },
                    },
                ],
            },
            {
                "title": "🚚 SUPPLY CHAIN",
                "icon": "LocalShipping",
                "color": "#6b7280",
                "description": "Demand forecasting, risk mitigation",
                "use_cases": [
                    {
                        "key": "demand-planning",
                        "label": "Demand Planning",
                        "description": "How much should we produce next week/month?",
                        "icon": "Warehouse",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["15-30% inventory reduction", "Stock-out prevention", "Demand confidence bands"],
                            "how_it_works": "Multi-signal demand forecasting using Prophet/LSTM with scenario forecasting for conservative vs aggressive plans.",
                            "tech_stack": ["Prophet", "LSTM", "Multi-signal Forecasting", "Scenario Analysis"],
                        },
                    },
                    {
                        "key": "supply-optimization",
                        "label": "Supply Chain Optimization",
                        "description": "Where will delays or shortages hurt us most?",
                        "icon": "LocalShipping",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Risk mitigation", "Alternative sourcing", "Bottleneck alerts"],
                            "how_it_works": "Supplier risk scoring and logistics route optimization using graph optimization and risk scoring models.",
                            "tech_stack": ["Graph Optimization", "Risk Scoring", "Supplier Analytics", "Logistics"],
                        },
                    },
                ],
            },
        ],
    },
    "realestate": {
        "id": "realestate",
        "name": "Real Estate AI",
        "tagline": "Decision Intelligence for Property, Investment & Construction",
        "description": "6 AI use cases for valuation, investment, and construction intelligence",
        "icon": "HomeWork",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "🏷️ VALUATION",
                "icon": "MapOutlined",
                "color": "#6b7280",
                "description": "Automated property valuation and market analysis",
                "use_cases": [
                    {
                        "key": "property-valuation",
                        "label": "Property Valuation AI",
                        "description": "Automated, explainable property value estimation",
                        "icon": "HomeWork",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Accurate valuations", "Explainable AI", "Comparable analysis"],
                            "how_it_works": "Data-driven valuation using Gradient Boosting (XGBoost/LightGBM) and hedonic pricing regression with feature attribution (SHAP).",
                            "tech_stack": ["XGBoost", "LightGBM", "Hedonic Pricing", "SHAP"],
                        },
                    },
                    {
                        "key": "market-trend-analysis",
                        "label": "Market Trend Analysis",
                        "description": "Predict short- to mid-term market direction",
                        "icon": "TrendingUp",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Market insights", "Confidence bands", "Regime detection"],
                            "how_it_works": "Time-series forecasting using Prophet/LSTM with regime detection (bull/flat/cooling) and signal fusion.",
                            "tech_stack": ["Prophet", "LSTM", "Regime Detection", "Time Series"],
                        },
                    },
                ],
            },
            {
                "title": "💼 INVESTMENT",
                "icon": "TrendingUp",
                "color": "#6b7280",
                "description": "Investment opportunity scoring and lead prioritization",
                "use_cases": [
                    {
                        "key": "investment-scoring",
                        "label": "Investment Opportunity Scoring",
                        "description": "Rank properties by ROI potential",
                        "icon": "TrendingUp",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["ROI optimization", "Risk adjustment", "Investment profiles"],
                            "how_it_works": "Multi-factor scoring models with risk-adjusted return calculations and investment profile classification.",
                            "tech_stack": ["Scoring Models", "Risk-Adjusted ROI", "Multi-factor Analysis"],
                        },
                    },
                    {
                        "key": "lead-scoring",
                        "label": "Lead Scoring",
                        "description": "Prioritize serious buyers & sellers",
                        "icon": "People",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Better prioritization", "Conversion prediction", "Sales efficiency"],
                            "how_it_works": "Behavioral and financial intent scoring using logistic regression and random forest with probability-to-convert modeling.",
                            "tech_stack": ["Logistic Regression", "Random Forest", "Intent Scoring"],
                        },
                    },
                ],
            },
            {
                "title": "🏗️ CONSTRUCTION",
                "icon": "Construction",
                "color": "#6b7280",
                "description": "Project risk assessment and building optimization",
                "use_cases": [
                    {
                        "key": "project-risk",
                        "label": "Project Risk Assessment",
                        "description": "Predict construction overruns & failures",
                        "icon": "Construction",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Risk mitigation", "Early warnings", "Cost/time prediction"],
                            "how_it_works": "Predictive risk modeling across cost, time, and vendor reliability using risk classification models and delay prediction regression.",
                            "tech_stack": ["Risk Classification", "Delay Prediction", "Regression Models"],
                        },
                    },
                    {
                        "key": "smart-building",
                        "label": "Smart Building Analytics",
                        "description": "Optimize operational efficiency post-construction",
                        "icon": "HomeWork",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Energy savings", "Predictive maintenance", "Cost optimization"],
                            "how_it_works": "Predictive maintenance and energy optimization using anomaly detection and time-series forecasting with sensor data.",
                            "tech_stack": ["Anomaly Detection", "Time Series", "Energy Optimization", "IoT"],
                        },
                    },
                ],
            },
        ],
    },
    "travel": {
        "id": "travel",
        "name": "Travel AI",
        "tagline": "Demand Volatility & Experience Optimization",
        "description": "AI understands demand volatility, price sensitivity, and operational constraints — optimizing experiences before stress points become problems",
        "icon": "Flight",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "Pricing & Revenue Intelligence",
                "icon": "TrendingUp",
                "color": "#3b82f6",
                "description": "AI transforms pricing from reactive to proactive",
                "use_cases": [
                    {
                        "key": "dynamic-pricing",
                        "label": "Dynamic Pricing Engine",
                        "description": "Real-time price optimization based on demand",
                        "icon": "CurrencyExchange",
                        "route": "#",
                        "details": {
                            "duration": "~8 min",
                            "difficulty": "Advanced",
                            "benefits": ["Revenue maximization", "Real-time adaptation", "Continuous optimization"],
                            "how_it_works": "Prices adapt dynamically to demand, seasonality, and booking velocity. What took 3-5 days now happens in under 2 minutes.",
                            "tech_stack": ["Time-Series Modeling", "Price Elasticity", "Real-time Processing"],
                        },
                    },
                    {
                        "key": "demand-forecast",
                        "label": "Demand Forecasting",
                        "description": "Predict booking volumes with uncertainty bands",
                        "icon": "TravelExplore",
                        "route": "#",
                        "details": {
                            "duration": "~7 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Proactive planning", "Uncertainty awareness", "Risk zones"],
                            "how_it_works": "AI forecasts demand windows 30-90 days ahead with confidence levels and uncertainty bands.",
                            "tech_stack": ["Forecasting Models", "Uncertainty Quantification", "Time Series"],
                        },
                    },
                ],
            },
            {
                "title": "Personalized Travel Intelligence",
                "icon": "Recommend",
                "color": "#10b981",
                "description": "Context-aware personalization that converts",
                "use_cases": [
                    {
                        "key": "trip-recommendations",
                        "label": "Personalized Recommendations",
                        "description": "AI adapts recommendations to traveler intent and behavior",
                        "icon": "AttractionsOutlined",
                        "route": "#",
                        "details": {
                            "duration": "~6 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Higher conversion", "Better matches", "Context-aware"],
                            "how_it_works": "AI adapts recommendations to traveler intent, timing, and behavior. Recommendations that actually convert.",
                            "tech_stack": ["Intent Clustering", "Context-Aware Filtering", "Recommendation Systems"],
                        },
                    },
                    {
                        "key": "chatbot-concierge",
                        "label": "AI Concierge",
                        "description": "Conversational assistant that anticipates needs",
                        "icon": "Luggage",
                        "route": "#",
                        "details": {
                            "duration": "~5 min",
                            "difficulty": "Intermediate",
                            "benefits": ["24/7 support", "Proactive assistance", "Context memory"],
                            "how_it_works": "Conversational assistant anticipates needs and reduces friction. Context-aware conversations available 24/7.",
                            "tech_stack": ["Conversational AI", "Context Memory", "Decision Support"],
                        },
                    },
                ],
            },
            {
                "title": "Operational Intelligence",
                "icon": "FlightTakeoff",
                "color": "#f59e0b",
                "description": "AI-driven optimization that adapts to constraints",
                "use_cases": [
                    {
                        "key": "route-optimization",
                        "label": "Route Optimization",
                        "description": "Routes adapt to constraints and disruptions",
                        "icon": "DirectionsCar",
                        "route": "#",
                        "details": {
                            "duration": "~7 min",
                            "difficulty": "Advanced",
                            "benefits": ["Time savings", "Fuel efficiency", "Disruption handling"],
                            "how_it_works": "Routes adapt automatically to constraints and disruptions. Optimization happens in minutes, saving time and fuel.",
                            "tech_stack": ["Graph Algorithms", "Constraint Solvers", "Route Optimization"],
                        },
                    },
                    {
                        "key": "hotel-matching",
                        "label": "Hotel Matching AI",
                        "description": "Find the perfect hotel, not just the cheapest",
                        "icon": "Hotel",
                        "route": "#",
                        "details": {
                            "duration": "~6 min",
                            "difficulty": "Beginner",
                            "benefits": ["Better matches", "Higher satisfaction", "Reduced cancellations"],
                            "how_it_works": "AI matches traveler intent with hotel attributes. Best-fit selection leads to higher satisfaction.",
                            "tech_stack": ["Preference Matching", "Attribute Ranking", "Vector Similarity"],
                        },
                    },
                ],
            },
        ],
    },
    "fintech": {
        "id": "fintech",
        "name": "Fintech AI",
        "tagline": "Decision Intelligence, Not Predictions",
        "description": "Boardroom-grade AI for risk, compliance, and market intelligence",
        "icon": "AccountBalance",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "Boardroom-Grade Intelligence",
                "icon": "Shield",
                "color": "#6b7280",
                "description": "Enterprise decision intelligence for CXOs",
                "use_cases": [
                    {
                        "key": "credit-risk-intelligence",
                        "label": "Credit Risk Intelligence",
                        "description": "Understand exposure, uncertainty, and risk drivers",
                        "icon": "CreditScore",
                        "route": "#",
                        "details": {
                            "duration": "~8 min",
                            "difficulty": "Advanced",
                            "benefits": ["Near-real-time insight", "Explainable risk", "Decision readiness"],
                            "how_it_works": "AI compresses multi-day credit analysis into minutes with explainable risk decomposition.",
                            "tech_stack": ["Risk Models", "Feature Engineering", "Explainable AI"],
                        },
                    },
                    {
                        "key": "fraud-detection",
                        "label": "Fraud Detection Control Room",
                        "description": "Detect abnormal behavior the moment it happens",
                        "icon": "Security",
                        "route": "#",
                        "details": {
                            "duration": "~6 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Real-time detection", "Explainable alerts", "Reduced false positives"],
                            "how_it_works": "Live transaction monitoring with explainable anomaly detection and incident drill-down.",
                            "tech_stack": ["Anomaly Detection", "Real-time Streaming", "Explainable AI"],
                        },
                    },
                    {
                        "key": "kyc-aml",
                        "label": "KYC & AML Risk Engine",
                        "description": "Balance regulatory compliance with customer experience",
                        "icon": "Gavel",
                        "route": "#",
                        "details": {
                            "duration": "~7 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Faster onboarding", "Risk-based tiering", "Audit-ready"],
                            "how_it_works": "AI provides tiered, risk-based customer assessment with escalation logic and compliance trace.",
                            "tech_stack": ["Document AI", "Risk Tiering", "Compliance Automation"],
                        },
                    },
                    {
                        "key": "market-signal",
                        "label": "Market Signal Intelligence",
                        "description": "Understand market conditions without predicting prices",
                        "icon": "TrendingUp",
                        "route": "#",
                        "details": {
                            "duration": "~5 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Context awareness", "Strategic posture", "Risk awareness"],
                            "how_it_works": "AI analyzes news, sentiment, and macro events to provide market context and strategic implications.",
                            "tech_stack": ["NLP", "Sentiment Analysis", "Signal Processing"],
                        },
                    },
                ],
            },
            {
                "title": "Trader-Grade Intelligence",
                "icon": "TrendingUp",
                "color": "#6b7280",
                "description": "Advanced market regime analysis",
                "use_cases": [
                    {
                        "key": "market-regime",
                        "label": "Market Regime Simulation",
                        "description": "Stress test strategies across different market regimes",
                        "icon": "ShowChart",
                        "route": "#",
                        "details": {
                            "duration": "~9 min",
                            "difficulty": "Advanced",
                            "benefits": ["Stress testing", "Vulnerability assessment", "Risk awareness"],
                            "how_it_works": "AI simulates how trading strategies perform under different market regime conditions (volatile, stable, etc.) to identify vulnerabilities.",
                            "tech_stack": ["Regime Classification", "Monte Carlo", "Risk Models"],
                        },
                    },
                ],
            },
            {
                "title": "Market & Digital Asset Intelligence",
                "icon": "AccountBalanceWallet",
                "color": "#6b7280",
                "description": "Understand market behavior and digital asset evolution",
                "use_cases": [
                    {
                        "key": "commodity-trend",
                        "label": "Commodity Trend Intelligence",
                        "description": "AI-assisted analysis of short-term market direction for commodities",
                        "icon": "TrendingUp",
                        "route": "#",
                        "details": {
                            "duration": "~8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Pattern recognition", "Confidence-bounded signals", "Market context"],
                            "how_it_works": "AI analyzes historical behavior patterns to provide directional signals with confidence bands.",
                            "tech_stack": ["Pattern Recognition", "Time Series", "Confidence Modeling"],
                        },
                    },
                    {
                        "key": "market-regime-signals",
                        "label": "Market Regime Signals",
                        "description": "Identify current market phase: risk-on, risk-off, volatile, or stable",
                        "icon": "ShowChart",
                        "route": "#",
                        "details": {
                            "duration": "~7 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Regime classification", "Transition awareness", "Behavioral context"],
                            "how_it_works": "AI identifies the current market regime (risk-on, risk-off, volatile, stable) in real-time based on patterns and indicators.",
                            "tech_stack": ["Regime Classification", "Pattern Matching", "Signal Processing"],
                        },
                    },
                    {
                        "key": "crypto-adoption",
                        "label": "Digital Asset Adoption Intelligence",
                        "description": "Explore blockchain and digital asset usage evolution",
                        "icon": "AccountBalanceWallet",
                        "route": "#",
                        "details": {
                            "duration": "~6 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Adoption trends", "Geographic analysis", "Network intelligence"],
                            "how_it_works": "AI monitors adoption patterns across countries, exchanges, and user segments.",
                            "tech_stack": ["Adoption Analytics", "Network Analysis", "Trend Detection"],
                        },
                    },
                    {
                        "key": "exchange-risk-mapping",
                        "label": "Exchange & Market Risk Mapping",
                        "description": "Visualize concentration risk and systemic exposure",
                        "icon": "MapIcon",
                        "route": "#",
                        "details": {
                            "duration": "~8 min",
                            "difficulty": "Advanced",
                            "benefits": ["Risk visualization", "Dependency analysis", "Systemic awareness"],
                            "how_it_works": "AI maps exchange dependencies, liquidity clusters, and risk concentration patterns.",
                            "tech_stack": ["Risk Mapping", "Dependency Analysis", "Visualization"],
                        },
                    },
                ],
            },
        ],
    },
    "hospitality": {
        "id": "hospitality",
        "name": "Restaurant & Hospitality AI",
        "tagline": "Smart solutions for hospitality excellence",
        "description": "8 AI use cases for restaurants and hospitality",
        "icon": "Restaurant",
        "primary_color": "#ef4444",
        "secondary_color": "#dc2626",
        "categories": [
            {
                "title": "Menu & Kitchen",
                "icon": "MenuBook",
                "color": "#ef4444",
                "description": "Optimize menu and kitchen operations",
                "use_cases": [
                    {
                        "key": "menu-engineering",
                        "label": "Menu Engineering Intelligence",
                        "description": "Optimize menu profitability through margin, popularity, and profit analysis",
                        "icon": "MenuBook",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Higher margins", "Better UX", "Data-driven decisions"],
                            "how_it_works": "ML analyzes sales data, costs, and customer preferences using association rules and Bayesian inference to optimize menu profitability.",
                            "tech_stack": ["Association Rules", "Bayesian Inference", "Python"],
                        },
                    },
                ],
            },
            {
                "title": "Operations",
                "icon": "Groups",
                "color": "#6b7280",
                "description": "Streamline restaurant operations",
                "use_cases": [
                    {
                        "key": "demand-prediction",
                        "label": "AI-Powered Demand Forecasting & Kitchen Workflow Optimization",
                        "description": "Live operational command center for restaurant operations",
                        "icon": "Schedule",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Staff planning", "Inventory prep", "Reduce waste", "Workflow optimization"],
                            "how_it_works": "Time series models predict demand based on history, weather, events, and trends. AI provides real-time recommendations for kitchen prep, staffing, and workflow optimization.",
                            "tech_stack": ["Gradient Boosting", "Time Series", "Python", "React"],
                        },
                    },
                ],
            },
        ],
    },
    "ecommerce": {
        "id": "ecommerce",
        "name": "E-commerce AI",
        "tagline": "Complete AI solution for modern e-commerce",
        "description": "30 AI use cases for product discovery, personalization, pricing, and operations",
        "icon": "ShoppingCart",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "Product Discovery",
                "icon": "Search",
                "color": "#6b7280",
                "description": "Help customers find products faster with AI-powered search",
                "use_cases": [
                    {
                        "key": "nlp",
                        "label": "Smart Search (NLP)",
                        "description": "Natural language product search with semantic understanding",
                        "icon": "Search",
                        "route": "#",
                        "details": {
                            "duration": "5-8 min",
                            "difficulty": "Beginner",
                            "benefits": ["Understand user intent", "Handle typos & synonyms", "Multi-language support"],
                            "how_it_works": "Uses transformer models to understand natural language queries and match them with product attributes, descriptions, and metadata.",
                            "tech_stack": ["BERT", "Elasticsearch", "FastAPI", "React"],
                        },
                    },
                    {
                        "key": "vss",
                        "label": "Visual Similarity",
                        "description": "Image-based product discovery using deep learning",
                        "icon": "ImageSearch",
                        "route": "#",
                        "details": {
                            "duration": "8-12 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Shop by image", "Find similar styles", "Increase engagement"],
                            "how_it_works": "Extract visual embeddings from product images using CNN models, then perform similarity search in vector space.",
                            "tech_stack": ["ResNet", "FAISS", "PyTorch", "React"],
                        },
                    },
                    {
                        "key": "bundle",
                        "label": "Bundle Suggestions",
                        "description": "AI-powered outfit and bundle recommendations",
                        "icon": "Inventory",
                        "route": "#",
                        "details": {
                            "duration": "6-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Increase AOV", "Cross-sell automation", "Style consistency"],
                            "how_it_works": "Analyzes purchase patterns and visual compatibility to suggest complementary products.",
                            "tech_stack": ["Collaborative Filtering", "Graph Neural Networks", "Python"],
                        },
                    },
                ],
            },
            {
                "title": "Logistics & Operations",
                "icon": "LocalShipping",
                "color": "#6b7280",
                "description": "Optimize delivery and supply chain with predictive AI",
                "use_cases": [
                    {
                        "key": "eta",
                        "label": "ETA Prediction",
                        "description": "Accurate delivery time forecasting",
                        "icon": "Schedule",
                        "route": "#",
                        "details": {
                            "duration": "5-7 min",
                            "difficulty": "Beginner",
                            "benefits": ["Accurate delivery estimates", "Customer satisfaction", "Operational planning"],
                            "how_it_works": "Combines historical delivery data, traffic patterns, weather, and carrier performance to predict arrival times.",
                            "tech_stack": ["XGBoost", "Time Series", "FastAPI", "React"],
                        },
                    },
                    {
                        "key": "delay",
                        "label": "Delay Forecast",
                        "description": "Predict and prevent order delays",
                        "icon": "LocalShipping",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Proactive alerts", "Reduce complaints", "Better planning"],
                            "how_it_works": "ML models analyze risk factors like weather, carrier history, and route complexity to flag potential delays.",
                            "tech_stack": ["Random Forest", "Weather API", "Python", "React"],
                        },
                    },
                    {
                        "key": "inventory",
                        "label": "Inventory Reorder",
                        "description": "Smart replenishment recommendations",
                        "icon": "Warehouse",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Advanced",
                            "benefits": ["Prevent stockouts", "Reduce overstock", "Optimize capital"],
                            "how_it_works": "Demand forecasting combined with lead time analysis to recommend optimal reorder points and quantities.",
                            "tech_stack": ["Prophet", "ARIMA", "Python", "React"],
                        },
                    },
                ],
            },
            {
                "title": "Personalization",
                "icon": "Person",
                "color": "#6b7280",
                "description": "Deliver tailored experiences for every customer",
                "use_cases": [
                    {
                        "key": "personalization",
                        "label": "Real-Time Personalization",
                        "description": "Dynamic content per user session",
                        "icon": "Person",
                        "route": "#",
                        "details": {
                            "duration": "10-15 min",
                            "difficulty": "Advanced",
                            "benefits": ["Higher conversion", "Better engagement", "Increased loyalty"],
                            "how_it_works": "Real-time decision engine that combines user behavior, preferences, and context to personalize every touchpoint.",
                            "tech_stack": ["Feature Store", "Redis", "TensorFlow", "React"],
                        },
                    },
                    {
                        "key": "chat",
                        "label": "AI Chat Assistant",
                        "description": "Intelligent conversational support",
                        "icon": "Chat",
                        "route": "#",
                        "details": {
                            "duration": "8-12 min",
                            "difficulty": "Intermediate",
                            "benefits": ["24/7 support", "Reduce tickets", "Instant answers"],
                            "how_it_works": "LLM-powered chatbot trained on your product catalog and FAQs to handle customer queries.",
                            "tech_stack": ["GPT-4", "LangChain", "Vector DB", "React"],
                        },
                    },
                    {
                        "key": "voice",
                        "label": "Voice Search",
                        "description": "Voice-enabled product discovery",
                        "icon": "Mic",
                        "route": "#",
                        "details": {
                            "duration": "5-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Hands-free shopping", "Accessibility", "Mobile-first UX"],
                            "how_it_works": "Speech-to-text conversion followed by NLP processing to understand and execute product searches.",
                            "tech_stack": ["Whisper", "NLP Pipeline", "Web Speech API", "React"],
                        },
                    },
                ],
            },
            {
                "title": "Pricing & Fraud",
                "icon": "AttachMoney",
                "color": "#ef4444",
                "description": "Maximize revenue while protecting against fraud",
                "use_cases": [
                    {
                        "key": "pricing",
                        "label": "Dynamic Pricing",
                        "description": "AI-driven price optimization",
                        "icon": "AttachMoney",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Maximize margins", "Stay competitive", "Demand-based pricing"],
                            "how_it_works": "Analyzes demand elasticity, competitor prices, inventory levels, and market conditions to recommend optimal prices.",
                            "tech_stack": ["Reinforcement Learning", "Price Elasticity Models", "Python"],
                        },
                    },
                    {
                        "key": "fraud",
                        "label": "Fraud Detection",
                        "description": "Real-time transaction risk scoring",
                        "icon": "Security",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Reduce chargebacks", "Protect revenue", "Customer trust"],
                            "how_it_works": "ML models analyze transaction patterns, device fingerprints, and behavioral signals to score fraud risk.",
                            "tech_stack": ["Isolation Forest", "Neural Networks", "Real-time Streaming"],
                        },
                    },
                    {
                        "key": "coupon",
                        "label": "Coupon Abuse",
                        "description": "Detect promotional code misuse",
                        "icon": "LocalOffer",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Protect margins", "Fair promotions", "Reduce abuse"],
                            "how_it_works": "Pattern detection algorithms identify suspicious coupon usage across accounts and sessions.",
                            "tech_stack": ["Anomaly Detection", "Graph Analysis", "Python"],
                        },
                    },
                ],
            },
            {
                "title": "Marketing Intelligence",
                "icon": "TrendingDown",
                "color": "#ef4444",
                "description": "Data-driven marketing with predictive insights",
                "use_cases": [
                    {
                        "key": "churn",
                        "label": "Churn Prediction",
                        "description": "Identify at-risk customers early",
                        "icon": "TrendingDown",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Proactive retention", "Reduce churn", "Increase LTV"],
                            "how_it_works": "Survival analysis and ML models predict customer churn probability based on engagement patterns.",
                            "tech_stack": ["Survival Analysis", "XGBoost", "Python", "React"],
                        },
                    },
                    {
                        "key": "segmentation",
                        "label": "Customer Segmentation",
                        "description": "AI-powered audience clustering",
                        "icon": "PeopleAlt",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Targeted campaigns", "Personalized offers", "Better ROI"],
                            "how_it_works": "Unsupervised learning algorithms cluster customers based on behavior, demographics, and purchase patterns.",
                            "tech_stack": ["K-Means", "DBSCAN", "PCA", "Python"],
                        },
                    },
                    {
                        "key": "subject",
                        "label": "Email Subject Gen",
                        "description": "AI-generated high-converting subjects",
                        "icon": "Email",
                        "route": "#",
                        "details": {
                            "duration": "3-5 min",
                            "difficulty": "Beginner",
                            "benefits": ["Higher open rates", "A/B testing", "Time savings"],
                            "how_it_works": "LLM fine-tuned on high-performing email subjects generates compelling alternatives for your campaigns.",
                            "tech_stack": ["GPT-4", "Fine-tuning", "A/B Framework"],
                        },
                    },
                    {
                        "key": "leadgen",
                        "label": "Lead Gen Blueprint",
                        "description": "AI strategy recommendations",
                        "icon": "Leaderboard",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Qualified leads", "Better targeting", "Higher conversion"],
                            "how_it_works": "Analyzes your funnel data and market trends to recommend lead generation strategies.",
                            "tech_stack": ["Predictive Analytics", "Lead Scoring", "Python"],
                        },
                    },
                ],
            },
            {
                "title": "Product Intelligence",
                "icon": "Category",
                "color": "#6b7280",
                "description": "Automate product data management with AI",
                "use_cases": [
                    {
                        "key": "variant",
                        "label": "Variant Assignment",
                        "description": "Automatic variant detection",
                        "icon": "Label",
                        "route": "#",
                        "details": {
                            "duration": "5-7 min",
                            "difficulty": "Beginner",
                            "benefits": ["Automate cataloging", "Reduce errors", "Faster listing"],
                            "how_it_works": "Computer vision and NLP extract variant attributes (size, color, material) from images and descriptions.",
                            "tech_stack": ["Computer Vision", "NER", "Python", "React"],
                        },
                    },
                    {
                        "key": "categorization",
                        "label": "Auto Categorization",
                        "description": "ML-powered taxonomy mapping",
                        "icon": "Category",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Consistent taxonomy", "Faster onboarding", "Better search"],
                            "how_it_works": "Text classification models automatically assign products to the correct category in your taxonomy.",
                            "tech_stack": ["BERT", "Hierarchical Classification", "Python"],
                        },
                    },
                    {
                        "key": "sentiment",
                        "label": "Review Sentiment",
                        "description": "Customer feedback insights",
                        "icon": "Reviews",
                        "route": "#",
                        "details": {
                            "duration": "5-8 min",
                            "difficulty": "Beginner",
                            "benefits": ["Understand customers", "Improve products", "Track trends"],
                            "how_it_works": "NLP models analyze review text to extract sentiment, key topics, and actionable insights.",
                            "tech_stack": ["Sentiment Analysis", "Topic Modeling", "Python"],
                        },
                    },
                    {
                        "key": "descriptions",
                        "label": "Description Generator",
                        "description": "AI-generated product copy",
                        "icon": "Description",
                        "route": "#",
                        "details": {
                            "duration": "3-5 min",
                            "difficulty": "Beginner",
                            "benefits": ["SEO-optimized", "Consistent tone", "Scale content"],
                            "how_it_works": "LLM generates compelling product descriptions based on attributes, brand voice, and SEO keywords.",
                            "tech_stack": ["GPT-4", "SEO Optimization", "Content Templates"],
                        },
                    },
                ],
            },
            {
                "title": "Creative & AR Tools",
                "icon": "AutoFixHigh",
                "color": "#6b7280",
                "description": "Enhance product visuals with AI creativity",
                "use_cases": [
                    {
                        "key": "remover",
                        "label": "Background Remover",
                        "description": "AI-powered image editing",
                        "icon": "AutoFixHigh",
                        "route": "#",
                        "details": {
                            "duration": "3-5 min",
                            "difficulty": "Beginner",
                            "benefits": ["Professional photos", "Consistent style", "Save time"],
                            "how_it_works": "Segmentation models precisely separate foreground products from backgrounds for clean cutouts.",
                            "tech_stack": ["U-Net", "Segment Anything", "Python", "Canvas API"],
                        },
                    },
                    {
                        "key": "upscaler",
                        "label": "Image Upscaler",
                        "description": "Enhance image quality",
                        "icon": "PhotoSizeSelectActual",
                        "route": "#",
                        "details": {
                            "duration": "3-5 min",
                            "difficulty": "Beginner",
                            "benefits": ["HD images", "Zoom capability", "Better conversions"],
                            "how_it_works": "Super-resolution models enhance image quality and increase resolution without losing detail.",
                            "tech_stack": ["ESRGAN", "Real-ESRGAN", "Python"],
                        },
                    },
                    {
                        "key": "tryon",
                        "label": "AI Try-On (AR)",
                        "description": "Virtual fitting room",
                        "icon": "Checkroom",
                        "route": "#",
                        "details": {
                            "duration": "10-15 min",
                            "difficulty": "Advanced",
                            "benefits": ["Reduce returns", "Increase confidence", "Engagement"],
                            "how_it_works": "Combines pose estimation and image synthesis to virtually dress customers in products.",
                            "tech_stack": ["Pose Estimation", "GANs", "AR.js", "React"],
                        },
                    },
                ],
            },
            {
                "title": "Gamification",
                "icon": "Quiz",
                "color": "#ef4444",
                "description": "Engage customers with interactive AI experiences",
                "use_cases": [
                    {
                        "key": "quiz",
                        "label": "Product Match Quiz",
                        "description": "Interactive recommendation quiz",
                        "icon": "Quiz",
                        "route": "#",
                        "details": {
                            "duration": "5-8 min",
                            "difficulty": "Beginner",
                            "benefits": ["Higher engagement", "Personalized picks", "Data collection"],
                            "how_it_works": "Interactive quiz collects preferences and uses recommendation engine to suggest perfect products.",
                            "tech_stack": ["Recommendation Engine", "React", "Animation"],
                        },
                    },
                    {
                        "key": "spin",
                        "label": "Spin-to-Win",
                        "description": "Gamified promotional wheel",
                        "icon": "Casino",
                        "route": "#",
                        "details": {
                            "duration": "3-5 min",
                            "difficulty": "Beginner",
                            "benefits": ["Lead capture", "Viral potential", "Excitement"],
                            "how_it_works": "Configurable prize wheel with controlled probability distribution for promotional campaigns.",
                            "tech_stack": ["Probability Engine", "Canvas Animation", "React"],
                        },
                    },
                    {
                        "key": "iq",
                        "label": "IQ Game Suite",
                        "description": "Engagement mini-games",
                        "icon": "SportsEsports",
                        "route": "#",
                        "details": {
                            "duration": "5-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Time on site", "Brand recall", "Viral sharing"],
                            "how_it_works": "Collection of brain games and puzzles that reward players with discounts and perks.",
                            "tech_stack": ["Game Engine", "Reward System", "React"],
                        },
                    },
                ],
            },
            {
                "title": "Analytics & Insights",
                "icon": "ShowChart",
                "color": "#6b7280",
                "description": "Data-driven decisions with predictive analytics",
                "use_cases": [
                    {
                        "key": "forecast",
                        "label": "Sales Forecasting",
                        "description": "Predict future sales trends",
                        "icon": "ShowChart",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Better planning", "Inventory optimization", "Budget accuracy"],
                            "how_it_works": "Time series models analyze historical sales, seasonality, and external factors to forecast demand.",
                            "tech_stack": ["Prophet", "LSTM", "Time Series Analysis"],
                        },
                    },
                    {
                        "key": "timing",
                        "label": "Best Launch Timing",
                        "description": "Optimal product release schedule",
                        "icon": "CalendarMonth",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Maximum impact", "Avoid conflicts", "Trend alignment"],
                            "how_it_works": "Analyzes market trends, competitor activity, and seasonal patterns to recommend launch windows.",
                            "tech_stack": ["Trend Analysis", "Calendar Optimization", "Python"],
                        },
                    },
                    {
                        "key": "abtest",
                        "label": "A/B Test Analyzer",
                        "description": "Statistical experiment analysis",
                        "icon": "Science",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Data-driven decisions", "Statistical rigor", "Clear insights"],
                            "how_it_works": "Bayesian and frequentist analysis of A/B test results with confidence intervals and recommendations.",
                            "tech_stack": ["Bayesian Statistics", "Hypothesis Testing", "Python"],
                        },
                    },
                ],
            },
        ],
    },
    "entertainment": {
        "id": "entertainment",
        "name": "Entertainment AI",
        "tagline": "AI-powered media and entertainment",
        "description": "8 AI use cases for media and entertainment",
        "icon": "Movie",
        "primary_color": "#ef4444",
        "secondary_color": "#dc2626",
        "categories": [
            {
                "title": "Content",
                "icon": "Theaters",
                "color": "#ef4444",
                "description": "Intelligent content solutions",
                "use_cases": [
                    {
                        "key": "brand-placement",
                        "label": "AI-Driven Dynamic In-Video Brand Placement",
                        "description": "Ads that don't interrupt content — they become part of it",
                        "icon": "AutoFixHigh",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Non-interruptive", "Personalized per viewer", "Unlimited flexibility", "100% visibility"],
                            "how_it_works": "AI detects objects in video frames, tracks them across scenes, and seamlessly replaces brands while preserving lighting, motion, and realism. Same video, different brands per geography, audience, or campaign.",
                            "tech_stack": ["YOLOv8/DETR", "DeepSORT", "SAM", "Diffusion/GAN", "Optical Flow"],
                        },
                    },
                    {
                        "key": "content-recs",
                        "label": "Content Recommendation Intelligence",
                        "description": "Personalized content suggestions with explainable reasoning",
                        "icon": "Recommend",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Engagement", "Retention", "Discovery", "Explainable"],
                            "how_it_works": "Sequence models and embedding similarity create personalized recommendations with transparent reasoning (themes, moods, actors).",
                            "tech_stack": ["Transformers", "Embeddings", "Reinforcement Learning"],
                        },
                    },
                    {
                        "key": "content-moderation",
                        "label": "Content Moderation AI",
                        "description": "Safety without censorship drama",
                        "icon": "Security",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Brand safety", "Community trust", "Scalability"],
                            "how_it_works": "Vision transformers and context-aware NLP detect inappropriate content with timeline risk heatmaps for review.",
                            "tech_stack": ["Vision Transformers", "Audio Classifiers", "NLP"],
                        },
                    },
                ],
            },
            {
                "title": "Audience",
                "icon": "LiveTv",
                "color": "#6b7280",
                "description": "Understand and grow audiences",
                "use_cases": [
                    {
                        "key": "audience-analytics",
                        "label": "Audience Analytics Intelligence",
                        "description": "Audience Genome — Segments shown as evolving organisms",
                        "icon": "Sensors",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Programming decisions", "Advertising value", "Content strategy"],
                            "how_it_works": "K-Means clustering segments audiences based on viewing patterns, showing how segments evolve over time.",
                            "tech_stack": ["K-Means Clustering", "Behavioral Analytics", "Python"],
                        },
                    },
                    {
                        "key": "churn-prediction",
                        "label": "Subscriber Churn Prediction",
                        "description": "Exit Radar — Users shown moving toward churn zone",
                        "icon": "Subscriptions",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Retention", "Proactive engagement", "Revenue protection"],
                            "how_it_works": "Gradient boosting classifier predicts subscription cancellation probability with AI intervention suggestions.",
                            "tech_stack": ["Gradient Boosting", "Survival Analysis", "Python"],
                        },
                    },
                ],
            },
            {
                "title": "Monetization",
                "icon": "Campaign",
                "color": "#ef4444",
                "description": "Maximize revenue potential",
                "use_cases": [
                    {
                        "key": "ad-optimization",
                        "label": "Ad Optimization Intelligence",
                        "description": "Revenue Control Board — Shows ad yield per second of content",
                        "icon": "Campaign",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Advanced",
                            "benefits": ["Higher CPMs", "Better targeting", "User experience"],
                            "how_it_works": "ML models optimize ad placement, targeting, and bidding in real-time with revenue yield visualization.",
                            "tech_stack": ["Real-time Bidding", "CTR Prediction", "Python"],
                        },
                    },
                    {
                        "key": "music-discovery",
                        "label": "Music/Media Discovery AI",
                        "description": "Emotion Compass — Navigate by mood, not genre",
                        "icon": "MusicNote",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Engagement", "Artist discovery", "Personalization"],
                            "how_it_works": "Content-based filtering matches content by mood and emotion rather than traditional genre classification.",
                            "tech_stack": ["Audio Embeddings", "Mood Detection", "Content-Based Filtering"],
                        },
                    },
                ],
            },
        ],
    },
    "retail": {
        "id": "retail",
        "name": "Retail AI",
        "tagline": "In-store and omnichannel retail intelligence",
        "description": "8 AI use cases for modern retail",
        "icon": "Store",
        "primary_color": "#6b7280",
        "secondary_color": "#4b5563",
        "categories": [
            {
                "title": "In-Store",
                "icon": "Storefront",
                "color": "#6b7280",
                "description": "Transform the in-store experience",
                "use_cases": [
                    {
                        "key": "footfall-analysis",
                        "label": "In-Store Behavior Intelligence",
                        "description": "Footfall & Dwell Analysis — Understand where customers go and how long they stay",
                        "icon": "People",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Layout optimization", "Zone performance", "Customer journey insights"],
                            "how_it_works": "Computer vision tracks customer movements and behavior patterns to generate heatmaps and dwell time analysis.",
                            "tech_stack": ["Computer Vision (YOLOv8)", "DeepSORT Tracking", "Spatio-temporal Analysis"],
                        },
                    },
                    {
                        "key": "queue-intelligence",
                        "label": "Queue & Checkout Intelligence",
                        "description": "Wait Time Reduction — Predict queue buildup before it happens",
                        "icon": "Groups",
                        "route": "#",
                        "details": {
                            "duration": "6-8 min",
                            "difficulty": "Intermediate",
                            "benefits": ["30-40% wait time reduction", "Proactive staff allocation", "Customer satisfaction"],
                            "how_it_works": "ML predicts queue lengths and wait times 15-30 minutes ahead to optimize checkout staffing.",
                            "tech_stack": ["Time Series Forecasting", "Person Counting", "LSTM/Prophet"],
                        },
                    },
                ],
            },
            {
                "title": "Operations",
                "icon": "PointOfSale",
                "color": "#6b7280",
                "description": "Optimize retail operations",
                "use_cases": [
                    {
                        "key": "inventory-ai",
                        "label": "Inventory Intelligence",
                        "description": "Smart inventory management",
                        "icon": "ShoppingBasket",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Reduce stockouts", "Lower carrying costs", "Better turns"],
                            "how_it_works": "Demand forecasting and optimization models manage inventory across locations.",
                            "tech_stack": ["Demand Forecasting", "Optimization", "Python"],
                        },
                    },
                    {
                        "key": "loss-prevention",
                        "label": "Loss Prevention Intelligence",
                        "description": "Shrinkage Detection — Identify risk zones, not individuals",
                        "icon": "Security",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Advanced",
                            "benefits": ["Early detection", "Risk zone identification", "Reduced false positives"],
                            "how_it_works": "Action recognition and anomaly detection identify suspicious patterns in anonymized, zone-based data.",
                            "tech_stack": ["Anomaly Detection (Isolation Forest)", "Action Recognition (SlowFast/I3D)", "Multi-signal Correlation"],
                        },
                    },
                ],
            },
            {
                "title": "Customer",
                "icon": "Loyalty",
                "color": "#ef4444",
                "description": "Enhance customer relationships",
                "use_cases": [
                    {
                        "key": "customer-journey",
                        "label": "Customer Journey Mapping",
                        "description": "Understand omnichannel customer behavior",
                        "icon": "LocalMall",
                        "route": "#",
                        "details": {
                            "duration": "10-12 min",
                            "difficulty": "Advanced",
                            "benefits": ["Unified view", "Better targeting", "Experience optimization"],
                            "how_it_works": "ML unifies customer touchpoints to map and predict journey patterns.",
                            "tech_stack": ["Identity Resolution", "Journey Analytics", "Python"],
                        },
                    },
                    {
                        "key": "loyalty-optimization",
                        "label": "Loyalty Program Optimization",
                        "description": "Maximize loyalty program ROI",
                        "icon": "Loyalty",
                        "route": "#",
                        "details": {
                            "duration": "8-10 min",
                            "difficulty": "Intermediate",
                            "benefits": ["Higher redemption", "Better engagement", "Reduced costs"],
                            "how_it_works": "ML optimizes reward structures and personalized offers for maximum engagement.",
                            "tech_stack": ["Optimization", "Personalization", "Python"],
                        },
                    },
                ],
            },
        ],
    },
}


def seed_industries_and_use_cases(db: Session):
    """Seed industries and use cases from the data"""
    print("Starting content migration...")
    
    industries_created = 0
    categories_created = 0
    use_cases_created = 0
    themes_created = 0
    content_blocks_created = 0
    
    for industry_key, industry_data in INDUSTRIES_DATA.items():
        # Create or update industry
        industry = db.query(Industry).filter(Industry.industry_id == industry_key).first()
        if not industry:
            industry = Industry(
                industry_id=industry_key,
                name=industry_data["name"],
                icon=industry_data.get("icon", ""),
                description=industry_data.get("description", ""),
                is_active=True,  # Explicitly set is_active
            )
            db.add(industry)
            db.commit()
            db.refresh(industry)
            industries_created += 1
            print(f"  ✓ Created industry: {industry_data['name']}")
        else:
            # Update existing
            industry.name = industry_data["name"]
            industry.description = industry_data.get("description", "")
            industry.icon = industry_data.get("icon", "")
            # Ensure is_active is set if it was None
            if industry.is_active is None:
                industry.is_active = True
            db.commit()
            print(f"  ✓ Updated industry: {industry_data['name']}")
        
        # Create theme for industry
        theme = db.query(Theme).filter(
            Theme.scope == "industry",
            Theme.scope_id == industry_key
        ).first()
        
        if not theme:
            theme = Theme(
                theme_id=f"theme_{industry_key}",
                name=f"{industry_data['name']} Theme",
                scope="industry",
                scope_id=industry_key,
                primary_color=industry_data.get("primary_color"),
                secondary_color=industry_data.get("secondary_color"),
                description=industry_data.get("tagline", ""),
            )
            db.add(theme)
            db.commit()
            themes_created += 1
            print(f"    ✓ Created theme for {industry_data['name']}")
        
        # Create content blocks for industry
        content_block = db.query(ContentBlock).filter(
            ContentBlock.entity_type == "industry",
            ContentBlock.entity_id == industry_key,
            ContentBlock.block_type == "description"
        ).first()
        
        if not content_block:
            block = ContentBlock(
                block_id=f"block_{industry_key}_desc",
                content_type="text",
                entity_type="industry",
                entity_id=industry_key,
                block_type="description",
                block_key="main_description",
                title="Description",
                content=industry_data.get("description", ""),
                order_index=0,
                is_visible=True,
            )
            db.add(block)
            content_blocks_created += 1
        
        tagline_block = db.query(ContentBlock).filter(
            ContentBlock.entity_type == "industry",
            ContentBlock.entity_id == industry_key,
            ContentBlock.block_type == "tagline"
        ).first()
        
        if not tagline_block:
            block = ContentBlock(
                block_id=f"block_{industry_key}_tagline",
                content_type="text",
                entity_type="industry",
                entity_id=industry_key,
                block_type="tagline",
                block_key="main_tagline",
                title="Tagline",
                content=industry_data.get("tagline", ""),
                order_index=1,
                is_visible=True,
            )
            db.add(block)
            content_blocks_created += 1
        
        # Process categories and use cases
        for cat_idx, category_data in enumerate(industry_data.get("categories", [])):
            # Create category
            category_id = f"{industry_key}_{cat_idx}"
            category = db.query(UseCaseCategory).filter(
                UseCaseCategory.category_id == category_id
            ).first()
            
            if not category:
                category = UseCaseCategory(
                    category_id=category_id,
                    name=category_data["title"],
                    icon=category_data.get("icon", ""),
                    description=category_data.get("description", ""),
                    display_order=cat_idx,
                    is_active=True,
                )
                db.add(category)
                db.commit()
                db.refresh(category)
                categories_created += 1
            
            # Create use cases
            for uc_idx, use_case_data in enumerate(category_data.get("use_cases", [])):
                use_case_key = use_case_data["key"]
                use_case = db.query(UseCase).filter(
                    UseCase.use_case_id == use_case_key
                ).first()
                
                details = use_case_data.get("details", {})
                
                if not use_case:
                    use_case = UseCase(
                        use_case_id=use_case_key,
                        display_name=use_case_data["label"],
                        industry_id=industry_key,
                        category_id=category_id,
                        category=category_data["title"],
                        short_description=use_case_data.get("description", ""),
                        long_description=details.get("how_it_works", ""),
                        theory_content=details.get("how_it_works", ""),
                        icon=use_case_data.get("icon", ""),
                        keywords=details.get("tech_stack", []),
                        tips=details.get("benefits", []),
                        interactive_route=use_case_data.get("route", ""),
                        industry_route=f"/industries/{industry_key}",
                        is_active=True,
                        display_order=uc_idx,
                        meta_data={
                            "duration": details.get("duration", ""),
                            "difficulty": details.get("difficulty", ""),
                            "tech_stack": details.get("tech_stack", []),
                            "benefits": details.get("benefits", []),
                        },
                    )
                    db.add(use_case)
                    db.commit()
                    db.refresh(use_case)
                    use_cases_created += 1
                    print(f"    ✓ Created use case: {use_case_data['label']}")
                    
                    # Create content blocks for use case
                    content_blocks = [
                        {
                            "block_type": "description",
                            "block_key": "short_description",
                            "title": "Short Description",
                            "content": use_case_data.get("description", ""),
                            "order_index": 0,
                        },
                        {
                            "block_type": "theory",
                            "block_key": "how_it_works",
                            "title": "How It Works",
                            "content": details.get("how_it_works", ""),
                            "order_index": 1,
                        },
                    ]
                    
                    for cb_data in content_blocks:
                        existing = db.query(ContentBlock).filter(
                            ContentBlock.entity_type == "use_case",
                            ContentBlock.entity_id == use_case_key,
                            ContentBlock.block_key == cb_data["block_key"]
                        ).first()
                        
                        if not existing:
                            block = ContentBlock(
                                block_id=f"block_{use_case_key}_{cb_data['block_key']}",
                                content_type="markdown",
                                entity_type="use_case",
                                entity_id=use_case_key,
                                **cb_data
                            )
                            db.add(block)
                            content_blocks_created += 1
    
    db.commit()
    
    print(f"\n✅ Migration completed:")
    print(f"  - Industries: {industries_created} created")
    print(f"  - Categories: {categories_created} created")
    print(f"  - Use Cases: {use_cases_created} created")
    print(f"  - Themes: {themes_created} created")
    print(f"  - Content Blocks: {content_blocks_created} created")


def main():
    """Main function"""
    db = SessionLocal()
    try:
        seed_industries_and_use_cases(db)
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

