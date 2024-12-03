from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = FastAPI()

# Spoonacular API key from .env file
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Conversational Recipe Innovation Bot API. Use /generate_recipe/ to get started."}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")

class RecipeRequest(BaseModel):
    ingredients: list
    preferences: dict

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
