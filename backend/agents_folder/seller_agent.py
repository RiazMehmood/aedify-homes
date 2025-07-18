from .config import GEMINI_MODEL
from prompts.agent_prompts import seller_agent_prompt
from models.pydantic_models import UserInfo
from agents_folder.moderation_agent import moderation_agent
from agents import Agent
from agent_tools.tools_archieve import (
    addProperty,
    updateProperty,
    subscriber
)

from dotenv import load_dotenv
import os
import litellm
from agents.extensions.models.litellm_model import LitellmModel
from agents import set_tracing_disabled

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables")

gemini_api_key = api_key
set_tracing_disabled(True)
litellm.disable_aiohttp_transport = True 


seller_agent: Agent[UserInfo] = Agent(
    name="RealEstate Seller",
    instructions=seller_agent_prompt,
    model=LitellmModel(
        model="gemini/gemini-2.5-flash-preview-04-17",
        api_key=gemini_api_key,
    ),
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