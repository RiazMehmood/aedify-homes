from agents_folder import moderation_agent
from prompts.agent_prompts import customer_agent_prompt
from models.pydantic_models import UserInfo
from agents.tools_archieve import (
    featuredOffers,
    futurePropertyFinder,
    searchProperty,
    onOffer,
    contactSeller,
    offerAccepted
)

customer_agent: Agent[UserInfo] = Agent(
    name="RealEstate Customer",
    description="Agent specialized in assisting real estate customers.",
    instructions=customer_agent_prompt,
    model="gemini-2.5-flash-lite-preview-06-17",
    tools=[
        featuredOffers,
        futurePropertyFinder,
        searchProperty,
        onOffer,
        contactSeller,
        offerAccepted,
        moderation_agent.as_tool()
    ]
)