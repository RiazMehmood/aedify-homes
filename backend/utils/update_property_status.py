from pprint import pprint
from bson import ObjectId
from db.mongo import properties_collection
from models.pydantic_models import PropertyModerationOutput



def update_property_status(data: PropertyModerationOutput) -> dict:

    object_id = ObjectId(data.property_id)

    # Check if property exists before update
    property_data = properties_collection.find_one({"_id": object_id})

    if not property_data:
        return {"success": False, "message": "Property not found with given ID."}

    pprint({"Before Update": property_data})

    result = properties_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": data.status,
                "review_comment": data.review_comment
            }
        }
    )

    updated_data = properties_collection.find_one({"_id": object_id})
    pprint({"After Update": updated_data})

    if result.modified_count == 1:
        return {"success": True, "message": "Property updated successfully"}
    else:
        return {"success": False, "message": "No update performed. Values may be unchanged."}
