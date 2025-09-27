
import os
from agents import OpenAIChatCompletionsModel, RunConfig,AsyncOpenAI, ModelProvider, Model
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME='gemini-2.5-flash'

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta",
)
class CustomModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=model_name or MODEL_NAME, openai_client=external_client)

CUSTOM_MODEL_PROVIDER = CustomModelProvider()

config = RunConfig(model_provider=CUSTOM_MODEL_PROVIDER)