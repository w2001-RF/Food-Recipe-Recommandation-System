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
