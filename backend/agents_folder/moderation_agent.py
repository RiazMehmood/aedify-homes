from agents import Agent
from models.pydantic_models import UserInfo, PropertyModerationOutput
from prompts.agent_prompts import moderation_agent_prompt
from agents.tools_archieve import (
    queryDatabase,
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
        queryDatabase,
        pendingApproval,
        updatePendingApproval,
        AISuggestions
    ]
)