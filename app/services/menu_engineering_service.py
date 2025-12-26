"""
Menu Engineering Intelligence Service
Optimizes menu profitability using association rules and Bayesian inference
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
from itertools import combinations


class MenuEngineeringService:
    """
    Menu Engineering Intelligence
    
    Uses:
    - Association rule mining for bundle recommendations
    - Bayesian profit inference for pricing suggestions
    - Multi-dimensional analysis (margin, popularity, complexity)
    """
    
    def __init__(self):
        """Initialize menu engineering service"""
        self.menu_items = self._initialize_menu_items()
        self.order_history = self._generate_sample_order_history()
        self.model_version = "1.0.0"
    
    def _initialize_menu_items(self) -> List[Dict[str, Any]]:
        """Initialize menu items with cost, price, and complexity"""
        return [
            {"id": "burger", "name": "Classic Burger", "price": 12.99, "cost": 4.50, "prep_time": 12, "complexity": "medium", "category": "mains"},
            {"id": "pizza", "name": "Margherita Pizza", "price": 14.99, "cost": 5.20, "prep_time": 18, "complexity": "high", "category": "mains"},
            {"id": "salad", "name": "Caesar Salad", "price": 9.99, "cost": 3.20, "prep_time": 6, "complexity": "low", "category": "sides"},
            {"id": "pasta", "name": "Spaghetti Carbonara", "price": 13.99, "cost": 4.80, "prep_time": 15, "complexity": "medium", "category": "mains"},
            {"id": "wings", "name": "Buffalo Wings", "price": 11.99, "cost": 5.50, "prep_time": 20, "complexity": "medium", "category": "appetizers"},
            {"id": "tacos", "name": "Fish Tacos", "price": 10.99, "cost": 4.00, "prep_time": 10, "complexity": "low", "category": "mains"},
            {"id": "steak", "name": "Ribeye Steak", "price": 24.99, "cost": 12.00, "prep_time": 22, "complexity": "high", "category": "mains"},
            {"id": "soup", "name": "Tomato Soup", "price": 6.99, "cost": 2.00, "prep_time": 5, "complexity": "low", "category": "sides"},
            {"id": "fries", "name": "French Fries", "price": 4.99, "cost": 1.50, "prep_time": 8, "complexity": "low", "category": "sides"},
            {"id": "dessert", "name": "Chocolate Cake", "price": 7.99, "cost": 2.50, "prep_time": 3, "complexity": "low", "category": "desserts"},
        ]
    
    def _generate_sample_order_history(self) -> List[Dict[str, Any]]:
        """Generate sample order history for analysis"""
        orders = []
        np.random.seed(42)
        
        # Generate 500 orders with realistic patterns
        for i in range(500):
            order_items = []
            
            # Main item (always present)
            main = np.random.choice(["burger", "pizza", "pasta", "tacos", "steak"], p=[0.3, 0.25, 0.2, 0.15, 0.1])
            order_items.append(main)
            
            # Side item (70% chance)
            if np.random.random() < 0.7:
                side = np.random.choice(["salad", "fries", "soup"], p=[0.4, 0.4, 0.2])
                order_items.append(side)
            
            # Appetizer (30% chance, especially with wings)
            if np.random.random() < 0.3:
                order_items.append("wings")
            
            # Dessert (25% chance)
            if np.random.random() < 0.25:
                order_items.append("dessert")
            
            orders.append({
                "order_id": f"ORD-{i:04d}",
                "items": order_items,
                "total_value": sum(self._get_item_price(item) for item in order_items),
            })
        
        return orders
    
    def _get_item_price(self, item_id: str) -> float:
        """Get price for menu item"""
        item = next((i for i in self.menu_items if i["id"] == item_id), None)
        return item["price"] if item else 0.0
    
    def analyze_menu_items(self) -> List[Dict[str, Any]]:
        """
        Analyze all menu items across margin, popularity, and complexity
        
        Returns menu items with:
        - Margin percentage
        - Popularity score (orders count)
        - Profit score (margin × popularity)
        - Recommendation category (star, plowhorse, puzzle, dog)
        """
        # Calculate metrics for each item
        item_stats = {}
        for item in self.menu_items:
            item_id = item["id"]
            
            # Count occurrences in orders
            order_count = sum(1 for order in self.order_history if item_id in order["items"])
            popularity = order_count / len(self.order_history) if self.order_history else 0
            
            # Calculate margin
            margin = ((item["price"] - item["cost"]) / item["price"]) * 100 if item["price"] > 0 else 0
            
            # Profit score (normalized)
            revenue = order_count * item["price"]
            profit = order_count * (item["price"] - item["cost"])
            profit_score = profit / max(revenue, 1) * 100  # Normalize
            
            # Determine category
            avg_margin = np.mean([(i["price"] - i["cost"]) / i["price"] * 100 for i in self.menu_items])
            avg_popularity = np.mean([sum(1 for o in self.order_history if i["id"] in o["items"]) / len(self.order_history) for i in self.menu_items])
            
            if margin >= avg_margin and popularity >= avg_popularity:
                category = "star"  # High margin, high popularity
                recommendation = "Promote and maintain"
            elif margin >= avg_margin and popularity < avg_popularity:
                category = "puzzle"  # High margin, low popularity
                recommendation = "Promote more, consider price reduction"
            elif margin < avg_margin and popularity >= avg_popularity:
                category = "plowhorse"  # Low margin, high popularity
                recommendation = "Consider price increase or cost reduction"
            else:
                category = "dog"  # Low margin, low popularity
                recommendation = "Consider removing or repositioning"
            
            item_stats[item_id] = {
                **item,
                "order_count": order_count,
                "popularity": round(popularity * 100, 1),  # Percentage
                "margin": round(margin, 1),
                "profit_score": round(profit_score, 1),
                "revenue": round(revenue, 2),
                "profit": round(profit, 2),
                "category": category,
                "recommendation": recommendation,
            }
        
        return list(item_stats.values())
    
    def get_menu_item_details(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed analysis for a specific menu item"""
        menu_analysis = self.analyze_menu_items()
        item = next((i for i in menu_analysis if i["id"] == item_id), None)
        
        if not item:
            return None
        
        # Get association rules (bundles)
        bundles = self._find_bundle_opportunities(item_id)
        
        # Get pricing suggestions
        pricing_suggestions = self._suggest_pricing(item_id, item)
        
        return {
            "item": item,
            "bundles": bundles,
            "pricing_suggestions": pricing_suggestions,
        }
    
    def _find_bundle_opportunities(self, item_id: str, min_support: float = 0.1) -> List[Dict[str, Any]]:
        """
        Find association rules (items frequently ordered together)
        Using simplified association rule mining
        """
        bundles = []
        
        # Find items frequently ordered with this item
        co_occurrence = defaultdict(int)
        item_order_count = 0
        
        for order in self.order_history:
            if item_id in order["items"]:
                item_order_count += 1
                for other_item in order["items"]:
                    if other_item != item_id:
                        co_occurrence[other_item] += 1
        
        # Calculate confidence (probability of other_item given item_id)
        for other_item_id, co_count in co_occurrence.items():
            confidence = co_count / item_order_count if item_order_count > 0 else 0
            
            if confidence >= min_support:
                other_item = next((i for i in self.menu_items if i["id"] == other_item_id), None)
                current_item = next((i for i in self.menu_items if i["id"] == item_id), None)
                if other_item and current_item:
                    bundle_price = current_item["price"] + other_item["price"]
                    bundles.append({
                        "item_id": other_item_id,
                        "item_name": other_item["name"],
                        "confidence": round(confidence * 100, 1),  # Percentage
                        "co_occurrence_count": co_count,
                        "bundle_price": round(bundle_price, 2),
                        "suggested_bundle_discount": 0.10,  # 10% discount
                        "suggested_bundle_price": round(bundle_price * 0.9, 2),
                    })
        
        # Sort by confidence
        bundles.sort(key=lambda x: x["confidence"], reverse=True)
        
        return bundles[:5]  # Top 5 bundles
    
    def _suggest_pricing(self, item_id: str, item_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bayesian-style pricing suggestions based on:
        - Current margin vs category average
        - Popularity elasticity
        - Competitive positioning
        """
        current_price = item_stats["price"]
        current_margin = item_stats["margin"]
        popularity = item_stats["popularity"]
        category = item_stats["category"]
        
        suggestions = {
            "current_price": current_price,
            "current_margin": current_margin,
            "recommendations": [],
        }
        
        # Pricing recommendations based on category
        if category == "star":
            # High margin, high popularity - consider slight increase
            suggested_price = current_price * 1.05
            suggestions["recommendations"].append({
                "action": "maintain_or_slight_increase",
                "suggested_price": round(suggested_price, 2),
                "expected_margin_change": round(current_margin * 1.05 - current_margin, 1),
                "reasoning": f"Strong performer. Small price increase could improve margins without significant demand impact.",
            })
        
        elif category == "puzzle":
            # High margin, low popularity - consider price reduction to increase volume
            suggested_price = current_price * 0.90
            suggestions["recommendations"].append({
                "action": "reduce_price",
                "suggested_price": round(suggested_price, 2),
                "expected_margin_change": round((suggested_price - item_stats["cost"]) / suggested_price * 100 - current_margin, 1),
                "reasoning": f"High margin but low popularity. Price reduction could increase order volume and total profit.",
            })
        
        elif category == "plowhorse":
            # Low margin, high popularity - consider price increase
            suggested_price = current_price * 1.10
            suggestions["recommendations"].append({
                "action": "increase_price",
                "suggested_price": round(suggested_price, 2),
                "expected_margin_change": round((suggested_price - item_stats["cost"]) / suggested_price * 100 - current_margin, 1),
                "reasoning": f"Popular but low margin. Price increase could improve profitability while maintaining acceptable demand.",
            })
        
        elif category == "dog":
            # Low margin, low popularity - consider removal or repositioning
            suggestions["recommendations"].append({
                "action": "consider_removal_or_reposition",
                "reasoning": f"Low margin and low popularity. Consider removing from menu or repositioning with cost reduction.",
            })
        
        return suggestions


# Global instance
menu_engineering_service = MenuEngineeringService()

