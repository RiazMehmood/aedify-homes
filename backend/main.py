import asyncio
import os
import litellm
from utils.websocket import connect_client, disconnect_client
from jose import jwt, JWTError
from utils.websocket import connect_client, disconnect_client
from models.pydantic_models import Input
from routes import (images, properties, auth)
from fastapi import FastAPI, Request, Depends, WebSocket, Query, WebSocketDisconnect
from models.pydantic_models import UserInfo
from agents_folder.customer_agent import customer_agent
from agents_folder.seller_agent import seller_agent
from agents_folder.guardrail_agent import guardrail_agent
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import get_current_user
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    set_tracing_disabled,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    TResponseInputItem,
    input_guardrail,
)

# Load .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables")

gemini_api_key = api_key
set_tracing_disabled(True)
litellm.disable_aiohttp_transport = True # Disable aiohttp transport for litellm

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


SECRET_KEY = os.getenv("NEXTAUTH_SECRET")
ALGORITHM = "HS256"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    print("🔐 WebSocket request received")
    email = None  # define up front to access in finally block

    try:
        print("🔍 Decoding token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

        if not email:
            print("❌ Missing email in token.")
            await websocket.close(code=1008)
            return

        print(f"✅ Token verified. Email: {email}")
        await connect_client(email, websocket)
        print(f"📡 WebSocket connection established for: {email}")

        while True:
            try:
                message = await websocket.receive_text()
                if message == "ping":
                    continue  # just ignore pings
            except WebSocketDisconnect:
                print(f"🚫 Client disconnected: {email}")
                break
            except Exception as e:
                print(f"⚠️ Unexpected WebSocket error: {e}")
                break


    except WebSocketDisconnect as e:
        print(f"⚠️ WebSocketDisconnect: {e}")
        # no need to call websocket.close() here — it's already closed

    except Exception as e:
        print(f"⚠️ Unexpected WebSocket error: {e}")
        try:
            await websocket.close(code=1011)  # only close if not already closed
        except RuntimeError:
            print("⚠️ Tried to close already-closed WebSocket.")

    finally:
        if email:
            try:
                await disconnect_client(email)
            except Exception as disconnect_err:
                print(f"⚠️ Error during disconnect: {disconnect_err}")

# Input Guardrail for Real Estate Queries
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
        email=user.get("email", ""),
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
        result = await Runner.run(agent, input.value, max_turns=5, context=user_info)
        return {"result": result.final_output}
    except InputGuardrailTripwireTriggered:
        return {"result": "I only handle real estate queries."}


#                       Test Preparation code
# ---------------------------------------------------------------------
# from pydantic import BaseModel

# class AddInput(BaseModel):
#     x: int
#     y: int


# class Output(BaseModel):
#     first_number: int
#     second_number: int
#     operation: str
#     result: int





# test_agent: Agent = Agent(
#     name="Test Agent",
#     instructions="you are a test agent always use the provided tools for addition",
#     model=LitellmModel(
#         model="gemini/gemini-2.5-flash-preview-04-17",
#         api_key=gemini_api_key,
#     ),

# )



# # 🔁 Manual test
# async def main():
#     try:
#         print("🔍 RealEstate Assistant (Type 'exit' to quit)")
#         while True:
#             user_input = input("You: ")
#             if user_input.lower() == "exit":
#                 break
#             result = await Runner.run(test_agent, user_input)
#             print("Guardrail Not Triggered")
#             print(f"🤖 Agent: {result.final_output}")
#     except InputGuardrailTripwireTriggered:
#         print("Guardrail Triggered")
#         print("I only handle real estate queries.")

# if __name__ == "__main__":
#     asyncio.run(main())