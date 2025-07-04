from agents import Agent
from prompts.agent_prompts import seller_agent_prompt
from models.pydantic_models import UserInfo
from agents_folder.moderation_agent import moderation_agent
from agent_tools.tools_archieve import (
    addProperty,
    updateProperty,
    subscriber
)



seller_agent: Agent[UserInfo] = Agent(
    name="RealEstate Seller",
    instructions=seller_agent_prompt,
    model="gemini-2.5-flash-lite-preview-06-17",
    tools=[
        addProperty,
        updateProperty,
        subscriber,
        moderation_agent.as_tool(
            tool_name="moderation_agent",
            tool_description="Moderation agent for property listings."
        )
    ]
)