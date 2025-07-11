from fastapi import APIRouter, Depends, HTTPException
from db.mongo import properties_collection
from routes.auth import get_current_user
from datetime import datetime
from models.pydantic_models import PropertyInput

router = APIRouter()

from fastapi import Request
# ========== API Endpoint ==========

@router.post("/api/properties", status_code=201)
async def add_property(
    payload: PropertyInput,
    request: Request,
    user: dict = Depends(get_current_user)
):
    

    try:

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
            "views": 100,
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


        return {
            "message": "✅ Property added successfully",
            "property_id": str(result.inserted_id)
        }
    except Exception as e:
        body = await request.body()
        print("❌ Invalid Payload Recieved", body.decode())
        print("❌ Error Details:", e)



from bson import ObjectId


@router.get("/api/properties/me")
async def get_my_properties(user: dict = Depends(get_current_user)):
    if user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view their properties.")

    try:
        # 🟢 Sort by creation date (newest first)
        properties_cursor = properties_collection.find(
            {"email": user["email"]}
        ).sort("created_at", -1)

        properties = []
        for p in properties_cursor:
            p["id"] = str(p["_id"])
            p.pop("_id", None)
            properties.append(p)

        return properties

    except Exception as e:
        print("❌ Error fetching properties:", e)
        raise HTTPException(status_code=500, detail="Something went wrong.")