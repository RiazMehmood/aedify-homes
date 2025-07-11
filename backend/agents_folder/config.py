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

GEMINI_MODEL = LitellmModel(
        model="gemini/gemini-2.5-flash-preview-04-17",
        api_key=gemini_api_key,
    ),