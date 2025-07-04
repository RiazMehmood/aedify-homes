import json
from utils.update_property_status import update_property_status
from utils.get_pending_properties import get_pending_properties
from fastapi import APIRouter, Depends, HTTPException
from db.mongo import properties_collection
from routes.auth import get_current_user
from datetime import datetime
from agents import Runner
from agents_folder.moderation_agent import moderation_agent
from models.pydantic_models import ( ResidentialSellDetails, 
                                    ResidentialRentDetails, 
                                    CommercialRentDetails,
                                    CommercialSellDetails,
                                    AgriculturalLeaseDetails,
                                    AgriculturalSellDetails,
                                    PropertyInput)

router = APIRouter()

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
    
    agent_result = await Runner.run(moderation_agent, string_data)  # list[TResponseInputItem]
    print(agent_result.final_output)
    update_property_status(agent_result.final_output)
    print("Property status updated successfully.")


    return {
        "message": "✅ Property added successfully",
        "property_id": str(result.inserted_id)
    }

