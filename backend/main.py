import json
from utils.update_property_status import update_property_status
from models.pydantic_models import PropertyModerationOutput
from utils.get_pending_properties import get_pending_properties
from prompts.agent_prompts import assistant_instructions
from routes import (images, properties, auth)
from fastapi import FastAPI, Request, Depends
from models.pydantic_models import UserInfo
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
from pydantic import BaseModel
from agents import (
    Agent,
    set_default_openai_api,
    ItemHelpers,
    set_default_openai_client,
    AsyncOpenAI,
    Runner,
    set_tracing_disabled,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    TResponseInputItem,
    input_guardrail,
    function_tool,
    RunConfig,
    OpenAIChatCompletionsModel,
)
from routes.auth import get_current_user
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables")

gemini_api_key = api_key
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(external_client)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite-preview-06-17",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# FastAPI app setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class RealEstateInput(BaseModel):
    is_real_estate_query: bool
    query: str

class Input(BaseModel):
    value: str

app.include_router(auth.router, prefix="/api/auth")
app.include_router(properties.router)
app.include_router(images.router)


# Guardrail agent
guardrail_agent: Agent[UserInfo] = Agent(
    name="RealEstate Guardrail",
    instructions=(
        "Determine if the user's message is either:\n"
        "1. A real estate related query (buying, selling, renting, pricing, etc.) OR\n"
        "2. A greeting (e.g., 'hi', 'hello', 'how are you').\n"
        "Set 'is_real_estate_query' to true if either condition is met."
    ),
    output_type=RealEstateInput,
    model="gemini-2.5-flash-lite-preview-06-17"
)

@input_guardrail
async def real_estate_input_guardrail(
    ctx: RunContextWrapper[UserInfo],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_real_estate_query
    )

# 🔧 Real estate task tools
@function_tool
def handle_buying(wrapper: RunContextWrapper[UserInfo], query: str) -> str:
    return (
        f"{wrapper.context.name} You're looking to buy a property. Please provide:\n"
        "- Location\n- Budget\n- Property type (e.g., house, shop, plot)\n"
        "- Your name, address, phone number, and email."
    )

@function_tool
def handle_selling(wrapper: RunContextWrapper[UserInfo], query: str) -> str:
    return (
        f"{wrapper.context.name} You're looking to sell a property. Please provide:\n"
        "- Property location\n- Property details (e.g., size, type)\n"
        "- Your contact information (name, phone, email)."
    )

@function_tool
def handle_searching(wrapper: RunContextWrapper[UserInfo], query: str) -> str:
    return (
        f"Greet, {wrapper.context.name} with friendly greetings.\n"
        f"Are you looking for a property in {wrapper.context.city} where you live, "
        "or anywhere else? I can search accordingly."
    )




# 👨‍💼 Assistant agent with tool access
assistant_agent: Agent[UserInfo] = Agent(
    name="RealEstate Assistant",
    instructions=assistant_instructions,
    model="gemini-2.5-flash-lite-preview-06-17",
    input_guardrails=[real_estate_input_guardrail],
    tools=[
        handle_buying,
        handle_selling,
        handle_searching
    ]
)



# 🧪 Test endpoint (optional)
@app.post("/chat")
async def agent_endpoint(input: Input, request: Request, user: dict = Depends(get_current_user)):
    user_info = UserInfo(
        name=user.get("name", "User"),
        city=user.get("city", ""),
        role=user.get("role", ""),
        whatsapp=user.get("whatsapp")
    )
    try:
        result = await Runner.run(assistant_agent, input.value, max_turns=2, context=user_info)
        return {"result": result.final_output}
    except InputGuardrailTripwireTriggered:
        return {"result": "I only handle real estate queries."}
# 🔁 Manual test
async def main():
    try:
        moderation_data = get_pending_properties()

        string_data = json.dumps(moderation_data, indent=2)
        print("Stringified Data:")
        print(string_data)
        # Wrap each item as TResponseInputItem
        # formatted_items = [TResponseInputItem(content=dumps(item)) for item in moderation_data]

        # Then run them
        
        # result = await Runner.run(verifier_agent, string_data)  # list[TResponseInputItem]
        # print(result.final_output)
        # update_property_status(result.final_output)
        # print("Property status updated successfully.", update_property_status(result.final_output))


        print("🔍 RealEstate Assistant (Type 'exit' to quit)")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            result = await Runner.run(assistant_agent, user_input)
            print("Guardrail Not Triggered")
            print(f"🤖 Agent: {result.final_output}")
    except InputGuardrailTripwireTriggered:
        print("Guardrail Triggered")
        print("I only handle real estate queries.")

if __name__ == "__main__":
    asyncio.run(main())