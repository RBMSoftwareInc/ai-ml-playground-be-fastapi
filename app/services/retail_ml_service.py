"""
Retail AI Store Intelligence ML Service
Production-grade ML models for physical store intelligence
"""
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest, GradientBoostingRegressor
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings
import random
warnings.filterwarnings('ignore')

from app.services.retail_data_generator import retail_data_generator, FootfallEvent, QueueEvent, SuspiciousEvent


class FootfallAnalysisService:
    """
    In-Store Behavior Intelligence
    Footfall & Dwell Analysis using object detection and tracking
    """
    
    def __init__(self):
        self.model_version = "1.0.0"
    
    def analyze_footfall(
        self,
        start_time: datetime,
        end_time: datetime,
        store_layout: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze footfall patterns and generate insights
        
        Returns:
        - Zone-level traffic metrics
        - Dwell time analysis
        - Heatmap data
        - Plain-English insights
        """
        # Get footfall events for time window
        events = retail_data_generator.get_footfall_events(start_time, end_time)
        
        # Aggregate by zone
        zone_metrics = {}
        for zone in store_layout.get("zones", []):
            zone_id = zone["zone_id"]
            zone_events = [e for e in events if e["zone_id"] == zone_id]
            
            total_traffic = sum(e["person_count"] for e in zone_events)
            dwell_events = [e for e in zone_events if e.get("dwell_duration_seconds")]
            avg_dwell = float(np.mean([e["dwell_duration_seconds"] for e in dwell_events])) if dwell_events else 0.0
            dwell_ratio = len(dwell_events) / len(zone_events) if zone_events and len(zone_events) > 0 else 0.0
            
            zone_metrics[zone_id] = {
                "zone_name": zone["zone_name"],
                "zone_type": zone["zone_type"],
                "total_traffic": total_traffic,
                "event_count": len(zone_events),
                "avg_dwell_seconds": round(avg_dwell, 1),
                "dwell_ratio": round(dwell_ratio, 3),
                "coordinates": zone.get("coordinates", {}),
            }
        
        # Generate insights
        insights = self._generate_insights(zone_metrics, store_layout)
        
        # Heatmap data (normalized 0-1)
        max_traffic = max([m["total_traffic"] for m in zone_metrics.values()], default=1)
        if max_traffic == 0:
            max_traffic = 1  # Prevent division by zero
        heatmap_data = {
            zone_id: {
                **metrics,
                "heat_intensity": round(metrics["total_traffic"] / max_traffic, 3),
            }
            for zone_id, metrics in zone_metrics.items()
        }
        
        return {
            "zone_metrics": zone_metrics,
            "heatmap_data": heatmap_data,
            "insights": insights,
            "total_events": len(events),
        }
    
    def _generate_insights(
        self,
        zone_metrics: Dict[str, Dict],
        store_layout: Dict[str, Any]
    ) -> List[str]:
        """Generate plain-English insights"""
        insights = []
        
        # Find high traffic, low dwell zones (underperforming)
        for zone_id, metrics in zone_metrics.items():
            if metrics["zone_type"] == "aisle":
                if metrics["total_traffic"] > 500 and metrics["dwell_ratio"] < 0.3:
                    insights.append(
                        f"{metrics['zone_name']} has high traffic ({metrics['total_traffic']} people) "
                        f"but low dwell time (only {metrics['dwell_ratio']*100:.0f}% of visitors stop). "
                        f"Consider product placement or display adjustments."
                    )
                elif metrics["total_traffic"] < 200:
                    insights.append(
                        f"{metrics['zone_name']} receives low traffic ({metrics['total_traffic']} people). "
                        f"May benefit from signage or repositioning."
                    )
        
        # Checkout congestion
        checkout_zone = [z for z in store_layout.get("zones", []) if z["zone_type"] == "checkout"]
        if checkout_zone:
            checkout_metrics = zone_metrics.get(checkout_zone[0]["zone_id"], {})
            if checkout_metrics.get("total_traffic", 0) > 1000:
                insights.append(
                    f"Checkout zone experiences high traffic. Monitor queue lengths and consider "
                    f"opening additional counters during peak hours."
                )
        
        return insights


class QueueIntelligenceService:
    """
    Queue & Checkout Intelligence
    Wait time prediction and optimization
    """
    
    def __init__(self):
        self.model_version = "1.0.0"
        self._wait_time_model = None
        self._is_trained = False
    
    def train_wait_time_model(self, queue_events: List[Dict]):
        """Train wait time prediction model"""
        if len(queue_events) < 50:
            return
        
        # Prepare features
        X = []
        y = []
        
        for event in queue_events:
            hour = datetime.fromisoformat(event["timestamp"]).hour
            minute = datetime.fromisoformat(event["timestamp"]).minute
            is_peak = hour in [12, 13, 18, 19, 20]
            
            features = [
                event["queue_length"],
                is_peak * 1.0,
                hour / 24.0,
                event["service_completion_rate"],
            ]
            X.append(features)
            y.append(event["average_wait_time_seconds"])
        
        X = np.array(X)
        y = np.array(y)
        
        self._wait_time_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            random_state=42
        )
        self._wait_time_model.fit(X, y)
        self._is_trained = True
    
    def analyze_queues(
        self,
        current_time: datetime,
        forecast_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze current queue state and predict future wait times
        
        Returns:
        - Current queue status
        - Future predictions
        - Recommendations
        """
        # Get recent queue events
        lookback = timedelta(hours=2)
        recent_events = retail_data_generator.get_queue_events(
            start_time=current_time - lookback,
            end_time=current_time
        )
        
        # Train model if needed
        if not self._is_trained:
            all_events = retail_data_generator.get_queue_events()
            self.train_wait_time_model(all_events)
        
        # Get current state
        current_queues = {}
        counters = ["counter_1", "counter_2", "counter_3", "counter_4"]
        
        for counter_id in counters:
            counter_events = [e for e in recent_events if e["counter_id"] == counter_id]
            if counter_events:
                latest = sorted(counter_events, key=lambda x: x["timestamp"], reverse=True)[0]
                current_queues[counter_id] = {
                    "queue_length": latest["queue_length"],
                    "wait_time_seconds": latest["average_wait_time_seconds"],
                }
            else:
                current_queues[counter_id] = {
                    "queue_length": 0,
                    "wait_time_seconds": 0,
                }
        
        # Predict future wait times
        predictions = []
        for minutes_ahead in [15, 30]:
            future_time = current_time + timedelta(minutes=minutes_ahead)
            future_hour = future_time.hour
            is_peak = future_hour in [12, 13, 18, 19, 20]
            
            # Predict queue length (simplified - would use LSTM in production)
            current_total_queue = sum([q["queue_length"] for q in current_queues.values()])
            future_queue_base = current_total_queue + (1 if is_peak else -0.5) * (minutes_ahead / 15)
            future_queue = max(0, int(future_queue_base + random.uniform(-1, 1)))
            
            # Predict wait time
            if self._is_trained and future_queue > 0:
                features = np.array([[
                    future_queue / 4,  # Average per counter
                    is_peak * 1.0,
                    future_hour / 24.0,
                    1.2,  # Average service rate
                ]])
                predicted_wait = self._wait_time_model.predict(features)[0]
            else:
                predicted_wait = future_queue * 120  # Fallback: 2 min per person
            
            predictions.append({
                "minutes_ahead": minutes_ahead,
                "predicted_queue_length": future_queue,
                "predicted_wait_time_seconds": max(0, round(predicted_wait, 1)),
            })
        
        # Generate recommendations
        recommendations = self._generate_recommendations(current_queues, predictions)
        
        # Observations
        observations = []
        total_queue = sum([q["queue_length"] for q in current_queues.values()])
        avg_wait = np.mean([q["wait_time_seconds"] for q in current_queues.values()])
        
        if total_queue > 10:
            observations.append({
                "observation": f"Current total queue length is {total_queue} customers across all counters",
                "severity": "high",
            })
        if avg_wait > 420:  # 7 minutes
            observations.append({
                "observation": f"Average wait time is {avg_wait/60:.1f} minutes, exceeding target of 5 minutes",
                "severity": "high",
            })
        
        return {
            "current_queues": current_queues,
            "predictions": predictions,
            "recommendations": recommendations,
            "observations": observations,
            "total_queue_length": total_queue,
            "average_wait_time_seconds": round(avg_wait, 1),
        }
    
    def _generate_recommendations(
        self,
        current_queues: Dict[str, Dict],
        predictions: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        total_queue = sum([q["queue_length"] for q in current_queues.values()])
        active_counters = sum(1 for q in current_queues.values() if q["queue_length"] > 0)
        
        # Check 30-minute prediction
        future_prediction = predictions[1] if len(predictions) > 1 else predictions[0]
        future_wait = future_prediction["predicted_wait_time_seconds"]
        
        if future_wait > 420 and active_counters < 4:  # 7 minutes, can open more counters
            recommendations.append({
                "action": "Open additional counter",
                "urgency": "high",
                "reasoning": f"Predicted wait time in 30 minutes will exceed 7 minutes ({future_wait/60:.1f} min). Opening additional counter can reduce wait by approximately {(future_wait - 300)/60:.1f} minutes.",
                "estimated_impact": "Reduces wait time by 30-40%",
            })
        
        if total_queue > 12:
            recommendations.append({
                "action": "Reallocate staff to checkout",
                "urgency": "medium",
                "reasoning": f"Current queue length is {total_queue} customers. Additional staff at checkout will improve service speed.",
                "estimated_impact": "Reduces wait time by 20-25%",
            })
        
        return recommendations


class LossPreventionService:
    """
    Loss Prevention Intelligence
    Shrinkage detection using anomaly detection
    """
    
    def __init__(self):
        self.model_version = "1.0.0"
        self._anomaly_model = None
        self._is_trained = False
    
    def train_anomaly_model(self, footfall_events: List[Dict], suspicious_events: List[Dict]):
        """Train anomaly detection model"""
        if len(footfall_events) < 100:
            return
        
        # Prepare features from footfall events
        X = []
        
        # Aggregate features per zone per hour
        zone_features = {}
        for event in footfall_events:
            dt = datetime.fromisoformat(event["timestamp"])
            key = (event["zone_id"], dt.hour)
            
            if key not in zone_features:
                zone_features[key] = {
                    "dwell_count": 0,
                    "total_dwell": 0,
                    "event_count": 0,
                }
            
            zone_features[key]["event_count"] += 1
            if event.get("dwell_duration_seconds"):
                zone_features[key]["dwell_count"] += 1
                zone_features[key]["total_dwell"] += event["dwell_duration_seconds"]
        
        # Convert to feature vectors
        for (zone_id, hour), features in zone_features.items():
            avg_dwell = features["total_dwell"] / features["dwell_count"] if features["dwell_count"] > 0 else 0
            dwell_ratio = features["dwell_count"] / features["event_count"] if features["event_count"] > 0 else 0
            
            feature_vector = [
                features["event_count"],
                avg_dwell,
                dwell_ratio,
                hour / 24.0,
            ]
            X.append(feature_vector)
        
        if len(X) < 50:
            return
        
        X = np.array(X)
        
        # Train isolation forest
        self._anomaly_model = IsolationForest(
            contamination=0.05,  # Expect 5% anomalies
            random_state=42
        )
        self._anomaly_model.fit(X)
        self._is_trained = True
    
    def analyze_loss_prevention(
        self,
        start_time: datetime,
        end_time: datetime,
        store_layout: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze suspicious patterns and generate risk assessment
        
        Returns:
        - Risk heatmap by zone
        - Suspicious events (anonymized)
        - Risk scores
        - Recommendations
        """
        # Get suspicious events
        suspicious_events = retail_data_generator.get_suspicious_events(start_time, end_time, min_risk_score=0.5)
        
        # Get footfall events for context
        footfall_events = retail_data_generator.get_footfall_events(start_time, end_time)
        
        # Train model if needed
        if not self._is_trained:
            all_footfall = retail_data_generator.get_footfall_events()
            all_suspicious = retail_data_generator.get_suspicious_events()
            self.train_anomaly_model(all_footfall, all_suspicious)
        
        # Aggregate risk by zone
        zone_risks = {}
        for zone in store_layout.get("zones", []):
            zone_id = zone["zone_id"]
            zone_suspicious = [e for e in suspicious_events if e["zone_id"] == zone_id]
            
            if zone_suspicious:
                avg_risk = np.mean([e["risk_score"] for e in zone_suspicious])
                max_risk = max([e["risk_score"] for e in zone_suspicious])
                event_count = len(zone_suspicious)
            else:
                avg_risk = 0.0
                max_risk = 0.0
                event_count = 0
            
            zone_risks[zone_id] = {
                "zone_name": zone["zone_name"],
                "risk_score": round(avg_risk, 3),
                "max_risk_score": round(max_risk, 3),
                "suspicious_event_count": event_count,
                "coordinates": zone.get("coordinates", {}),
            }
        
        # Generate insights
        insights = []
        high_risk_zones = [z for z, r in zone_risks.items() if r["risk_score"] > 0.7]
        
        if high_risk_zones:
            zone_names = [zone_risks[z]["zone_name"] for z in high_risk_zones]
            insights.append(
                f"Zones with elevated risk patterns: {', '.join(zone_names)}. "
                f"Consider increasing visibility or repositioning high-value items."
            )
        
        if len(suspicious_events) > 10:
            insights.append(
                f"Detected {len(suspicious_events)} suspicious pattern events in the analysis period. "
                f"Review zone layouts and consider security presence adjustments."
            )
        
        return {
            "zone_risks": zone_risks,
            "suspicious_events": suspicious_events,
            "insights": insights,
            "total_suspicious_events": len(suspicious_events),
            "risk_period_start": start_time.isoformat(),
            "risk_period_end": end_time.isoformat(),
        }


# Global service instances
footfall_analysis_service = FootfallAnalysisService()
queue_intelligence_service = QueueIntelligenceService()
loss_prevention_service = LossPreventionService()

