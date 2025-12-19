"""
General ML Service for classification, regression, and recommendation
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle
import os
from app.core.config import settings


class MLService:
    """General machine learning service"""
    
    def __init__(self):
        """Initialize ML service"""
        self.models_dir = settings.MODELS_DIR
        os.makedirs(self.models_dir, exist_ok=True)
        self.loaded_models = {}
    
    def predict_fraud(
        self,
        transaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict if transaction is fraudulent
        
        Args:
            transaction_data: Transaction features
            
        Returns:
            Fraud prediction with risk score
        """
        # Extract features
        amount = transaction_data.get("amount", 0)
        device_fingerprint = transaction_data.get("device_fingerprint", "")
        ip_address = transaction_data.get("ip_address", "")
        
        # Simple rule-based fraud detection (can be replaced with trained model)
        risk_score = 0.0
        reasons = []
        
        # High amount check
        if amount > 50000:
            risk_score += 0.3
            reasons.append("High transaction amount")
        
        # Device fingerprint check (simplified)
        if not device_fingerprint or len(device_fingerprint) < 10:
            risk_score += 0.2
            reasons.append("Suspicious device fingerprint")
        
        # IP address check (simplified)
        if ip_address:
            # Check for known suspicious patterns
            if ip_address.startswith("192.168") and amount > 10000:
                risk_score += 0.15
                reasons.append("Internal IP with high amount")
        
        # Location mismatch (if provided)
        if transaction_data.get("location_mismatch"):
            risk_score += 0.25
            reasons.append("Location mismatch detected")
        
        # Velocity check (if provided)
        if transaction_data.get("transactions_last_hour", 0) > 10:
            risk_score += 0.3
            reasons.append("High transaction velocity")
        
        is_fraud = risk_score > 0.5
        
        return {
            "is_fraud": is_fraud,
            "risk_score": min(1.0, risk_score),
            "reasons": reasons,
            "confidence": 0.85
        }
    
    def predict_churn(
        self,
        customer_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict customer churn probability
        
        Args:
            customer_data: Customer features
            
        Returns:
            Churn prediction
        """
        # Extract features
        days_since_last_purchase = customer_data.get("days_since_last_purchase", 0)
        total_orders = customer_data.get("total_orders", 0)
        total_spent = customer_data.get("total_spent", 0)
        avg_order_value = customer_data.get("average_order_value", 0)
        
        # Simple churn prediction model
        churn_probability = 0.0
        
        # Days since last purchase
        if days_since_last_purchase > 90:
            churn_probability += 0.4
        elif days_since_last_purchase > 60:
            churn_probability += 0.25
        elif days_since_last_purchase > 30:
            churn_probability += 0.1
        
        # Low engagement
        if total_orders < 3:
            churn_probability += 0.2
        
        # Low spending
        if total_spent < 1000:
            churn_probability += 0.15
        
        # Determine risk level
        if churn_probability > 0.6:
            risk_level = "high"
        elif churn_probability > 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        recommendations = []
        if risk_level == "high":
            recommendations.append("Send retention email with special offer")
            recommendations.append("Personalized discount code")
        elif risk_level == "medium":
            recommendations.append("Engage with product recommendations")
        
        return {
            "churn_probability": min(1.0, churn_probability),
            "risk_level": risk_level,
            "recommendations": recommendations
        }
    
    def segment_customers(
        self,
        customer_data: List[Dict[str, Any]],
        num_segments: int = 5
    ) -> Dict[str, Any]:
        """
        Segment customers using clustering
        
        Args:
            customer_data: List of customer features
            num_segments: Number of segments to create
            
        Returns:
            Customer segments
        """
        if not customer_data:
            return {"segments": []}
        
        # Extract features for clustering
        features = []
        for customer in customer_data:
            features.append([
                customer.get("total_orders", 0),
                customer.get("total_spent", 0),
                customer.get("average_order_value", 0),
                customer.get("days_since_last_purchase", 0)
            ])
        
        features = np.array(features)
        
        # Normalize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=min(num_segments, len(customer_data)), random_state=42)
        labels = kmeans.fit_predict(features_scaled)
        
        # Create segments
        segments = []
        for i in range(num_segments):
            segment_customers = [customer_data[j] for j in range(len(customer_data)) if labels[j] == i]
            if segment_customers:
                segments.append({
                    "segment_id": f"segment_{i+1}",
                    "name": f"Segment {i+1}",
                    "size": len(segment_customers),
                    "characteristics": {
                        "avg_orders": np.mean([c.get("total_orders", 0) for c in segment_customers]),
                        "avg_spent": np.mean([c.get("total_spent", 0) for c in segment_customers]),
                        "avg_aov": np.mean([c.get("average_order_value", 0) for c in segment_customers])
                    }
                })
        
        return {
            "segments": segments,
            "num_segments": len(segments)
        }
    
    def recommend_price(
        self,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recommend optimal price
        
        Args:
            product_data: Product and market data
            
        Returns:
            Price recommendation
        """
        current_price = product_data.get("current_price", 0)
        competitor_prices = product_data.get("competitor_prices", [])
        inventory_level = product_data.get("inventory_level", 0)
        demand_elasticity = product_data.get("demand_elasticity", 1.5)
        
        # Simple pricing logic
        recommended_price = current_price
        
        # Competitor pricing
        if competitor_prices:
            avg_competitor_price = np.mean(competitor_prices)
            if avg_competitor_price < current_price * 0.9:
                # Competitors are significantly cheaper
                recommended_price = avg_competitor_price * 1.05
            elif avg_competitor_price > current_price * 1.1:
                # We can increase price
                recommended_price = min(current_price * 1.1, avg_competitor_price * 0.95)
        
        # Inventory-based pricing
        if inventory_level < 10:
            # Low inventory - can increase price
            recommended_price *= 1.05
        elif inventory_level > 100:
            # High inventory - consider discount
            recommended_price *= 0.95
        
        # Ensure price is reasonable
        recommended_price = max(current_price * 0.7, min(current_price * 1.3, recommended_price))
        
        reasoning = []
        if competitor_prices:
            reasoning.append(f"Competitor average: {np.mean(competitor_prices):.2f}")
        if inventory_level < 10:
            reasoning.append("Low inventory - premium pricing")
        elif inventory_level > 100:
            reasoning.append("High inventory - promotional pricing")
        
        return {
            "recommended_price": round(recommended_price, 2),
            "confidence": 0.80,
            "reasoning": " ".join(reasoning) if reasoning else "Market-based pricing"
        }


ml_service = MLService()

