from jose import jwt, JWTError
from utils.websocket import connect_client, disconnect_client
from models.pydantic_models import Input
from routes import (images, properties, auth)
from fastapi import FastAPI, Request, Depends, WebSocket, Query
from models.pydantic_models import UserInfo
from agents_folder.customer_agent import customer_agent
from agents_folder.seller_agent import seller_agent
from agents_folder.guardrail_agent import guardrail_agent
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import get_current_user
from dotenv import load_dotenv
import asyncio
import os
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
    RunConfig,
    OpenAIChatCompletionsModel,
)

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


app.include_router(auth.router, prefix="/api/auth")
app.include_router(properties.router)
app.include_router(images.router)


# SECRET_KEY = os.getenv("NEXTAUTH_SECRET")
# ALGORITHM = "HS256"


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
#     try:
#         # Decode JWT from query parameter
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("email")

#         if not email:
#             await websocket.close(code=1008)
#             return

#         # Accept and register this client
#         await connect_client(email, websocket)

#         while True:
#             await websocket.receive_text()  # Keeps the connection alive

#     except JWTError:
#         await websocket.close(code=1008)

#     except Exception:
#         await websocket.close(code=1011)
#         await disconnect_client(email)



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





# 🧪 Test endpoint (optional)
@app.post("/chat")
async def agent_endpoint(input: Input, request: Request, user: dict = Depends(get_current_user)):
    user_info = UserInfo(
        name=user.get("name", "User"),
        city=user.get("city", ""),
        role=user.get("role", ""),
        whatsapp=user.get("whatsapp")
    )
    
    # Determine agent based on user role
    if user_info.role == "customer":
        print(f"User {user_info.name} is a customer.")
        agent = customer_agent
    elif user_info.role == "seller":
        print(f"User {user_info.name} is a seller.")
        agent = seller_agent
    else:
        return {"result": "Your role is not recognized. Please contact support."}

    try:
        result = await Runner.run(agent, input.value, max_turns=2, context=user_info)
        return {"result": result.final_output}
    except InputGuardrailTripwireTriggered:
        return {"result": "I only handle real estate queries."}
   
# 🔁 Manual test
async def main():
    try:
        print("🔍 RealEstate Assistant (Type 'exit' to quit)")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            result = await Runner.run(customer_agent, user_input)
            print("Guardrail Not Triggered")
            print(f"🤖 Agent: {result.final_output}")
    except InputGuardrailTripwireTriggered:
        print("Guardrail Triggered")
        print("I only handle real estate queries.")

if __name__ == "__main__":
    asyncio.run(main())