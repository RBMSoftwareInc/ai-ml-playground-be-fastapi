"""
Entertainment AI Data Generator
Generates comprehensive synthetic datasets for training and demo purposes
"""
import numpy as np
import random
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json


@dataclass
class ContentItem:
    content_id: str
    title: str
    genre: str
    mood: str
    actors: List[str]
    themes: List[str]
    duration_minutes: int
    release_year: int
    rating: float
    view_count: int


@dataclass
class UserInteraction:
    user_id: str
    content_id: str
    interaction_type: str  # 'watch', 'like', 'skip', 'share'
    timestamp: datetime
    watch_duration_seconds: int
    completion_rate: float


@dataclass
class AudienceSegment:
    segment_id: str
    segment_name: str
    size: int
    demographics: Dict[str, Any]
    content_preferences: List[str]
    engagement_score: float


class EntertainmentDataGenerator:
    """Generate synthetic entertainment industry data"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.genres = [
            'Action', 'Comedy', 'Drama', 'Thriller', 'Romance',
            'Sci-Fi', 'Horror', 'Documentary', 'Animation', 'Crime'
        ]
        
        self.moods = [
            'uplifting', 'suspenseful', 'emotional', 'lighthearted',
            'intense', 'thoughtful', 'adventurous', 'dark', 'hopeful'
        ]
        
        self.themes = [
            'friendship', 'love', 'betrayal', 'redemption', 'heroism',
            'survival', 'justice', 'family', 'adventure', 'mystery'
        ]
        
        self.actors = [
            'Actor A', 'Actor B', 'Actor C', 'Actor D', 'Actor E',
            'Actor F', 'Actor G', 'Actor H', 'Actor I', 'Actor J'
        ]
        
        # Generate content catalog
        self.content_catalog: List[ContentItem] = []
        self.user_interactions: List[UserInteraction] = []
        self.audience_segments: List[AudienceSegment] = []
        
        self._generate_content_catalog()
        self._generate_audience_segments()
        self._generate_user_interactions()
    
    def _generate_content_catalog(self, num_items: int = 100):
        """Generate synthetic content catalog"""
        for i in range(num_items):
            content = ContentItem(
                content_id=f"content_{i:03d}",
                title=f"{random.choice(['The', 'A', 'In', 'Beyond'])} {random.choice(['Secret', 'Lost', 'Hidden', 'Last'])} {random.choice(['Story', 'Journey', 'Quest', 'Truth'])}",
                genre=random.choice(self.genres),
                mood=random.choice(self.moods),
                actors=random.sample(self.actors, k=random.randint(2, 5)),
                themes=random.sample(self.themes, k=random.randint(2, 4)),
                duration_minutes=random.randint(20, 180),
                release_year=random.randint(2018, 2024),
                rating=np.random.normal(7.5, 1.5),
                view_count=random.randint(1000, 5000000)
            )
            content.rating = max(1.0, min(10.0, content.rating))
            self.content_catalog.append(content)
    
    def _generate_audience_segments(self):
        """Generate audience segments"""
        segments_data = [
            {
                'segment_id': 'young_adults',
                'segment_name': 'Young Adults (18-25)',
                'size': 350000,
                'demographics': {'age_range': '18-25', 'gender_distribution': {'M': 0.52, 'F': 0.48}},
                'content_preferences': ['Action', 'Comedy', 'Sci-Fi'],
                'engagement_score': 0.82
            },
            {
                'segment_id': 'middle_aged',
                'segment_name': 'Middle-Aged (35-50)',
                'size': 280000,
                'demographics': {'age_range': '35-50', 'gender_distribution': {'M': 0.48, 'F': 0.52}},
                'content_preferences': ['Drama', 'Thriller', 'Documentary'],
                'engagement_score': 0.75
            },
            {
                'segment_id': 'seniors',
                'segment_name': 'Seniors (55+)',
                'size': 150000,
                'demographics': {'age_range': '55+', 'gender_distribution': {'M': 0.45, 'F': 0.55}},
                'content_preferences': ['Drama', 'Documentary', 'Romance'],
                'engagement_score': 0.68
            },
        ]
        
        for seg_data in segments_data:
            segment = AudienceSegment(**seg_data)
            self.audience_segments.append(segment)
    
    def _generate_user_interactions(self, num_users: int = 1000, days: int = 90):
        """Generate user interaction history"""
        start_date = datetime.now() - timedelta(days=days)
        
        for user_idx in range(num_users):
            user_id = f"user_{user_idx:04d}"
            
            # Each user interacts with 10-50 pieces of content
            num_interactions = random.randint(10, 50)
            
            for _ in range(num_interactions):
                content = random.choice(self.content_catalog)
                interaction_type = random.choices(
                    ['watch', 'like', 'skip', 'share'],
                    weights=[0.6, 0.2, 0.15, 0.05]
                )[0]
                
                timestamp = start_date + timedelta(
                    days=random.randint(0, days),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                watch_duration = random.randint(60, content.duration_minutes * 60) if interaction_type == 'watch' else 0
                completion_rate = watch_duration / (content.duration_minutes * 60) if interaction_type == 'watch' else 0.0
                completion_rate = min(1.0, completion_rate)
                
                interaction = UserInteraction(
                    user_id=user_id,
                    content_id=content.content_id,
                    interaction_type=interaction_type,
                    timestamp=timestamp,
                    watch_duration_seconds=watch_duration,
                    completion_rate=completion_rate
                )
                self.user_interactions.append(interaction)
    
    def get_content_catalog(self) -> List[Dict[str, Any]]:
        """Get serialized content catalog"""
        return [asdict(item) for item in self.content_catalog]
    
    def get_user_interactions(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get serialized user interactions"""
        interactions = self.user_interactions
        if user_id:
            interactions = [i for i in interactions if i.user_id == user_id]
        
        return [{
            'user_id': i.user_id,
            'content_id': i.content_id,
            'interaction_type': i.interaction_type,
            'timestamp': i.timestamp.isoformat(),
            'watch_duration_seconds': i.watch_duration_seconds,
            'completion_rate': i.completion_rate,
        } for i in interactions]
    
    def get_audience_segments(self) -> List[Dict[str, Any]]:
        """Get serialized audience segments"""
        return [asdict(segment) for segment in self.audience_segments]
    
    def generate_churn_risk_data(self, num_subscribers: int = 5000) -> List[Dict[str, Any]]:
        """Generate subscriber churn risk data"""
        subscribers = []
        
        for i in range(num_subscribers):
            user_id = f"subscriber_{i:04d}"
            
            # Calculate engagement metrics
            user_interactions = [ui for ui in self.user_interactions if ui.user_id == user_id]
            total_watches = len([ui for ui in user_interactions if ui.interaction_type == 'watch'])
            avg_completion = np.mean([ui.completion_rate for ui in user_interactions if ui.completion_rate > 0]) if user_interactions else 0
            
            days_since_last_watch = random.randint(0, 60)
            subscription_age_days = random.randint(30, 730)
            
            # Churn risk factors
            engagement_score = min(1.0, (total_watches * 0.1) + (avg_completion * 0.5))
            inactivity_score = days_since_last_watch / 60.0
            
            # Simulate churn probability
            churn_probability = 0.2 * (1 - engagement_score) + 0.3 * inactivity_score
            churn_probability += np.random.normal(0, 0.1)
            churn_probability = max(0.0, min(1.0, churn_probability))
            
            subscribers.append({
                'user_id': user_id,
                'subscription_age_days': subscription_age_days,
                'total_watches': total_watches,
                'avg_completion_rate': round(avg_completion, 3),
                'days_since_last_watch': days_since_last_watch,
                'engagement_score': round(engagement_score, 3),
                'churn_probability': round(churn_probability, 3),
                'risk_level': 'high' if churn_probability > 0.7 else 'medium' if churn_probability > 0.4 else 'low',
            })
        
        return subscribers
    
    def generate_content_moderation_data(self, num_segments: int = 100) -> List[Dict[str, Any]]:
        """Generate content moderation risk data"""
        segments = []
        
        risk_types = ['violence', 'profanity', 'sexual_content', 'hate_speech', 'none']
        risk_levels = ['none', 'low', 'medium', 'high']
        
        for i in range(num_segments):
            segment_start = i * 10  # 10 seconds per segment
            segment_end = (i + 1) * 10
            
            # Randomly assign risks (mostly none/low)
            risk_type = random.choices(risk_types, weights=[0.05, 0.05, 0.03, 0.02, 0.85])[0]
            risk_level = random.choice(risk_levels) if risk_type != 'none' else 'none'
            
            segments.append({
                'segment_id': f"segment_{i:03d}",
                'start_time': segment_start,
                'end_time': segment_end,
                'risk_type': risk_type,
                'risk_level': risk_level,
                'confidence': round(np.random.uniform(0.7, 0.98) if risk_type != 'none' else np.random.uniform(0.85, 0.99), 3),
                'requires_review': risk_type != 'none' and risk_level in ['medium', 'high'],
            })
        
        return segments
    
    def generate_ad_optimization_data(self, num_placements: int = 50) -> List[Dict[str, Any]]:
        """Generate ad placement optimization data"""
        placements = []
        
        ad_types = ['pre_roll', 'mid_roll', 'post_roll', 'overlay']
        
        for i in range(num_placements):
            placement_time = i * 120  # Every 2 minutes
            
            # Simulate ad performance
            impressions = random.randint(10000, 1000000)
            clicks = random.randint(int(impressions * 0.01), int(impressions * 0.05))
            ctr = clicks / impressions
            
            revenue_per_second = np.random.uniform(0.5, 5.0)
            total_revenue = revenue_per_second * 30  # 30 second ad
            
            placements.append({
                'placement_id': f"ad_{i:03d}",
                'ad_type': random.choice(ad_types),
                'placement_time_seconds': placement_time,
                'impressions': impressions,
                'clicks': clicks,
                'ctr': round(ctr, 4),
                'revenue_per_second': round(revenue_per_second, 2),
                'total_revenue': round(total_revenue, 2),
                'engagement_score': round(np.random.uniform(0.3, 0.9), 2),
            })
        
        return placements


# Global instance
entertainment_data_generator = EntertainmentDataGenerator(seed=42)

