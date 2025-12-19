"""
Inventory Models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Enum, Boolean
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class MovementType(enum.Enum):
    """Inventory movement type"""
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"
    RETURN = "return"
    DAMAGED = "damaged"


class Inventory(Base):
    """Inventory model"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(100), ForeignKey("products.product_id"), nullable=False)
    variant_id = Column(String(100), ForeignKey("product_variants.variant_id"), nullable=True)
    warehouse_id = Column(String(100), nullable=False)
    
    # Stock levels
    current_stock = Column(Integer, default=0, nullable=False)
    reserved_stock = Column(Integer, default=0)
    available_stock = Column(Integer, default=0)
    
    # Reorder points
    reorder_point = Column(Integer)
    reorder_quantity = Column(Integer)
    safety_stock = Column(Integer)
    
    # Lead time
    lead_time_days = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class InventoryMovement(Base):
    """Inventory movement log"""
    __tablename__ = "inventory_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(100), ForeignKey("products.product_id"), nullable=False)
    variant_id = Column(String(100), ForeignKey("product_variants.variant_id"), nullable=True)
    warehouse_id = Column(String(100), nullable=False)
    
    movement_type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    previous_stock = Column(Integer)
    new_stock = Column(Integer)
    
    # Reference
    reference_id = Column(String(100))  # Order ID, PO ID, etc.
    reference_type = Column(String(50))  # order, purchase_order, adjustment, etc.
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

