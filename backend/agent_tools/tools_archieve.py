from pprint import pprint
from bson import ObjectId
from utils.get_pending_properties import get_pending_properties
from db.mongo import properties_collection
from models.pydantic_models import PropertyModerationOutput, UserInfo
from agents import function_tool, RunContextWrapper
from utils.websocket import send_event
from db.mongo import properties_collection
from bson import ObjectId

def addPropertyErrorFunction(wrapper: RunContextWrapper[UserInfo], error: Exception) -> str:
    return {"status": error , "message": "There is some issue inside the addProperty tool."}


#Seller Agent Tools
@function_tool(failure_error_function=addPropertyErrorFunction)
async def addProperty(wrapper: RunContextWrapper[UserInfo]) -> dict:
    """
    Triggers the 'Add Property' button in the frontend via WebSocket.
    """
    email = wrapper.context.email
    if not email:
        return {"status": "error", "message": "User email not found in context"}

    # await trigger_add_property_modal(email)
    print("Trigger add Property initiated")
    await send_event(email, {
        "type": "open_add_property_modal"
    })
    return {"status": "success", "message": "Add Property modal triggered"}


@function_tool
async def pendingApproval(wrapper: RunContextWrapper[UserInfo]) -> dict:
    """
    Fetch all properties uploaded by the user with status 'pending approval'.
    """
    user_email = wrapper.context.email

    properties_cursor = properties_collection.find({
        "email": user_email,
        "status": "pending approval"
    })

    properties = []
    for p in properties_cursor:
        p["id"] = str(p["_id"])
        p.pop("_id", None)
        properties.append(p)

    return {
        "success": True,
        "pending_properties": properties,
        "count": len(properties)
    }


@function_tool
def updatePendingApproval(
    wrapper: RunContextWrapper[UserInfo],
    property_id: str,
    status: str,
    review_comment: str
) -> dict:
    """
    Update the status and review comment of a pending approval property.

    Parameters:
    - property_id: ID of the property to update.
    - status: 'approved' or 'not approved'.
    - review_comment: Moderation explanation and findings.
    """
    user_email = wrapper.context.email

    try:
        result = properties_collection.update_one(
            {
                "_id": ObjectId(property_id),
                "email": user_email,
                "status": "pending approval"
            },
            {
                "$set": {
                    "status": status,
                    "review_comment": review_comment
                }
            }
        )

        if result.matched_count == 0:
            return {
                "success": False,
                "message": "Property not found or not eligible for update."
            }

        # ✅ Notify frontend via WebSocket
        import asyncio
        asyncio.create_task(send_event(user_email, {
            "type": "moderation_updated",
            "property_id": property_id,
            "status": status,
            "review_comment": review_comment
        }))

        return {
            "success": True,
            "message": f"Property updated with status '{status}'."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update property: {str(e)}"
        }

    


@function_tool
async def updateProperty(wrapper: RunContextWrapper[UserInfo]):
    from utils.websocket import send_event
    await send_event(wrapper.context.email, {"type": "open_update_properties_modal"})
    return {"success": True, "message": "Modal opened"}

@function_tool
def queryDataBase(wrapper: RunContextWrapper[UserInfo]) -> dict:
    """
    Query the database for properties based on given criteria.
    """
    return {"success": False, "message": "No properties found matching the query"} 


@function_tool
def AISuggestions(wrapper: RunContextWrapper[UserInfo], property_id: str) -> dict:
    """
    Add AI suggestions to a property.
    """
    return {"success": False, "message": "Failed to add AI suggestions"}    
    

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
    
