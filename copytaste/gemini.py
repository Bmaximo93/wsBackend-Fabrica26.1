
from django.conf import settings
from google import genai
from google.genai import types
from pydantic import BaseModel
import time

client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.5-flash"

PROMPT = (
    "Watch the provided video and extract the recipe if one exists. "
    "If the ingredients and steps are not explicitly provided or if the video has no narration, try to carefully infer ingredients and steps from the visual content. "
    "Return all text fields (title, description, ingredients, steps) in Brazilian portuguese. "
    "try to infer duration if no duration is provided in the video, if duration cannot be reasonably inferred, set duration_minutes to none "
    "Set is_recipe to false and leave all other fields as empty strings or empty lists if the video does not contain a recipe. "
    "Do not invent or fabricate ingredients or steps that are not present in the video. "
    "Do not include promotional content, brand names, or links in the recipe. "
    "Do not include quantities in the ingredients list as a separate field, keep them together with the ingredient name. "
    "Avoid merging multiple steps into one, keep each step as separate, atomic actions"
    "If the video contains multiple recipes, extract only the main one or the first"
)

class RecipeSchema(BaseModel):
    # Schema pydantic para output estruturado do gemini
    is_recipe: bool
    title: str
    description: str
    ingredients: list[str]
    steps: list[str]
    duration_minutes: int | None

# proc. de shorts: ~8seg
# proc. de um video de 15 minutos: ~2min 💀💀
# aproximadamente 8 segundos por minuto de video
# TODO: ver se processamento de vídeo longo vai causar timeout no deploy
# TODO: se der tempo, tentar implementar processamento assíncrono
def extract_recipe_from_video(url: str):

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_uri(file_uri=url, mime_type="video/youtube"),
            PROMPT,
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": RecipeSchema,
        },
    )

    recipe = RecipeSchema.model_validate_json(response.text)

    if not recipe.is_recipe:
        raise ValueError("O video fornecido não parece conter uma receita")

    return recipe

# TODO: tentar implementar estimativa de tempo de processamento para feedback
#  def get_video_duration(url: str):


def test_gemini():

    inicio = time.time()
    result = extract_recipe_from_video('https://www.youtube.com/watch?v=JxUSzM29Y3M')
    fim = time.time()

    print(f'is_recipe: {result.is_recipe}')
    print(f'titulo: {result.title}')
    print(f'descrição: {result.description}')
    print(f'ingredientes: {result.ingredients}')
    print(f'passos: {result.steps}')
    print(f'duração: {result.duration_minutes} min')
    print(f'\ntempo de processamento: {fim - inicio}s')

