from utils import update_property_status
from utils.get_pending_properties import get_pending_properties
from fastapi import APIRouter, Depends, HTTPException
from db.mongo import properties_collection
from routes.auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from agents import Runner
from agents_folder import moderation_agent
import json

router = APIRouter()

# ========== Property Detail Schemas ==========

class ResidentialSellDetails(BaseModel):
    price: float
    negotiable: bool
    address: str
    bedrooms: int
    bathrooms: int
    floor_number: Optional[str] = None
    total_area_yards: float
    documents: str  # "documented" or "kacha"
    description: Optional[str] = ""

class ResidentialRentDetails(BaseModel):
    monthly_rent: float
    negotiable: bool
    advance_amount: float
    utility_bills_included: bool
    address: str
    bedrooms: int
    bathrooms: int
    floor_number: Optional[str] = None
    total_area_yards: Optional[float] = None
    description: Optional[str] = ""

class CommercialRentDetails(BaseModel):
    monthly_rent: float
    negotiable: bool
    advance_amount: float
    utility_bills_included: bool
    address: str
    area_yards: float
    floor_number: Optional[str] = None
    description: Optional[str] = ""

class CommercialSellDetails(BaseModel):
    price: float
    negotiable: bool
    address: str
    area_yards: float
    floor_number: Optional[str] = None
    description: Optional[str] = ""

class AgriculturalLeaseDetails(BaseModel):
    rent_per_acre: float
    negotiable: bool
    address: str
    total_area: float
    lease_duration: int
    available_area: float
    description: Optional[str] = ""

class AgriculturalSellDetails(BaseModel):
    price_per_acre: float
    negotiable: bool
    address: str
    total_area: float
    available_area: float
    description: Optional[str] = ""

# ========== Main Property Model ==========

class PropertyInput(BaseModel):
    category: str  # "residential", "commercial", "agricultural"
    subcategory: str  # "rent", "sell", "lease"
    title: str
    images: List[str] = []

    # Optional Details for Conditional Fields
    residential_sell: Optional[ResidentialSellDetails] = None
    residential_rent: Optional[ResidentialRentDetails] = None
    commercial_rent: Optional[CommercialRentDetails] = None
    commercial_sell: Optional[CommercialSellDetails] = None
    agricultural_lease: Optional[AgriculturalLeaseDetails] = None
    agricultural_sell: Optional[AgriculturalSellDetails] = None

# ========== API Endpoint ==========

@router.post("/api/properties", status_code=201)
async def add_property(
    payload: PropertyInput,
    user: dict = Depends(get_current_user)
):
    if user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add properties.")

    property_doc = {
        "category": payload.category,
        "subcategory": payload.subcategory,
        "title": payload.title,
        "images": payload.images,
        "email": user["email"],
        "city": user.get("city", ""),
        "created_at": datetime.utcnow(),
        "views": 0,
        "watchlist": 0,
        "inquiries": [],
        "active": True,
        "status": "pending approval",
        "review_comment": "",
    }

    # Inject correct data based on category/subcategory
    if payload.category == "residential":
        if payload.subcategory == "sell" and payload.residential_sell:
            property_doc.update(payload.residential_sell.dict())
        elif payload.subcategory == "rent" and payload.residential_rent:
            property_doc.update(payload.residential_rent.dict())
        else:
            raise HTTPException(status_code=400, detail="Missing residential details.")

    elif payload.category == "commercial":
        if payload.subcategory == "sell" and payload.commercial_sell:
            property_doc.update(payload.commercial_sell.dict())
        elif payload.subcategory == "rent" and payload.commercial_rent:
            property_doc.update(payload.commercial_rent.dict())
        else:
            raise HTTPException(status_code=400, detail="Missing commercial details.")

    elif payload.category == "agricultural":
        if payload.subcategory == "sell" and payload.agricultural_sell:
            property_doc.update(payload.agricultural_sell.dict())
        elif payload.subcategory == "lease" and payload.agricultural_lease:
            property_doc.update(payload.agricultural_lease.dict())
        else:
            raise HTTPException(status_code=400, detail="Missing agricultural details.")

    else:
        raise HTTPException(status_code=400, detail="Invalid property category.")
    print("📦 Inserting property:", property_doc)
    result = properties_collection.insert_one(property_doc)
    # Fetch pending properties for moderation
    # get_pending_properties()
    moderation_data = get_pending_properties()

    string_data = json.dumps(moderation_data, indent=2)
    print("Stringified Data:")
    print(string_data)
    
    result = await Runner.run(moderation_agent, string_data)  # list[TResponseInputItem]
    print(result.final_output)
    update_property_status(result.final_output)
    print("Property status updated successfully.")


    return {
        "message": "✅ Property added successfully",
        "property_id": str(result.inserted_id)
    }

