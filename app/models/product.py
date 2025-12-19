"""
Product Models
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProductCategory(Base):
    """Product category model"""
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    parent_category_id = Column(String(100), ForeignKey("product_categories.category_id"), nullable=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Product(Base):
    """Product model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(100), unique=True, index=True, nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category_id = Column(String(100), ForeignKey("product_categories.category_id"))
    brand = Column(String(255))
    price = Column(Float, nullable=False)
    cost = Column(Float)
    currency = Column(String(10), default="INR")
    
    # Product attributes
    attributes = Column(JSON)  # Color, size, material, etc.
    images = Column(JSON)  # Array of image URLs
    tags = Column(JSON)  # Array of tags
    
    # SEO
    seo_title = Column(String(255))
    seo_description = Column(Text)
    seo_keywords = Column(JSON)
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Embeddings for search
    embedding = Column(JSON)  # Vector embedding for semantic search
    visual_embedding = Column(JSON)  # Visual similarity embedding
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    variants = relationship("ProductVariant", back_populates="product")


class ProductVariant(Base):
    """Product variant model"""
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(String(100), unique=True, index=True, nullable=False)
    product_id = Column(String(100), ForeignKey("products.product_id"), nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255))
    attributes = Column(JSON)  # Size, color, etc.
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="variants")

