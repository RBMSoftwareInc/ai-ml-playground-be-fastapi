"""
Staff Scheduling Intelligence Service
Optimizes staff scheduling using constraint satisfaction and demand forecasting
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class Shift:
    start_time: datetime
    end_time: datetime
    staff_count: int
    role: str


@dataclass
class ScheduleRisk:
    overload_periods: List[Tuple[datetime, datetime]]
    idle_periods: List[Tuple[datetime, datetime]]
    customer_impact_score: float
    burnout_risk: float


class StaffSchedulingService:
    """
    Staff Scheduling Intelligence
    
    Uses:
    - Constraint satisfaction for shift optimization
    - Demand forecasting integration
    - Workload simulation
    """
    
    def __init__(self):
        """Initialize staff scheduling service"""
        self.model_version = "1.0.0"
        
        # Staff roles and capabilities
        self.roles = {
            "kitchen": {"min_staff": 2, "max_staff": 8, "base_capacity": 4},  # orders per 15 min per staff
            "front": {"min_staff": 1, "max_staff": 4, "base_capacity": 6},
            "delivery": {"min_staff": 0, "max_staff": 5, "base_capacity": 3},
        }
    
    def simulate_schedule(
        self,
        shifts: List[Dict[str, Any]],
        demand_forecast: List[Dict[str, Any]],
        current_time: datetime
    ) -> Dict[str, Any]:
        """
        Simulate staff schedule and analyze risks
        
        Returns:
        - Overload risk periods
        - Idle time periods
        - Customer impact score
        - Burnout risk score
        """
        # Parse shifts
        schedule = self._parse_shifts(shifts)
        
        # Calculate capacity per time interval (15-min)
        intervals = self._calculate_capacity_intervals(schedule, current_time)
        
        # Match against demand forecast
        workload_analysis = self._analyze_workload(intervals, demand_forecast)
        
        # Calculate risks
        risks = self._calculate_risks(workload_analysis)
        
        # Calculate duration for each shift
        total_hours = 0
        for shift in schedule:
            duration = (shift.end_time - shift.start_time).total_seconds() / 3600
            total_hours += duration * shift.staff_count
        
        return {
            "schedule_summary": {
                "total_staff_hours": round(total_hours, 1),
                "peak_staff_count": max(i["total_staff"] for i in intervals) if intervals else 0,
                "low_staff_count": min(i["total_staff"] for i in intervals) if intervals else 0,
            },
            "workload_analysis": workload_analysis,
            "risks": risks,
            "recommendations": self._generate_recommendations(workload_analysis, risks),
        }
    
    def _parse_shifts(self, shifts: List[Dict[str, Any]]) -> List[Shift]:
        """Parse shift data into Shift objects"""
        parsed = []
        for shift in shifts:
            start = datetime.fromisoformat(shift["start_time"].replace('Z', '+00:00'))
            end = datetime.fromisoformat(shift["end_time"].replace('Z', '+00:00'))
            parsed.append(Shift(
                start_time=start,
                end_time=end,
                staff_count=shift["staff_count"],
                role=shift.get("role", "kitchen")
            ))
        return parsed
    
    def _calculate_capacity_intervals(self, shifts: List[Shift], start_time: datetime) -> List[Dict[str, Any]]:
        """Calculate staff capacity for each 15-minute interval"""
        intervals = []
        current = start_time
        
        # Generate 24 hours of intervals
        for _ in range(96):  # 24 hours * 4 intervals per hour
            interval_end = current + timedelta(minutes=15)
            
            # Count active staff in this interval
            active_staff = {"kitchen": 0, "front": 0, "delivery": 0}
            total_capacity = 0
            
            for shift in shifts:
                if current >= shift.start_time and interval_end <= shift.end_time:
                    role = shift.role
                    if role in active_staff:
                        active_staff[role] += shift.staff_count
                        # Calculate capacity (orders per 15 min)
                        capacity_per_staff = self.roles[role]["base_capacity"]
                        total_capacity += shift.staff_count * capacity_per_staff
            
            intervals.append({
                "timestamp": current,
                "end_timestamp": interval_end,
                "staff_by_role": active_staff,
                "total_staff": sum(active_staff.values()),
                "capacity_orders": total_capacity,
            })
            
            current = interval_end
        
        return intervals
    
    def _analyze_workload(
        self,
        intervals: List[Dict[str, Any]],
        demand_forecast: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze workload by matching capacity to demand"""
        workload = []
        
        # Create demand map by timestamp
        demand_map = {}
        for forecast in demand_forecast:
            forecast_time = datetime.fromisoformat(forecast["timestamp"].replace('Z', '+00:00'))
            demand_map[forecast_time] = forecast["predicted_orders"]
        
        for interval in intervals:
            demand = demand_map.get(interval["timestamp"], 0)
            capacity = interval["capacity_orders"]
            utilization = (demand / capacity * 100) if capacity > 0 else 0
            
            # Classify workload
            if utilization > 100:
                status = "overload"
                risk = min(100, utilization - 100)  # Risk from 0-100
            elif utilization > 80:
                status = "high"
                risk = (utilization - 80) / 20 * 50  # Risk from 0-50
            elif utilization > 40:
                status = "optimal"
                risk = 0
            else:
                status = "idle"
                risk = (40 - utilization) / 40 * 30  # Idle risk (waste)
            
            workload.append({
                **interval,
                "predicted_orders": demand,
                "utilization_percent": round(utilization, 1),
                "status": status,
                "risk_score": round(risk, 1),
                "gap": round(demand - capacity, 1),
            })
        
        return workload
    
    def _calculate_risks(self, workload: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall schedule risks"""
        overload_periods = []
        idle_periods = []
        total_overload_risk = 0
        total_idle_risk = 0
        customer_impact_sum = 0
        
        current_overload_start = None
        current_idle_start = None
        
        for period in workload:
            if period["status"] == "overload":
                if not current_overload_start:
                    current_overload_start = period["timestamp"]
                total_overload_risk += period["risk_score"]
                customer_impact_sum += max(0, period["gap"]) * 2  # Each order gap = 2 impact points
            else:
                if current_overload_start:
                    overload_periods.append((current_overload_start, period["timestamp"]))
                    current_overload_start = None
            
            if period["status"] == "idle":
                if not current_idle_start:
                    current_idle_start = period["timestamp"]
                total_idle_risk += period["risk_score"]
            else:
                if current_idle_start:
                    idle_periods.append((current_idle_start, period["timestamp"]))
                    current_idle_start = None
        
        # Finalize periods if still open
        if current_overload_start:
            overload_periods.append((current_overload_start, workload[-1]["timestamp"]))
        if current_idle_start:
            idle_periods.append((current_idle_start, workload[-1]["timestamp"]))
        
        # Calculate scores (0-100)
        burnout_risk = min(100, total_overload_risk / max(len(workload), 1) * 2)
        customer_impact = min(100, customer_impact_sum / max(len(workload), 1))
        efficiency_score = 100 - min(100, total_idle_risk / max(len(workload), 1) * 2)
        
        return {
            "overload_periods": [
                {"start": start.isoformat(), "end": end.isoformat()}
                for start, end in overload_periods
            ],
            "idle_periods": [
                {"start": start.isoformat(), "end": end.isoformat()}
                for start, end in idle_periods
            ],
            "burnout_risk": round(burnout_risk, 1),
            "customer_impact_score": round(customer_impact, 1),
            "efficiency_score": round(efficiency_score, 1),
        }
    
    def _generate_recommendations(
        self,
        workload: List[Dict[str, Any]],
        risks: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate scheduling recommendations"""
        recommendations = []
        
        # Overload recommendations
        if risks["overload_periods"]:
            peak_period = max(
                (p for p in workload if p["status"] == "overload"),
                key=lambda x: x["risk_score"],
                default=None
            )
            if peak_period:
                recommended_staff = int(np.ceil(peak_period["predicted_orders"] / self.roles["kitchen"]["base_capacity"]))
                recommendations.append({
                    "type": "increase_staff",
                    "period": peak_period["timestamp"].isoformat(),
                    "current_staff": peak_period["staff_by_role"].get("kitchen", 0),
                    "recommended_staff": recommended_staff,
                    "reasoning": f"Predicted {peak_period['predicted_orders']} orders but capacity only {peak_period['capacity_orders']}. Add {recommended_staff - peak_period['staff_by_role'].get('kitchen', 0)} staff.",
                    "priority": "high",
                })
        
        # Idle time recommendations
        if risks["idle_periods"]:
            idle_period = max(
                (p for p in workload if p["status"] == "idle"),
                key=lambda x: x["risk_score"],
                default=None
            )
            if idle_period:
                recommendations.append({
                    "type": "reduce_staff",
                    "period": idle_period["timestamp"].isoformat(),
                    "current_staff": idle_period["total_staff"],
                    "recommended_staff": max(1, int(idle_period["total_staff"] * 0.7)),
                    "reasoning": f"Low demand ({idle_period['predicted_orders']} orders) with excess capacity ({idle_period['capacity_orders']}). Reduce staff to cut costs.",
                    "priority": "medium",
                })
        
        # Burnout risk recommendation
        if risks["burnout_risk"] > 50:
            recommendations.append({
                "type": "balance_workload",
                "reasoning": f"High burnout risk ({risks['burnout_risk']:.1f}%) detected. Consider distributing peak workload across more staff or extending shifts.",
                "priority": "high",
            })
        
        return recommendations


# Global instance
staff_scheduling_service = StaffSchedulingService()

