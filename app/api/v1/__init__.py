"""
API v1 Routes
"""
from fastapi import APIRouter
from app.api.v1 import ecommerce, healthcare, fintech, travel, hospitality, entertainment, manufacturing, realestate, retail, webhooks

api_router = APIRouter()

# Include all industry routers
api_router.include_router(ecommerce.router, prefix="/ecommerce", tags=["E-commerce"])
api_router.include_router(healthcare.router, prefix="/healthcare", tags=["Healthcare"])
api_router.include_router(fintech.router, prefix="/fintech", tags=["Fintech"])
api_router.include_router(travel.router, prefix="/travel", tags=["Travel"])
api_router.include_router(hospitality.router, prefix="/hospitality", tags=["Hospitality"])
api_router.include_router(entertainment.router, prefix="/entertainment", tags=["Entertainment"])
api_router.include_router(manufacturing.router, prefix="/manufacturing", tags=["Manufacturing"])
api_router.include_router(realestate.router, prefix="/realestate", tags=["Real Estate"])
api_router.include_router(retail.router, prefix="/retail", tags=["Retail"])

# Webhook routes for real-time updates
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

# Legacy endpoints for backward compatibility
api_router.include_router(ecommerce.router, prefix="", tags=["Legacy E-commerce"])

