from pprint import pprint
from bson import ObjectId
from db.mongo import properties_collection
from models.pydantic_models import PropertyModerationOutput, UserInfo
from agents import function_tool, RunContextWrapper


@function_tool
def update_property_status(wrapper: RunContextWrapper[UserInfo], data: PropertyModerationOutput) -> dict:

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


#Seller Agent Tools
@function_tool
def addProperty(wrapper: RunContextWrapper[UserInfo] ) -> dict:
    """
    Add a new property to the database.
    """
    return 
    
@function_tool
def pendingApproval(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Mark a property as pending approval.
    """
    object_id = ObjectId(property_id)
    result = properties_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": "pending_approval"}}
    )
    if result.modified_count == 1:
        return {"success": True, "message": "Property marked as pending approval"}
    else:
        return {"success": False, "message": "Failed to mark property as pending approval"}

@function_tool
def updatePendingApproval(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Update a pending approval property.
    """
    return {"success": False, "message": "Failed to update pending approval property"}  
    
@function_tool
def AISuggestions(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Add AI suggestions to a property.
    """
    return {"success": False, "message": "Failed to add AI suggestions"}    
    
@function_tool
def updateProperty(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Update an existing property.
    """
    return {"success": False, "message": "Failed to update property"}   
    

@function_tool
def subscriber(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Get subscribers for a property.
    """
    object_id = ObjectId(property_id)
    property_data = properties_collection.find_one({"_id": object_id}, {"subscribers": 1})
    
    if property_data and "subscribers" in property_data:
        return {"success": True, "subscribers": property_data["subscribers"]}
    else:
        return {"success": False, "message": "No subscribers found or property does not exist"} 
    

# Customer Agent Tools

@function_tool
def featuredOffers(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Get featured offers for a property.
    """
    object_id = ObjectId(property_id)
    property_data = properties_collection.find_one({"_id": object_id}, {"featured_offers": 1})
    
    if property_data and "featured_offers" in property_data:
        return {"success": True, "featured_offers": property_data["featured_offers"]}
    else:
        return {"success": False, "message": "No featured offers found or property does not exist"} 
    
@function_tool
def futurePropertyFinder(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Get future property finder details for a property.
    """
    object_id = ObjectId(property_id)
    property_data = properties_collection.find_one({"_id": object_id}, {"future_property_finder": 1})
    
    if property_data and "future_property_finder" in property_data:
        return {"success": True, "future_property_finder": property_data["future_property_finder"]}
    else:
        return {"success": False, "message": "No future property finder details found or property does not exist"}  
    
@function_tool
def searchProperty(wrapper: RunContextWrapper[UserInfo]) -> dict:
    """
    Search for properties based on given criteria.
    """
    return {"success": False, "message": "No properties found matching the criteria"}   
    
@function_tool
def onOffer(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Submit an offer for a property.
    """
    return {"success": False, "message": "Failed to submit offer or property does not exist"}   
    
@function_tool
def contactSeller(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Contact the seller of a property.
    """
    return {"success": False, "message": "Failed to send contact request or property does not exist"}   
    
@function_tool
def queryDataBase(wrapper: RunContextWrapper[UserInfo]) -> dict:
    """
    Query the database for properties based on given criteria.
    """
    return {"success": False, "message": "No properties found matching the query"}  
    
@function_tool
def offerAccepted(wrapper: RunContextWrapper[UserInfo], property_id: str, offer_id: str) -> dict:
    """
    Accept an offer for a property.
    """
    object_id = ObjectId(property_id)
    result = properties_collection.update_one(
        {"_id": object_id, "offers._id": ObjectId(offer_id)},
        {"$set": {"offers.$.status": "accepted"}}
    )
    
    if result.modified_count == 1:
        return {"success": True, "message": "Offer accepted successfully"}
    else:
        return {"success": False, "message": "Failed to accept offer or property/offer does not exist"} 
    
