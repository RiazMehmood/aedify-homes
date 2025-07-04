from agents_folder.moderation_agent import moderation_agent
from prompts.agent_prompts import customer_agent_prompt
from models.pydantic_models import UserInfo
from agents import Agent
from agent_tools.tools_archieve import (
    featuredOffers,
    futurePropertyFinder,
    searchProperty,
    onOffer,
    contactSeller,
    offerAccepted
)

customer_agent: Agent[UserInfo] = Agent(
    name="RealEstate Customer",
    instructions=customer_agent_prompt,
    model="gemini-2.5-flash-lite-preview-06-17",
    tools=[
        featuredOffers,
        futurePropertyFinder,
        searchProperty,
        onOffer,
        contactSeller,
        offerAccepted,
        moderation_agent.as_tool(
            tool_name="moderation_agent",
            tool_description="Moderation agent for property listings."
        )
    ]
)