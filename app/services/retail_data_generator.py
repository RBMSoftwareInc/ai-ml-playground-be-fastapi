"""
Retail AI Store Intelligence Data Generator
Generates comprehensive synthetic datasets for physical store intelligence
"""
import numpy as np
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum


class ZoneType(str, Enum):
    ENTRANCE = "entrance"
    AISLE = "aisle"
    CHECKOUT = "checkout"
    DISPLAY = "display"
    EXIT = "exit"


@dataclass
class StoreLayout:
    store_id: str
    zones: List[Dict[str, Any]]  # Zone definitions with coordinates
    total_area_sqft: float
    checkout_counters: int


@dataclass
class FootfallEvent:
    event_id: str
    timestamp: datetime
    zone_id: str
    person_count: int
    movement_type: str  # 'enter', 'exit', 'pass_through', 'dwell'
    dwell_duration_seconds: Optional[float] = None


@dataclass
class QueueEvent:
    queue_id: str
    counter_id: str
    timestamp: datetime
    queue_length: int
    average_wait_time_seconds: float
    service_completion_rate: float


@dataclass
class POSEvent:
    transaction_id: str
    timestamp: datetime
    counter_id: str
    transaction_value: float
    item_count: int
    transaction_duration_seconds: float


@dataclass
class SuspiciousEvent:
    event_id: str
    timestamp: datetime
    zone_id: str
    event_type: str  # 'lingering', 'concealment_pattern', 'unusual_movement'
    risk_score: float
    description: str


class RetailDataGenerator:
    """Generate synthetic retail store intelligence data"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        # Generate store layout
        self.store_layout = self._generate_store_layout()
        
        # Generate historical data
        self.footfall_events: List[FootfallEvent] = []
        self.queue_events: List[QueueEvent] = []
        self.pos_events: List[POSEvent] = []
        self.suspicious_events: List[SuspiciousEvent] = []
        
        self._generate_footfall_data()
        self._generate_queue_data()
        self._generate_pos_data()
        self._generate_suspicious_events()
    
    def _generate_store_layout(self) -> StoreLayout:
        """Generate a realistic store layout"""
        zones = [
            {
                "zone_id": "entrance_1",
                "zone_name": "Main Entrance",
                "zone_type": ZoneType.ENTRANCE.value,
                "area_sqft": 150,
                "coordinates": {"x": 0, "y": 0, "width": 30, "height": 5},
            },
            {
                "zone_id": "aisle_1",
                "zone_name": "Electronics Aisle",
                "zone_type": ZoneType.AISLE.value,
                "area_sqft": 800,
                "coordinates": {"x": 0, "y": 5, "width": 40, "height": 20},
            },
            {
                "zone_id": "aisle_2",
                "zone_name": "Clothing Aisle",
                "zone_type": ZoneType.AISLE.value,
                "area_sqft": 1000,
                "coordinates": {"x": 40, "y": 5, "width": 50, "height": 20},
            },
            {
                "zone_id": "aisle_3",
                "zone_name": "Food & Beverages",
                "zone_type": ZoneType.AISLE.value,
                "area_sqft": 600,
                "coordinates": {"x": 0, "y": 25, "width": 30, "height": 20},
            },
            {
                "zone_id": "display_1",
                "zone_name": "Featured Products Display",
                "zone_type": ZoneType.DISPLAY.value,
                "area_sqft": 300,
                "coordinates": {"x": 30, "y": 25, "width": 20, "height": 15},
            },
            {
                "zone_id": "checkout_zone",
                "zone_name": "Checkout Area",
                "zone_type": ZoneType.CHECKOUT.value,
                "area_sqft": 400,
                "coordinates": {"x": 70, "y": 5, "width": 30, "height": 40},
                "counters": [
                    {"counter_id": "counter_1", "x": 72, "y": 10},
                    {"counter_id": "counter_2", "x": 75, "y": 10},
                    {"counter_id": "counter_3", "x": 78, "x": 10},
                    {"counter_id": "counter_4", "x": 81, "y": 10},
                ],
            },
            {
                "zone_id": "exit_1",
                "zone_name": "Main Exit",
                "zone_type": ZoneType.EXIT.value,
                "area_sqft": 100,
                "coordinates": {"x": 70, "y": 0, "width": 10, "height": 5},
            },
        ]
        
        return StoreLayout(
            store_id="store_001",
            zones=zones,
            total_area_sqft=3350,
            checkout_counters=4,
        )
    
    def _generate_footfall_data(self, days: int = 7, hours_per_day: int = 14):
        """Generate footfall and movement data"""
        start_date = datetime.now() - timedelta(days=days)
        
        # Peak hours: 10 AM - 2 PM, 5 PM - 8 PM
        peak_hours = [10, 11, 12, 13, 14, 17, 18, 19, 20]
        
        event_id = 0
        for day in range(days):
            for hour in range(8, 22):  # 8 AM to 10 PM
                is_peak = hour in peak_hours
                
                # Events per hour (higher during peak)
                events_per_hour = random.randint(120, 200) if is_peak else random.randint(40, 80)
                
                for _ in range(events_per_hour):
                    minute = random.randint(0, 59)
                    second = random.randint(0, 59)
                    timestamp = start_date + timedelta(
                        days=day,
                        hours=hour - 8,
                        minutes=minute,
                        seconds=second
                    )
                    
                    # Zone selection (weighted)
                    zone = random.choices(
                        self.store_layout.zones,
                        weights=[0.15, 0.25, 0.25, 0.20, 0.10, 0.05, 0.05],
                    )[0]
                    
                    # Movement type
                    if zone["zone_type"] == ZoneType.ENTRANCE.value:
                        movement_type = "enter"
                        person_count = random.randint(1, 3)
                        dwell_duration = None
                    elif zone["zone_type"] == ZoneType.EXIT.value:
                        movement_type = "exit"
                        person_count = random.randint(1, 3)
                        dwell_duration = None
                    elif zone["zone_type"] == ZoneType.AISLE.value:
                        movement_type = random.choices(
                            ["pass_through", "dwell"],
                            weights=[0.6, 0.4]
                        )[0]
                        person_count = random.randint(1, 2)
                        dwell_duration = random.uniform(15, 180) if movement_type == "dwell" else None
                    elif zone["zone_type"] == ZoneType.DISPLAY.value:
                        movement_type = "dwell"
                        person_count = random.randint(1, 3)
                        dwell_duration = random.uniform(30, 120)
                    else:
                        movement_type = "pass_through"
                        person_count = random.randint(1, 5)
                        dwell_duration = None
                    
                    event = FootfallEvent(
                        event_id=f"footfall_{event_id:06d}",
                        timestamp=timestamp,
                        zone_id=zone["zone_id"],
                        person_count=person_count,
                        movement_type=movement_type,
                        dwell_duration_seconds=dwell_duration,
                    )
                    self.footfall_events.append(event)
                    event_id += 1
    
    def _generate_queue_data(self, days: int = 7):
        """Generate queue and checkout data"""
        start_date = datetime.now() - timedelta(days=days)
        counters = ["counter_1", "counter_2", "counter_3", "counter_4"]
        
        for day in range(days):
            for hour in range(8, 22):
                # Sample every 15 minutes
                for minute in [0, 15, 30, 45]:
                    timestamp = start_date + timedelta(
                        days=day,
                        hours=hour - 8,
                        minutes=minute
                    )
                    
                    is_peak = hour in [12, 13, 18, 19, 20]
                    
                    for counter_id in counters:
                        # Queue length (higher during peak)
                        base_queue = random.randint(0, 2) if not is_peak else random.randint(2, 8)
                        queue_length = max(0, base_queue + random.randint(-1, 2))
                        
                        # Wait time (approximately 2 minutes per person in queue)
                        average_wait_time = queue_length * 120 + random.uniform(0, 60)
                        
                        # Service rate (items per minute)
                        service_rate = random.uniform(0.8, 1.5)
                        
                        event = QueueEvent(
                            queue_id=f"queue_{day}_{hour}_{minute}_{counter_id}",
                            counter_id=counter_id,
                            timestamp=timestamp,
                            queue_length=queue_length,
                            average_wait_time_seconds=average_wait_time,
                            service_completion_rate=service_rate,
                        )
                        self.queue_events.append(event)
    
    def _generate_pos_data(self, days: int = 7):
        """Generate POS transaction data"""
        start_date = datetime.now() - timedelta(days=days)
        counters = ["counter_1", "counter_2", "counter_3", "counter_4"]
        
        transaction_id = 0
        for day in range(days):
            for hour in range(8, 22):
                is_peak = hour in [12, 13, 18, 19, 20]
                
                # Transactions per hour
                transactions_per_hour = random.randint(80, 150) if is_peak else random.randint(20, 60)
                
                for _ in range(transactions_per_hour):
                    minute = random.randint(0, 59)
                    second = random.randint(0, 59)
                    timestamp = start_date + timedelta(
                        days=day,
                        hours=hour - 8,
                        minutes=minute,
                        seconds=second
                    )
                    
                    counter_id = random.choice(counters)
                    
                    # Transaction details
                    item_count = random.randint(1, 15)
                    avg_item_price = random.uniform(8, 45)
                    transaction_value = item_count * avg_item_price + random.uniform(-5, 5)
                    
                    # Service time (30 seconds base + 10 seconds per item)
                    transaction_duration = 30 + (item_count * 10) + random.uniform(-5, 10)
                    
                    event = POSEvent(
                        transaction_id=f"pos_{transaction_id:06d}",
                        timestamp=timestamp,
                        counter_id=counter_id,
                        transaction_value=transaction_value,
                        item_count=item_count,
                        transaction_duration_seconds=transaction_duration,
                    )
                    self.pos_events.append(event)
                    transaction_id += 1
    
    def _generate_suspicious_events(self):
        """Generate suspicious behavior events (sparse, realistic)"""
        # Only generate a few suspicious events (realistic rate)
        num_suspicious = random.randint(5, 15)
        
        start_date = datetime.now() - timedelta(days=7)
        event_id = 0
        
        for _ in range(num_suspicious):
            # Random timestamp within last 7 days
            days_offset = random.uniform(0, 7)
            hours_offset = random.uniform(0, 14)
            timestamp = start_date + timedelta(days=days_offset, hours=hours_offset)
            
            # Select zone (aisles more likely)
            zone = random.choice([z for z in self.store_layout.zones if z["zone_type"] == ZoneType.AISLE.value])
            
            # Event type
            event_type = random.choice([
                "lingering",
                "concealment_pattern",
                "unusual_movement",
            ])
            
            # Risk score
            risk_score = random.uniform(0.6, 0.95)
            
            descriptions = {
                "lingering": f"Extended dwell time in {zone['zone_name']} exceeding normal patterns",
                "concealment_pattern": f"Movement pattern consistent with item handling in {zone['zone_name']}",
                "unusual_movement": f"Non-standard movement pattern detected in {zone['zone_name']}",
            }
            
            event = SuspiciousEvent(
                event_id=f"suspicious_{event_id:04d}",
                timestamp=timestamp,
                zone_id=zone["zone_id"],
                event_type=event_type,
                risk_score=risk_score,
                description=descriptions[event_type],
            )
            self.suspicious_events.append(event)
            event_id += 1
    
    def get_store_layout(self) -> Dict[str, Any]:
        """Get serialized store layout"""
        return {
            "store_id": self.store_layout.store_id,
            "zones": self.store_layout.zones,
            "total_area_sqft": self.store_layout.total_area_sqft,
            "checkout_counters": self.store_layout.checkout_counters,
        }
    
    def get_footfall_events(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        zone_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get serialized footfall events"""
        events = self.footfall_events
        
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        if zone_id:
            events = [e for e in events if e.zone_id == zone_id]
        
        return [{
            "event_id": e.event_id,
            "timestamp": e.timestamp.isoformat(),
            "zone_id": e.zone_id,
            "person_count": e.person_count,
            "movement_type": e.movement_type,
            "dwell_duration_seconds": e.dwell_duration_seconds,
        } for e in events]
    
    def get_queue_events(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        counter_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get serialized queue events"""
        events = self.queue_events
        
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        if counter_id:
            events = [e for e in events if e.counter_id == counter_id]
        
        return [{
            "queue_id": e.queue_id,
            "counter_id": e.counter_id,
            "timestamp": e.timestamp.isoformat(),
            "queue_length": e.queue_length,
            "average_wait_time_seconds": e.average_wait_time_seconds,
            "service_completion_rate": e.service_completion_rate,
        } for e in events]
    
    def get_pos_events(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get serialized POS events"""
        events = self.pos_events
        
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        
        return [{
            "transaction_id": e.transaction_id,
            "timestamp": e.timestamp.isoformat(),
            "counter_id": e.counter_id,
            "transaction_value": round(e.transaction_value, 2),
            "item_count": e.item_count,
            "transaction_duration_seconds": round(e.transaction_duration_seconds, 2),
        } for e in events]
    
    def get_suspicious_events(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        min_risk_score: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get serialized suspicious events"""
        events = self.suspicious_events
        
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
        if min_risk_score is not None:
            events = [e for e in events if e.risk_score >= min_risk_score]
        
        return [{
            "event_id": e.event_id,
            "timestamp": e.timestamp.isoformat(),
            "zone_id": e.zone_id,
            "event_type": e.event_type,
            "risk_score": round(e.risk_score, 3),
            "description": e.description,
        } for e in events]


# Global instance
retail_data_generator = RetailDataGenerator(seed=42)

