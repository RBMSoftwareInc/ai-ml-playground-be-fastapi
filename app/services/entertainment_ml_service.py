"""
Entertainment AI ML Service
Sophisticated ML models for content recommendation, audience analytics, churn prediction, etc.
"""
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import pickle
import os

from app.services.entertainment_data_generator import entertainment_data_generator


class ContentRecommendationService:
    """Content recommendation using collaborative filtering and content-based approaches"""
    
    def __init__(self):
        self.model_version = "1.0.0"
        self._user_content_matrix = None
        self._content_features = None
        self._vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self._is_trained = False
    
    def train(self, user_interactions: List[Dict], content_catalog: List[Dict]):
        """Train recommendation model"""
        # Build user-content interaction matrix
        user_ids = list(set([ui['user_id'] for ui in user_interactions]))
        content_ids = [c['content_id'] for c in content_catalog]
        
        # Create interaction matrix (users x content)
        matrix = np.zeros((len(user_ids), len(content_ids)))
        user_idx_map = {uid: idx for idx, uid in enumerate(user_ids)}
        content_idx_map = {cid: idx for idx, cid in enumerate(content_ids)}
        
        for ui in user_interactions:
            if ui['user_id'] in user_idx_map and ui['content_id'] in content_idx_map:
                user_idx = user_idx_map[ui['user_id']]
                content_idx = content_idx_map[ui['content_id']]
                
                # Weight interactions by type
                weight = {
                    'watch': 3.0,
                    'like': 2.0,
                    'share': 4.0,
                    'skip': -1.0
                }.get(ui['interaction_type'], 1.0)
                
                matrix[user_idx, content_idx] += weight * ui.get('completion_rate', 0.5)
        
        self._user_content_matrix = matrix
        self._user_ids = user_ids
        self._content_ids = content_ids
        self._user_idx_map = user_idx_map
        self._content_idx_map = content_idx_map
        
        # Build content feature vectors
        content_texts = [
            f"{c.get('title', '')} {c.get('genre', '')} {' '.join(c.get('themes', []))}"
            for c in content_catalog
        ]
        self._content_features = self._vectorizer.fit_transform(content_texts).toarray()
        
        self._is_trained = True
    
    def recommend(
        self,
        user_id: str,
        num_recommendations: int = 10,
        user_interactions: Optional[List[Dict]] = None
    ) -> List[Dict[str, Any]]:
        """Generate content recommendations for a user"""
        if not self._is_trained:
            # Train on default data
            interactions = entertainment_data_generator.get_user_interactions()
            catalog = entertainment_data_generator.get_content_catalog()
            self.train(interactions, catalog)
        
        if user_id not in self._user_idx_map:
            # New user - use content-based filtering
            return self._content_based_recommendations(num_recommendations)
        
        user_idx = self._user_idx_map[user_id]
        user_vector = self._user_content_matrix[user_idx]
        
        # Collaborative filtering: find similar users
        similarities = []
        for other_idx in range(len(self._user_ids)):
            if other_idx != user_idx:
                sim = 1 - cosine(user_vector, self._user_content_matrix[other_idx])
                similarities.append((other_idx, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get recommendations from similar users
        recommended_content_scores = {}
        for other_idx, sim in similarities[:10]:  # Top 10 similar users
            other_vector = self._user_content_matrix[other_idx]
            for content_idx in range(len(self._content_ids)):
                if user_vector[content_idx] == 0 and other_vector[content_idx] > 0:
                    score = sim * other_vector[content_idx]
                    content_id = self._content_ids[content_idx]
                    if content_id not in recommended_content_scores:
                        recommended_content_scores[content_id] = 0
                    recommended_content_scores[content_id] += score
        
        # Sort by score
        sorted_recommendations = sorted(
            recommended_content_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:num_recommendations]
        
        # Get full content details
        catalog = entertainment_data_generator.get_content_catalog()
        catalog_map = {c['content_id']: c for c in catalog}
        
        recommendations = []
        for content_id, score in sorted_recommendations:
            if content_id in catalog_map:
                content = catalog_map[content_id]
                recommendations.append({
                    'content_id': content_id,
                    'title': content['title'],
                    'genre': content['genre'],
                    'rating': content['rating'],
                    'recommendation_score': round(score, 4),
                    'reasoning': f"Users with similar tastes enjoyed this {content['genre']} content",
                })
        
        return recommendations
    
    def _content_based_recommendations(self, num_recommendations: int) -> List[Dict[str, Any]]:
        """Content-based recommendations for new users"""
        catalog = entertainment_data_generator.get_content_catalog()
        
        # Recommend popular/highly-rated content
        sorted_catalog = sorted(catalog, key=lambda x: x['rating'] * np.log(x['view_count'] + 1), reverse=True)
        
        return [
            {
                'content_id': c['content_id'],
                'title': c['title'],
                'genre': c['genre'],
                'rating': c['rating'],
                'recommendation_score': round(c['rating'] / 10.0, 4),
                'reasoning': f"Popular {c['genre']} content with high ratings",
            }
            for c in sorted_catalog[:num_recommendations]
        ]


class AudienceAnalyticsService:
    """Audience segmentation and analytics using clustering"""
    
    def __init__(self):
        self.model_version = "1.0.0"
        self._kmeans_model = None
        self._scaler = StandardScaler()
        self._is_trained = False
    
    def train(self, user_interactions: List[Dict], content_catalog: List[Dict], num_segments: int = 5):
        """Train audience segmentation model"""
        # Build user feature vectors
        user_ids = list(set([ui['user_id'] for ui in user_interactions]))
        user_features = []
        
        catalog_map = {c['content_id']: c for c in content_catalog}
        genres = list(set([c['genre'] for c in content_catalog]))
        
        for user_id in user_ids:
            user_uis = [ui for ui in user_interactions if ui['user_id'] == user_id]
            
            # Features: genre preferences, engagement level, watch frequency
            genre_counts = {g: 0 for g in genres}
            total_watches = 0
            total_completion = 0
            
            for ui in user_uis:
                if ui['interaction_type'] == 'watch':
                    content = catalog_map.get(ui['content_id'])
                    if content:
                        genre_counts[content['genre']] += 1
                    total_watches += 1
                    total_completion += ui.get('completion_rate', 0)
            
            avg_completion = total_completion / total_watches if total_watches > 0 else 0
            feature_vector = list(genre_counts.values()) + [total_watches, avg_completion]
            user_features.append(feature_vector)
        
        if len(user_features) > 0:
            user_features = np.array(user_features)
            user_features_scaled = self._scaler.fit_transform(user_features)
            
            self._kmeans_model = KMeans(n_clusters=num_segments, random_state=42, n_init=10)
            self._kmeans_model.fit(user_features_scaled)
            
            self._user_ids = user_ids
            self._is_trained = True
    
    def analyze_audience(self, user_interactions: List[Dict], content_catalog: List[Dict]) -> Dict[str, Any]:
        """Analyze audience segments"""
        if not self._is_trained:
            self.train(user_interactions, content_catalog)
        
        user_ids = list(set([ui['user_id'] for ui in user_interactions]))
        user_features = []
        catalog_map = {c['content_id']: c for c in content_catalog}
        genres = list(set([c['genre'] for c in content_catalog]))
        
        for user_id in user_ids:
            user_uis = [ui for ui in user_interactions if ui['user_id'] == user_id]
            genre_counts = {g: 0 for g in genres}
            total_watches = 0
            total_completion = 0
            
            for ui in user_uis:
                if ui['interaction_type'] == 'watch':
                    content = catalog_map.get(ui['content_id'])
                    if content:
                        genre_counts[content['genre']] += 1
                    total_watches += 1
                    total_completion += ui.get('completion_rate', 0)
            
            avg_completion = total_completion / total_watches if total_watches > 0 else 0
            feature_vector = list(genre_counts.values()) + [total_watches, avg_completion]
            user_features.append(feature_vector)
        
        if len(user_features) == 0:
            return {'segments': []}
        
        user_features_scaled = self._scaler.transform(np.array(user_features))
        segment_assignments = self._kmeans_model.predict(user_features_scaled)
        
        # Analyze each segment
        segments = []
        for segment_id in range(len(set(segment_assignments))):
            segment_user_indices = [i for i, seg_id in enumerate(segment_assignments) if seg_id == segment_id]
            segment_users = [user_ids[i] for i in segment_user_indices]
            
            # Get segment characteristics
            segment_uis = [ui for ui in user_interactions if ui['user_id'] in segment_users]
            segment_content_ids = list(set([ui['content_id'] for ui in segment_uis]))
            
            genres_watched = {}
            for ui in segment_uis:
                content = catalog_map.get(ui['content_id'])
                if content:
                    genres_watched[content['genre']] = genres_watched.get(content['genre'], 0) + 1
            
            segments.append({
                'segment_id': segment_id,
                'segment_name': f'Segment {segment_id + 1}',
                'size': len(segment_users),
                'preferred_genres': sorted(genres_watched.items(), key=lambda x: x[1], reverse=True)[:3],
                'engagement_score': round(np.mean([ui.get('completion_rate', 0) for ui in segment_uis]), 3),
            })
        
        return {'segments': segments, 'total_users': len(user_ids)}


class ChurnPredictionService:
    """Subscriber churn prediction using gradient boosting"""
    
    def __init__(self):
        self.model_version = "1.0.0"
        self._model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self._is_trained = False
    
    def train(self, subscriber_data: List[Dict]):
        """Train churn prediction model"""
        if len(subscriber_data) < 10:
            return
        
        # Prepare features
        X = []
        y = []
        
        for sub in subscriber_data:
            features = [
                sub['subscription_age_days'],
                sub['total_watches'],
                sub['avg_completion_rate'],
                sub['days_since_last_watch'],
                sub['engagement_score'],
            ]
            X.append(features)
            y.append(1 if sub['risk_level'] == 'high' else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        self._model.fit(X, y)
        self._is_trained = True
    
    def predict_churn_risk(self, subscriber_data: List[Dict]) -> List[Dict[str, Any]]:
        """Predict churn risk for subscribers"""
        if not self._is_trained:
            # Train on provided data
            self.train(subscriber_data)
        
        predictions = []
        for sub in subscriber_data:
            features = np.array([[
                sub['subscription_age_days'],
                sub['total_watches'],
                sub['avg_completion_rate'],
                sub['days_since_last_watch'],
                sub['engagement_score'],
            ]])
            
            probability = self._model.predict_proba(features)[0][1]
            risk_level = 'high' if probability > 0.7 else 'medium' if probability > 0.4 else 'low'
            
            predictions.append({
                **sub,
                'predicted_churn_probability': round(float(probability), 3),
                'predicted_risk_level': risk_level,
            })
        
        return predictions


class ContentModerationService:
    """Content moderation risk assessment"""
    
    def __init__(self):
        self.model_version = "1.0.0"
    
    def analyze_content_segments(self, segments: List[Dict]) -> Dict[str, Any]:
        """Analyze content segments for moderation risks"""
        high_risk_count = sum(1 for s in segments if s['risk_level'] == 'high')
        medium_risk_count = sum(1 for s in segments if s['risk_level'] == 'medium')
        requires_review_count = sum(1 for s in segments if s['requires_review'])
        
        risk_distribution = {}
        for segment in segments:
            risk_type = segment['risk_type']
            if risk_type not in risk_distribution:
                risk_distribution[risk_type] = 0
            risk_distribution[risk_type] += 1
        
        return {
            'total_segments': len(segments),
            'high_risk_segments': high_risk_count,
            'medium_risk_segments': medium_risk_count,
            'requires_review_count': requires_review_count,
            'risk_distribution': risk_distribution,
            'segments': segments,
            'overall_safety_score': round(1.0 - (high_risk_count / len(segments)) if segments else 1.0, 3),
        }


class AdOptimizationService:
    """Ad placement optimization"""
    
    def __init__(self):
        self.model_version = "1.0.0"
    
    def optimize_placements(self, placements: List[Dict]) -> Dict[str, Any]:
        """Optimize ad placements for maximum revenue"""
        # Sort by revenue per second
        sorted_placements = sorted(placements, key=lambda x: x['revenue_per_second'], reverse=True)
        
        total_revenue = sum(p['total_revenue'] for p in placements)
        optimal_revenue = sum(p['total_revenue'] for p in sorted_placements[:20])  # Top 20 placements
        
        recommendations = []
        for placement in sorted_placements[:10]:
            recommendations.append({
                'placement_id': placement['placement_id'],
                'ad_type': placement['ad_type'],
                'placement_time_seconds': placement['placement_time_seconds'],
                'expected_revenue': placement['total_revenue'],
                'reasoning': f"High revenue per second ({placement['revenue_per_second']:.2f}) with good engagement ({placement['engagement_score']:.2f})",
            })
        
        return {
            'current_total_revenue': round(total_revenue, 2),
            'optimal_revenue_potential': round(optimal_revenue, 2),
            'revenue_improvement': round((optimal_revenue / total_revenue - 1) * 100, 1) if total_revenue > 0 else 0,
            'recommended_placements': recommendations,
        }


# Global service instances
content_recommendation_service = ContentRecommendationService()
audience_analytics_service = AudienceAnalyticsService()
churn_prediction_service = ChurnPredictionService()
content_moderation_service = ContentModerationService()
ad_optimization_service = AdOptimizationService()

# Train models on startup
_interactions = entertainment_data_generator.get_user_interactions()
_catalog = entertainment_data_generator.get_content_catalog()
content_recommendation_service.train(_interactions, _catalog)
audience_analytics_service.train(_interactions, _catalog)

