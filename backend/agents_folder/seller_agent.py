from agents import Agent
from prompts.agent_prompts import seller_agent_prompt
from models.pydantic_models import UserInfo
from agents_folder.moderation_agent import moderation_agent
from agents.tools_archieve import (
    addProperty,
    updateProperty,
    subscriber
)



seller_agent: Agent[UserInfo] = Agent(
    name="RealEstate Seller",
    description="Agent specialized in selling real estate properties.",
    instructions=seller_agent_prompt,
    model="gemini-2.5-flash-lite-preview-06-17",
    tools=[
        addProperty,
        updateProperty,
        subscriber,
        moderation_agent.as_tool()
    ]
)