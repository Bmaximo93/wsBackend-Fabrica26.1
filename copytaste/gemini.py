
from django.conf import settings
from google import genai
from google.genai import types
from pydantic import BaseModel

client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-3-flash"

PROMPT = (
    "Watch the provided video and extract the recipe if one exists. "
    "Return all text fields (title, description, ingredients, steps) in Brazilian portuguese. "
    "try to infer duration if no duration is provided in the video, if duration cannot be reasonably inferred, set duration_minutes to none "
    "Set is_recipe to false and leave all other fields as empty strings or empty lists if the video does not contain a recipe. "
)

class RecipeSchema(BaseModel):
    # Schema pydantic para output estruturado do gemini
    is_recipe: bool
    title: str
    description: str
    ingredients: list[str]
    steps: list[str]
    duration_minutes: int | None