"""
Manufacturing ML Service
ML models and predictions for Manufacturing AI
"""
import numpy as np
from typing import Dict, Any, List, Tuple
import random


class ManufacturingMLService:
    """ML service for Manufacturing predictions"""
    
    def predict_maintenance(
        self,
        machines: List[Dict[str, Any]],
        sub_industry: str
    ) -> List[Dict[str, Any]]:
        """
        Predict machine failure probability and RUL
        
        Returns list of machine health predictions
        """
        machine_health = []
        
        for machine in machines:
            hours = machine.get('hours_operation', 10000)
            
            # Calculate base failure probability based on hours
            base_risk = min(0.8, hours / 20000.0)
            
            # Sub-industry adjustments
            if sub_industry == 'electronics':
                base_risk *= 0.7  # Electronics equipment typically more reliable
            elif sub_industry == 'process':
                base_risk *= 1.2  # Process equipment under harsher conditions
            
            # Generate failure probabilities for different time horizons
            failure_7d = min(0.95, base_risk * 0.25 + random.uniform(-0.05, 0.05))
            failure_30d = min(0.95, base_risk * 0.65 + random.uniform(-0.1, 0.1))
            failure_90d = min(0.95, base_risk + random.uniform(-0.15, 0.15))
            
            # Calculate remaining useful life
            rul_days = max(7, int((1 - base_risk) * 180) + random.randint(-30, 30))
            
            # Determine risk level
            if failure_30d > 0.5:
                risk_level = 'high'
            elif failure_30d > 0.3:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            # Generate top indicators
            indicators = [
                {
                    'indicator': 'Bearing Wear' if sub_industry != 'electronics' else 'Component Degradation',
                    'severity': 'high' if failure_30d > 0.4 else 'medium',
                    'contribution': 0.45
                },
                {
                    'indicator': 'Temperature Anomaly',
                    'severity': 'medium',
                    'contribution': 0.32
                },
                {
                    'indicator': 'Vibration Spike' if sub_industry != 'electronics' else 'Signal Drift',
                    'severity': 'high' if failure_30d > 0.5 else 'medium',
                    'contribution': 0.23
                }
            ]
            
            machine_health.append({
                'machine_id': machine['id'],
                'failure_probability_7d': max(0.0, min(1.0, failure_7d)),
                'failure_probability_30d': max(0.0, min(1.0, failure_30d)),
                'failure_probability_90d': max(0.0, min(1.0, failure_90d)),
                'remaining_useful_life_days': rul_days,
                'top_indicators': indicators,
                'risk_level': risk_level
            })
        
        return machine_health
    
    def analyze_energy(
        self,
        sub_industry: str
    ) -> Dict[str, Any]:
        """
        Analyze energy consumption and identify waste
        
        Returns energy analysis with recommendations
        """
        # Base consumption varies by sub-industry
        base_consumption = {
            'automotive': 450000,
            'electronics': 320000,
            'process': 580000
        }
        
        total_consumption = base_consumption.get(sub_industry, 450000)
        
        # Calculate potential savings (10-25% range)
        savings_pct = 0.15 + random.uniform(-0.05, 0.10)
        potential_savings = total_consumption * savings_pct
        
        # Generate cost leakage indicators
        zones = {
            'automotive': ['Production Line 1', 'HVAC System', 'Compressed Air', 'Lighting'],
            'electronics': ['Clean Room HVAC', 'Production Equipment', 'Compressed Air', 'Lighting'],
            'process': ['Reactor Systems', 'Distillation', 'Pumping Systems', 'HVAC']
        }
        
        zone_names = zones.get(sub_industry, zones['automotive'])
        
        cost_leakage = []
        total_waste = 0
        for i, zone in enumerate(zone_names):
            waste = potential_savings * (0.3 - i * 0.08) + random.uniform(-2000, 2000)
            total_waste += max(0, waste)
            cost_leakage.append({
                'zone': zone,
                'waste_kwh': max(0, waste),
                'severity': 'high' if waste > 15000 else 'medium' if waste > 8000 else 'low',
                'recommendation': f'Optimize {zone.lower()} during idle periods'
            })
        
        # Adjust to match total savings
        if total_waste > 0:
            scale_factor = potential_savings / total_waste
            for item in cost_leakage:
                item['waste_kwh'] *= scale_factor
        
        # Generate recommendations
        recommendations = [
            {
                'action': f'Shut down {zone_names[0]} during 3rd shift',
                'savings_kwh': cost_leakage[0]['waste_kwh'],
                'priority': 'high'
            },
            {
                'action': 'Reduce HVAC temperature by 2°C',
                'savings_kwh': cost_leakage[1]['waste_kwh'] * 0.7,
                'priority': 'medium'
            },
            {
                'action': 'Schedule compressed air maintenance',
                'savings_kwh': cost_leakage[2]['waste_kwh'] if len(cost_leakage) > 2 else 5000,
                'priority': 'medium'
            }
        ]
        
        return {
            'total_consumption': total_consumption,
            'potential_savings': potential_savings,
            'savings_percentage': savings_pct,
            'cost_leakage_indicators': cost_leakage,
            'recommendations': recommendations
        }
    
    def inspect_quality(
        self,
        sub_industry: str
    ) -> Dict[str, Any]:
        """
        Perform visual quality inspection
        
        Returns inspection results with defects
        """
        # Base defect rates vary by industry
        base_defect_rates = {
            'automotive': 0.038,
            'electronics': 0.025,
            'process': 0.042
        }
        
        defect_rate = base_defect_rates.get(sub_industry, 0.035)
        total_inspected = 1250
        defect_count = int(total_inspected * defect_rate)
        
        # Generate defect details
        defect_types = {
            'automotive': ['Surface Scratch', 'Misalignment', 'Paint Defect', 'Weld Issue'],
            'electronics': ['Solder Bridge', 'Component Misplacement', 'Contamination', 'Crack'],
            'process': ['Package Leak', 'Label Misalignment', 'Contamination', 'Fill Level']
        }
        
        types = defect_types.get(sub_industry, defect_types['automotive'])
        
        defects = []
        for i in range(min(defect_count, 5)):  # Show top 5 defects
            defects.append({
                'id': i + 1,
                'type': types[i % len(types)],
                'severity': random.choice(['high', 'medium', 'low']),
                'confidence': 0.85 + random.uniform(-0.1, 0.1),
                'bounding_box': [
                    random.randint(100, 400),
                    random.randint(80, 300),
                    random.randint(450, 600),
                    random.randint(350, 500)
                ],
                'explanation': f'{types[i % len(types)]} detected on component surface'
            })
        
        passed = total_inspected - defect_count
        review = int(defect_count * 0.25)
        rejected = defect_count - review
        
        return {
            'total_inspected': total_inspected,
            'defect_count': defect_count,
            'defect_rate': defect_rate,
            'defects': defects,
            'summary': {
                'passed': passed,
                'rejected': rejected,
                'review': review
            },
            'confidence_score': 0.89
        }
    
    def optimize_process(
        self,
        parameters: Dict[str, Any],
        sub_industry: str
    ) -> Dict[str, Any]:
        """
        Optimize process parameters for yield
        
        Returns optimization recommendations
        """
        temp = parameters.get('temperature', 185)
        pressure = parameters.get('pressure', 45)
        speed = parameters.get('speed', 75)
        
        # Calculate current yield (simplified)
        temp_optimal = 190 if sub_industry == 'automotive' else 185
        pressure_optimal = 48 if sub_industry == 'automotive' else 45
        speed_optimal = 78 if sub_industry == 'automotive' else 75
        
        temp_deviation = abs(temp - temp_optimal) / temp_optimal
        pressure_deviation = abs(pressure - pressure_optimal) / pressure_optimal
        speed_deviation = abs(speed - speed_optimal) / speed_optimal
        
        current_yield = 0.95 - (temp_deviation * 0.05) - (pressure_deviation * 0.03) - (speed_deviation * 0.02)
        current_yield = max(0.75, min(0.98, current_yield))
        
        optimal_yield = 0.94
        yield_improvement = max(0, optimal_yield - current_yield)
        
        # Parameter impacts
        parameter_impacts = [
            {
                'parameter': 'Temperature',
                'impact': 0.35,
                'optimal_value': temp_optimal,
                'safe_range': [temp_optimal - 15, temp_optimal + 5],
                'current_value': temp
            },
            {
                'parameter': 'Pressure',
                'impact': 0.28,
                'optimal_value': pressure_optimal,
                'safe_range': [pressure_optimal - 8, pressure_optimal + 10],
                'current_value': pressure
            },
            {
                'parameter': 'Speed',
                'impact': 0.22,
                'optimal_value': speed_optimal,
                'safe_range': [speed_optimal - 10, speed_optimal + 10],
                'current_value': speed
            }
        ]
        
        # Recommendations
        recommendations = []
        if temp < temp_optimal:
            recommendations.append({
                'parameter': 'Temperature',
                'change': temp_optimal - temp,
                'direction': 'increase',
                'impact': f'Yield improvement: +{(abs(temp - temp_optimal) / temp_optimal * 0.35 * 100):.1f}%'
            })
        if pressure < pressure_optimal:
            recommendations.append({
                'parameter': 'Pressure',
                'change': pressure_optimal - pressure,
                'direction': 'increase',
                'impact': f'Yield improvement: +{(abs(pressure - pressure_optimal) / pressure_optimal * 0.28 * 100):.1f}%'
            })
        if speed < speed_optimal:
            recommendations.append({
                'parameter': 'Speed',
                'change': speed_optimal - speed,
                'direction': 'increase',
                'impact': f'Yield improvement: +{(abs(speed - speed_optimal) / speed_optimal * 0.22 * 100):.1f}%'
            })
        
        return {
            'current_yield': current_yield,
            'optimal_yield': optimal_yield,
            'yield_improvement': yield_improvement,
            'parameter_impacts': parameter_impacts,
            'recommendations': recommendations,
            'confidence_score': 0.85
        }
    
    def forecast_demand(
        self,
        sub_industry: str,
        time_horizon_weeks: int
    ) -> Dict[str, Any]:
        """
        Forecast demand for production planning
        
        Returns demand forecast with confidence bands
        """
        # Base demand varies by sub-industry
        base_demands = {
            'automotive': 4800,
            'electronics': 12000,
            'process': 8500
        }
        
        base_demand = base_demands.get(sub_industry, 4800)
        
        # Generate weekly forecasts
        forecast_weeks = []
        for week in range(1, time_horizon_weeks + 1):
            # Simulate trend with some seasonality
            trend_factor = 1.0 - (week - 1) * 0.01
            seasonal_factor = 1.0 + 0.05 * np.sin(week * np.pi / 8)
            
            demand_mid = base_demand * trend_factor * seasonal_factor
            demand_low = demand_mid * (1 - 0.08)
            demand_high = demand_mid * (1 + 0.12)
            confidence = max(0.7, 0.85 - (week - 1) * 0.02)
            
            forecast_weeks.append({
                'week': week,
                'demand_low': int(demand_low),
                'demand_mid': int(demand_mid),
                'demand_high': int(demand_high),
                'confidence': confidence
            })
        
        # Calculate production plans
        avg_demand = np.mean([w['demand_mid'] for w in forecast_weeks])
        conservative_plan = int(avg_demand * 0.97)
        aggressive_plan = int(avg_demand * 1.03)
        
        # Risk assessment
        stockout_risk = 0.12 + random.uniform(-0.05, 0.05)
        overstock_risk = 0.28 + random.uniform(-0.05, 0.05)
        
        return {
            'forecast_weeks': forecast_weeks,
            'conservative_plan': conservative_plan,
            'aggressive_plan': aggressive_plan,
            'stockout_risk': max(0.0, min(1.0, stockout_risk)),
            'overstock_risk': max(0.0, min(1.0, overstock_risk)),
            'confidence_score': 0.82
        }
    
    def optimize_supply_chain(
        self,
        sub_industry: str
    ) -> Dict[str, Any]:
        """
        Analyze supply chain and identify risks/bottlenecks
        
        Returns supply chain analysis with alternatives
        """
        # Generate supplier profiles
        suppliers = []
        
        supplier_configs = {
            'automotive': [
                {'name': 'Supplier A - Raw Materials', 'location': 'China', 'lead_time': 45, 'base_risk': 0.32},
                {'name': 'Supplier B - Components', 'location': 'Mexico', 'lead_time': 28, 'base_risk': 0.58},
                {'name': 'Supplier C - Electronics', 'location': 'Taiwan', 'lead_time': 60, 'base_risk': 0.75},
            ],
            'electronics': [
                {'name': 'Supplier A - Silicon Wafers', 'location': 'Taiwan', 'lead_time': 90, 'base_risk': 0.65},
                {'name': 'Supplier B - Components', 'location': 'China', 'lead_time': 35, 'base_risk': 0.48},
                {'name': 'Supplier C - Packaging', 'location': 'Malaysia', 'lead_time': 42, 'base_risk': 0.55},
            ],
            'process': [
                {'name': 'Supplier A - Raw Chemicals', 'location': 'USA', 'lead_time': 30, 'base_risk': 0.35},
                {'name': 'Supplier B - Packaging', 'location': 'China', 'lead_time': 50, 'base_risk': 0.62},
                {'name': 'Supplier C - Specialty', 'location': 'Germany', 'lead_time': 55, 'base_risk': 0.52},
            ]
        }
        
        configs = supplier_configs.get(sub_industry, supplier_configs['automotive'])
        
        for i, config in enumerate(configs):
            risk_score = config['base_risk'] + random.uniform(-0.1, 0.1)
            performance = 1.0 - risk_score + random.uniform(-0.1, 0.1)
            
            if risk_score > 0.6:
                risk_level = 'high'
            elif risk_score > 0.4:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            suppliers.append({
                'id': i + 1,
                'name': config['name'],
                'risk_score': max(0.0, min(1.0, risk_score)),
                'performance_score': max(0.0, min(1.0, performance)),
                'location': config['location'],
                'lead_time_days': config['lead_time'],
                'risk_level': risk_level
            })
        
        # Identify bottlenecks
        bottlenecks = []
        if suppliers[0]['risk_score'] > 0.4:
            bottlenecks.append({
                'component': 'Raw Materials' if sub_industry == 'automotive' else 'Silicon Wafers' if sub_industry == 'electronics' else 'Raw Chemicals',
                'impact': 'high',
                'supplier': suppliers[0]['name'],
                'delay_risk': suppliers[0]['risk_score'] * 0.9,
                'alternative_available': True
            })
        if suppliers[2]['risk_score'] > 0.6:
            bottlenecks.append({
                'component': 'Electronics' if sub_industry == 'automotive' else 'Packaging' if sub_industry == 'electronics' else 'Specialty',
                'impact': 'critical',
                'supplier': suppliers[2]['name'],
                'delay_risk': suppliers[2]['risk_score'],
                'alternative_available': False
            })
        
        # Alternative sourcing
        alternative_sourcing = []
        if bottlenecks and bottlenecks[0]['alternative_available']:
            alternative_sourcing.append({
                'component': bottlenecks[0]['component'],
                'current_supplier': bottlenecks[0]['supplier'],
                'alternative': f'Supplier D - {bottlenecks[0]["component"]} (USA)',
                'lead_time_improvement': -10,
                'cost_delta': 0.05
            })
        
        overall_risk = np.mean([s['risk_score'] for s in suppliers])
        
        return {
            'suppliers': suppliers,
            'bottlenecks': bottlenecks,
            'alternative_sourcing': alternative_sourcing,
            'overall_risk': overall_risk
        }


# Global instance
manufacturing_ml_service = ManufacturingMLService()
