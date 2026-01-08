"""
Manufacturing API Routes
Industry 4.0 Decision Intelligence Platform
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas.manufacturing import (
    PredictiveMaintenanceRequest, PredictiveMaintenanceResponse,
    EnergyOptimizationRequest, EnergyOptimizationResponse,
    QualityVisionRequest, QualityVisionResponse,
    ProcessOptimizationRequest, ProcessOptimizationResponse,
    DemandPlanningRequest, DemandPlanningResponse,
    SupplyOptimizationRequest, SupplyOptimizationResponse,
    MachineHealth, FailureIndicator, CostLeakageIndicator, EnergyRecommendation,
    DefectDetail, InspectionSummary, ParameterImpact, ProcessRecommendation,
    ForecastWeek, SupplierInfo, BottleneckAlert, AlternativeSourcing,
)
from app.services.manufacturing_ml_service import manufacturing_ml_service

router = APIRouter(tags=["Manufacturing"])


@router.post("/predictive-maintenance", response_model=PredictiveMaintenanceResponse)
async def predictive_maintenance(request: PredictiveMaintenanceRequest):
    """
    Predictive Maintenance - Which machine is going to fail next — and when?
    
    Continuous sensor-based health monitoring with failure probability forecasting
    across 7/30/90 day horizons and remaining useful life estimation.
    """
    try:
        # Convert machines to dict format
        machines_data = [m.dict() for m in request.machines]
        
        # Predict maintenance
        machine_health_data = manufacturing_ml_service.predict_maintenance(
            machines_data,
            request.sub_industry
        )
        
        machine_health = []
        for mh in machine_health_data:
            indicators = [FailureIndicator(**i) for i in mh['top_indicators']]
            machine_health.append(MachineHealth(
                machine_id=mh['machine_id'],
                failure_probability_7d=mh['failure_probability_7d'],
                failure_probability_30d=mh['failure_probability_30d'],
                failure_probability_90d=mh['failure_probability_90d'],
                remaining_useful_life_days=mh['remaining_useful_life_days'],
                top_indicators=indicators,
                risk_level=mh['risk_level']
            ))
        
        return PredictiveMaintenanceResponse(
            machine_health=machine_health
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Predictive maintenance failed: {str(e)}")


@router.post("/energy-optimization", response_model=EnergyOptimizationResponse)
async def energy_optimization(request: EnergyOptimizationRequest):
    """
    Energy Optimization - Where are we wasting energy without knowing?
    
    Real-time energy pattern modeling with load vs output optimization
    and anomaly detection for energy waste identification.
    """
    try:
        # Analyze energy
        energy_analysis = manufacturing_ml_service.analyze_energy(
            request.sub_industry
        )
        
        cost_indicators = [CostLeakageIndicator(**c) for c in energy_analysis['cost_leakage_indicators']]
        recommendations = [EnergyRecommendation(**r) for r in energy_analysis['recommendations']]
        
        return EnergyOptimizationResponse(
            total_consumption=energy_analysis['total_consumption'],
            potential_savings=energy_analysis['potential_savings'],
            savings_percentage=energy_analysis['savings_percentage'],
            cost_leakage_indicators=cost_indicators,
            recommendations=recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Energy optimization failed: {str(e)}")


@router.post("/quality-vision", response_model=QualityVisionResponse)
async def quality_vision(request: QualityVisionRequest):
    """
    Visual Quality Inspection - Which products are defective — before shipping?
    
    Camera-based defect detection with 100% inspection and consistent judgment.
    Uses CNN (ResNet/EfficientNet) and object detection (YOLO/DETR) models.
    """
    try:
        # Perform quality inspection
        inspection_result = manufacturing_ml_service.inspect_quality(
            request.sub_industry
        )
        
        defects = [DefectDetail(**d) for d in inspection_result['defects']]
        summary = InspectionSummary(**inspection_result['summary'])
        
        return QualityVisionResponse(
            total_inspected=inspection_result['total_inspected'],
            defect_count=inspection_result['defect_count'],
            defect_rate=inspection_result['defect_rate'],
            defects=defects,
            summary=summary,
            confidence_score=inspection_result['confidence_score']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quality inspection failed: {str(e)}")


@router.post("/process-optimization", response_model=ProcessOptimizationResponse)
async def process_optimization(request: ProcessOptimizationRequest):
    """
    Process Optimization - Which parameters actually control yield?
    
    Parameter sensitivity modeling with yield vs input correlation analysis.
    Uses Bayesian optimization and SHAP feature importance.
    """
    try:
        # Optimize process
        optimization_result = manufacturing_ml_service.optimize_process(
            request.parameters.dict(),
            request.sub_industry
        )
        
        param_impacts = [ParameterImpact(**p) for p in optimization_result['parameter_impacts']]
        recommendations = [ProcessRecommendation(**r) for r in optimization_result['recommendations']]
        
        return ProcessOptimizationResponse(
            current_yield=optimization_result['current_yield'],
            optimal_yield=optimization_result['optimal_yield'],
            yield_improvement=optimization_result['yield_improvement'],
            parameter_impacts=param_impacts,
            recommendations=recommendations,
            confidence_score=optimization_result['confidence_score']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Process optimization failed: {str(e)}")


@router.post("/demand-planning", response_model=DemandPlanningResponse)
async def demand_planning(request: DemandPlanningRequest):
    """
    Demand Planning - How much should we produce next week/month?
    
    Multi-signal demand forecasting with Prophet/LSTM models.
    Provides confidence bands and scenario forecasting.
    """
    try:
        # Forecast demand
        forecast_result = manufacturing_ml_service.forecast_demand(
            request.sub_industry,
            request.time_horizon_weeks
        )
        
        forecast_weeks = [ForecastWeek(**f) for f in forecast_result['forecast_weeks']]
        
        return DemandPlanningResponse(
            forecast_weeks=forecast_weeks,
            conservative_plan=forecast_result['conservative_plan'],
            aggressive_plan=forecast_result['aggressive_plan'],
            stockout_risk=forecast_result['stockout_risk'],
            overstock_risk=forecast_result['overstock_risk'],
            confidence_score=forecast_result['confidence_score']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demand planning failed: {str(e)}")


@router.post("/supply-optimization", response_model=SupplyOptimizationResponse)
async def supply_optimization(request: SupplyOptimizationRequest):
    """
    Supply Chain Optimization - Where will delays or shortages hurt us most?
    
    Supplier risk scoring and logistics route optimization.
    Uses graph optimization and risk scoring models.
    """
    try:
        # Optimize supply chain
        supply_analysis = manufacturing_ml_service.optimize_supply_chain(
            request.sub_industry
        )
        
        suppliers = [SupplierInfo(**s) for s in supply_analysis['suppliers']]
        bottlenecks = [BottleneckAlert(**b) for b in supply_analysis['bottlenecks']]
        alternatives = [AlternativeSourcing(**a) for a in supply_analysis['alternative_sourcing']]
        
        return SupplyOptimizationResponse(
            suppliers=suppliers,
            bottlenecks=bottlenecks,
            alternative_sourcing=alternatives,
            overall_risk=supply_analysis['overall_risk']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supply chain optimization failed: {str(e)}")