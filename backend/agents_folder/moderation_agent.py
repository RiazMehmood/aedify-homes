from agents import Agent
from models.pydantic_models import (UserInfo, PropertyModerationOutput)
from prompts.agent_prompts import verifier_agent_prompt

moderation_agent: Agent[UserInfo] = Agent(
    name="RealEstate Verifier",
    instructions=verifier_agent_prompt,
    model="gemini-2.5-flash-lite-preview-06-17",
    output_type=PropertyModerationOutput

)