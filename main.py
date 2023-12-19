from fastapi import FastAPI
from pydantic import BaseModel, conlist
from typing import List, Optional
import pandas as pd
from recipes_suggestion import generate_recipes_suggestions


dataset = pd.read_csv('./Data/dataset.csv', compression='gzip')

app = FastAPI()


class params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False

class Recipe(BaseModel):
    Recipe_Name:str
    Recipe_Image_link:str
    Recipe_nutritions_values:conlist(float, min_items=9, max_items=9)
    RecipeIngredientParts:list[str]

    RecipeInstructions:list[str]
    CookTime:str
    PrepTime:str
    TotalTime:str


class RecipePredictionIn(BaseModel):
    nutrition_input:conlist(float, min_items=9, max_items=9)
    number_of_recommendations:int
    ingredients:list[str]

class RecipePredictionOut(BaseModel):
    Message: str
    output: Optional[List[Recipe]] = None

@app.get("/")
def home():
    return {"Food Recommendation System": "OK"}

@app.post("/Recipe_suggestions/",response_model=RecipePredictionOut)
def predict_recipes(prediction_input:RecipePredictionIn):
    output = generate_recipes_suggestions(
        dataset,
        RecipePredictionIn.nutrition_list,
        RecipePredictionIn.number_of_recommendations,
        RecipePredictionIn.ingredients)

    if output is None:
        return {
            "Message": "Not found",
            "output": None
            }
    else:
        return {
            "Message" : "Get recipes successfully",
            "output": output
            }
