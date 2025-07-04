from agents import Agent
from models.pydantic_models import UserInfo, PropertyModerationOutput
from prompts.agent_prompts import moderation_agent_prompt
from agent_tools.tools_archieve import (
    queryDataBase,
    pendingApproval,
    updatePendingApproval,
    AISuggestions
)



moderation_agent: Agent[UserInfo] = Agent(
    name="RealEstate moderator",
    instructions=moderation_agent_prompt,
    model="gemini-2.5-flash-lite-preview-06-17",
    output_type=PropertyModerationOutput,
    tools=[
        queryDataBase,
        pendingApproval,
        updatePendingApproval,
        AISuggestions
    ]
)