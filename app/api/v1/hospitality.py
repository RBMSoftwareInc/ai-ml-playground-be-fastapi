"""
Hospitality & Restaurant API
AI-powered demand forecasting and kitchen workflow optimization
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import time

from app.services.restaurant_ml_service import restaurant_ml_service
from app.services.restaurant_data_generator import restaurant_data_generator
from app.services.menu_engineering_service import menu_engineering_service
from app.services.staff_scheduling_service import staff_scheduling_service

router = APIRouter(tags=["Hospitality & Restaurant"])


class DemandForecastRequest(BaseModel):
    """Request for demand forecasting"""
    start_time: Optional[str] = Field(None, description="Start time (ISO format). Defaults to current time")
    hours_ahead: int = Field(2, ge=1, le=4, description="Hours ahead to forecast (1-4)")
    interval_minutes: int = Field(15, description="Forecast interval in minutes")


class KitchenRecommendationsRequest(BaseModel):
    """Request for kitchen recommendations"""
    demand_forecast: DemandForecastRequest = Field(..., description="Demand forecast parameters")
    active_orders_count: int = Field(0, ge=0, description="Number of orders currently being prepared")
    staff_count: int = Field(4, ge=1, le=20, description="Number of kitchen staff")
    current_items: Optional[List[str]] = Field(None, description="List of items currently in prep")


class WhatIfScenarioRequest(BaseModel):
    """What-if scenario simulation"""
    recommendations: List[Dict[str, Any]] = Field(..., description="List of recommendations")
    accepted_recommendations: List[str] = Field(..., description="Titles of accepted recommendations")
    demand_forecast: Dict[str, Any] = Field(..., description="Demand forecast data")
    current_kitchen_state: Dict[str, Any] = Field(..., description="Current kitchen state")


@router.post("/demand-forecast", response_model=Dict[str, Any])
async def get_demand_forecast(request: DemandForecastRequest):
    """
    Get AI-powered demand forecast for restaurant operations
    
    Returns predicted order volume for next N hours in 15-minute intervals
    with confidence bands and cumulative order tracking.
    """
    try:
        # Parse start time
        if request.start_time:
            start_time = datetime.fromisoformat(request.start_time.replace('Z', '+00:00'))
        else:
            start_time = datetime.now()
        
        # Get demand forecast
        forecast_df = restaurant_ml_service.predict_demand_forecast(
            start_time=start_time,
            hours_ahead=request.hours_ahead,
            interval_minutes=request.interval_minutes
        )
        
        # Convert to dict format
        intervals = []
        for _, row in forecast_df.iterrows():
            intervals.append({
                "timestamp": row['timestamp'].isoformat(),
                "predicted_orders": int(row['predicted_orders']),
                "confidence_lower": int(row['confidence_lower']),
                "confidence_upper": int(row['confidence_upper']),
                "cumulative_orders": int(row['cumulative_orders']),
                "interval_index": int(row['interval_index']),
                "hour": int(row['hour']),
                "is_peak_hour": bool(row['is_peak_hour']),
            })
        
        return {
            "success": True,
            "forecast": {
                "start_time": start_time.isoformat(),
                "hours_ahead": request.hours_ahead,
                "interval_minutes": request.interval_minutes,
                "total_intervals": len(intervals),
                "total_predicted_orders": int(forecast_df['predicted_orders'].sum()),
                "peak_interval": intervals[max(range(len(intervals)), key=lambda i: intervals[i]['predicted_orders'])],
                "intervals": intervals,
            },
            "model_version": restaurant_ml_service.model_version,
            "generated_at": datetime.now().isoformat(),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating demand forecast: {str(e)}")


@router.post("/kitchen-recommendations", response_model=Dict[str, Any])
async def get_kitchen_recommendations(request: KitchenRecommendationsRequest):
    """
    Get AI recommendations for kitchen workflow optimization
    
    Analyzes demand forecast and current kitchen state to provide:
    - Prep action recommendations
    - Staffing adjustments
    - Workflow optimizations
    
    Each recommendation includes reasoning, confidence, and impact if ignored.
    """
    try:
        # Parse start time
        if request.demand_forecast.start_time:
            start_time = datetime.fromisoformat(request.demand_forecast.start_time.replace('Z', '+00:00'))
        else:
            start_time = datetime.now()
        
        # Get demand forecast
        forecast_df = restaurant_ml_service.predict_demand_forecast(
            start_time=start_time,
            hours_ahead=request.demand_forecast.hours_ahead,
            interval_minutes=request.demand_forecast.interval_minutes
        )
        
        # Generate kitchen state
        current_orders = []
        for i in range(request.active_orders_count):
            # Generate sample order data
            items = request.current_items or ["burger", "pizza"]
            current_orders.append({
                "items": items[:2] if len(items) >= 2 else items,
                "prep_time_required": 15,
            })
        
        kitchen_workflow = restaurant_data_generator.generate_kitchen_workflow_data(
            current_orders=current_orders,
            staff_count=request.staff_count
        )
        
        # Get recommendations
        recommendations = restaurant_ml_service.generate_kitchen_recommendations(
            demand_forecast=forecast_df,
            current_kitchen_state=kitchen_workflow,
            current_time=start_time
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "current_kitchen_state": kitchen_workflow,
            "model_version": restaurant_ml_service.model_version,
            "generated_at": datetime.now().isoformat(),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@router.post("/what-if-scenario", response_model=Dict[str, Any])
async def simulate_what_if_scenario(request: WhatIfScenarioRequest):
    """
    Simulate operational impact of accepting/ignoring AI recommendations
    
    Returns projected metrics:
    - Wait times (avg, max)
    - Order backlog
    - Customer satisfaction
    - Kitchen stress level
    - Food waste percentage
    """
    try:
        # Convert demand forecast dict back to DataFrame structure
        # (In production, would validate structure more carefully)
        
        # Reconstruct demand forecast DataFrame from dict if needed
        demand_forecast_df = None
        if request.demand_forecast and request.demand_forecast.get('intervals'):
            import pandas as pd
            intervals_data = request.demand_forecast['intervals']
            if intervals_data:
                df_data = []
                for interval in intervals_data:
                    df_data.append({
                        'timestamp': pd.to_datetime(interval['timestamp']),
                        'predicted_orders': interval['predicted_orders'],
                    })
                demand_forecast_df = pd.DataFrame(df_data)
        
        # Simulate scenario
        impact = restaurant_ml_service.simulate_what_if_scenario(
            recommendations=request.recommendations,
            accepted_recommendations=request.accepted_recommendations,
            demand_forecast=demand_forecast_df,
            current_kitchen_state=request.current_kitchen_state
        )
        
        return {
            "success": True,
            "scenario": {
                "accepted_recommendations_count": len(request.accepted_recommendations),
                "total_recommendations_count": len(request.recommendations),
                "operational_impact": impact,
            },
            "generated_at": datetime.now().isoformat(),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating scenario: {str(e)}")


@router.get("/conventional-vs-ai", response_model=Dict[str, Any])
async def get_conventional_vs_ai_comparison():
    """
    Get comparison metrics between conventional and AI-driven restaurant operations
    
    Returns tangible benefits:
    - Time saved
    - Waste reduced
    - Staff stress minimized
    """
    return {
        "success": True,
        "comparison": {
            "time_saved": {
                "metric": "Average order prep time",
                "conventional": "22 minutes",
                "ai_driven": "15 minutes",
                "improvement": "32% reduction",
                "reasoning": "AI pre-prep recommendations reduce wait times by anticipating demand spikes",
            },
            "waste_reduced": {
                "metric": "Food waste percentage",
                "conventional": "12%",
                "ai_driven": "6%",
                "improvement": "50% reduction",
                "reasoning": "Precise demand forecasting prevents over-preparation and reduces spoilage",
            },
            "staff_stress": {
                "metric": "Kitchen stress level",
                "conventional": "High (75-85)",
                "ai_driven": "Moderate (40-55)",
                "improvement": "40% reduction",
                "reasoning": "Proactive recommendations distribute workload and prevent rush periods",
            },
            "customer_satisfaction": {
                "metric": "Customer satisfaction score",
                "conventional": "72/100",
                "ai_driven": "88/100",
                "improvement": "22% increase",
                "reasoning": "Reduced wait times and consistent service quality improve experience",
            },
        },
    }


# ==================== MENU ENGINEERING INTELLIGENCE ====================

@router.get("/menu-engineering/analysis", response_model=Dict[str, Any])
async def get_menu_analysis():
    """
    Get menu engineering analysis for all items
    
    Returns menu items with margin, popularity, and profit analysis
    Categorized as: star, plowhorse, puzzle, dog
    """
    try:
        menu_analysis = menu_engineering_service.analyze_menu_items()
        
        return {
            "success": True,
            "menu_items": menu_analysis,
            "total_items": len(menu_analysis),
            "model_version": menu_engineering_service.model_version,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing menu: {str(e)}")


@router.get("/menu-engineering/item/{item_id}", response_model=Dict[str, Any])
async def get_menu_item_details(item_id: str):
    """
    Get detailed analysis for a specific menu item
    
    Returns:
    - Item statistics (margin, popularity, profit)
    - Bundle opportunities (association rules)
    - Pricing suggestions
    """
    try:
        details = menu_engineering_service.get_menu_item_details(item_id)
        
        if not details:
            raise HTTPException(status_code=404, detail=f"Menu item {item_id} not found")
        
        return {
            "success": True,
            "details": details,
            "model_version": menu_engineering_service.model_version,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting menu item details: {str(e)}")


# ==================== STAFF SCHEDULING INTELLIGENCE ====================

class StaffScheduleSimulationRequest(BaseModel):
    """Request for staff schedule simulation"""
    shifts: List[Dict[str, Any]] = Field(..., description="List of shifts with start_time, end_time, staff_count, role")
    demand_forecast: List[Dict[str, Any]] = Field(..., description="Demand forecast intervals")
    current_time: Optional[str] = Field(None, description="Current time (ISO format)")


@router.post("/staff-scheduling/simulate", response_model=Dict[str, Any])
async def simulate_staff_schedule(request: StaffScheduleSimulationRequest):
    """
    Simulate staff schedule and analyze workload, burnout risk, and customer impact
    
    Returns:
    - Workload analysis per interval
    - Overload and idle periods
    - Burnout risk score
    - Customer impact score
    - Scheduling recommendations
    """
    try:
        current_time = datetime.now()
        if request.current_time:
            current_time = datetime.fromisoformat(request.current_time.replace('Z', '+00:00'))
        
        result = staff_scheduling_service.simulate_schedule(
            shifts=request.shifts,
            demand_forecast=request.demand_forecast,
            current_time=current_time
        )
        
        return {
            "success": True,
            "simulation": result,
            "model_version": staff_scheduling_service.model_version,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating schedule: {str(e)}")
