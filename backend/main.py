from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

class RecipeRequest(BaseModel):
    ingredients: list
    preferences: dict

# Replace with your actual Spoonacular API key
SPOONACULAR_API_KEY = "6bc071b43c9a4095addce64b7bce951f"

@app.post("/generate_recipe/")
async def generate_recipe(request: RecipeRequest):
    base_url = "https://api.spoonacular.com/recipes/complexSearch"
    response = requests.get(
        base_url,
        params={
            "apiKey": SPOONACULAR_API_KEY,
            "includeIngredients": ",".join(request.ingredients),
            "diet": request.preferences.get("diet", None),
            "number": 5,
        },
    )
    if response.status_code == 200:
        recipes = response.json().get("results", [])
        return {"recipes": recipes}
    return {"error": "Failed to fetch recipes"}

@app.get("/healthcheck/")
def healthcheck():
    return {"status": "OK"}