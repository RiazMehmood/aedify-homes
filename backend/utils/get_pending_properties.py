from typing import Union
from agents import TResponseInputItem
from models.pydantic_models import PropertyModerationInput
from db.mongo import properties_collection
from bson import ObjectId
from datetime import datetime
from pprint import pprint


def get_pending_properties() -> list[TResponseInputItem]:
    pending_properties = list(properties_collection.find({"status": "pending approval"}))

    print("\n📦 Pending Properties Extracted:")
    output_models = []

    for prop in pending_properties:
        model = PropertyModerationInput(
            property_id=str(prop["_id"]),
            category=prop.get("category", ""),
            subcategory=prop.get("subcategory", ""),
            title=prop.get("title", ""),
            images=prop.get("images", []),
            email=prop.get("email", ""),
            city=prop.get("city", ""),
            created_at=str(prop.get("created_at", datetime.utcnow())),
            description=prop.get("description", ""),
            status=prop.get("status", "pending approval"),
            review_comment=prop.get("review_comment", ""),
        )
        output_models.append(model.dict())

    for model_dict in output_models:
        pprint(model_dict)

    return output_models  # This is a list[dict] → valid as list[TResponseInputItem]
