from agents import Agent
from .config import GEMINI_MODEL
from prompts.agent_prompts import guardrail_agent_prompt
from models.pydantic_models import UserInfo, RealEstateInput


# Guardrail agent
guardrail_agent: Agent[UserInfo] = Agent(
    name="RealEstate Guardrail",
    instructions=guardrail_agent_prompt,
    output_type=RealEstateInput,
    model=GEMINI_MODEL,
)