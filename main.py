from fastapi import FastAPI
from pydantic import BaseModel, conlist
from typing import Dict, List, Optional
import pandas as pd
from recipes_suggestion import generate_recipes_suggestions
from repas_suggestions import generate_repas_programme
from Person import Person

dataset = pd.read_csv('./Data/dataset.csv', compression='gzip')

app = FastAPI()


class params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False


class Recipe(BaseModel):
    Recipe_Name: str
    Recipe_Image_link: str
    Recipe_nutritions_values: conlist(float, min_items=9, max_items=9)
    RecipeIngredient: List[str]
    RecipeInstructions: List[str]
    CookTime: str
    PrepTime: str
    TotalTime: str


class RecipePredictionIn(BaseModel):
    nutrition_input: conlist(float, min_items=9, max_items=9)
    number_of_recommendations: int
    ingredients: List[str] = []


class RecipePredictionOut(BaseModel):
    Message: str
    output: Optional[List[Recipe]] = None


class RepasPredictionIn(BaseModel):
    age: int
    height: int
    weight: int
    gender: str
    activity: str
    number_of_meals: int
    weight_loss_plan: str
    nutrition_input: conlist(float, min_items=9, max_items=9)
    ingredients: List[str] = []
    params: Optional[params]


class NutritionProgramme(BaseModel):
    BMI: str
    BMICategory: str
    CaloriesPerDay: str
    Repas_Programme: Dict[str, List[Recipe]]


class RepasPredictionOut(BaseModel):
    Message: str
    output: Optional[NutritionProgramme] = None


@app.get("/")
def home():
    return {"Food Recommendation System": "OK"}


@app.post("/Recipe_suggestions/", response_model=RecipePredictionOut)
def predict_recipes(prediction_input: RecipePredictionIn):
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
            "Message": "Get recipes successfully",
            "output": output
        }


@app.post("/Repas_suggestions/", response_model=RepasPredictionOut)
def predict_repas(prediction_input: RepasPredictionIn):
    age = RepasPredictionIn.age
    height = RepasPredictionIn.height
    weight = RepasPredictionIn.weight
    gender = RepasPredictionIn.gender
    activity = RepasPredictionIn.activity
    number_of_meals = RepasPredictionIn.number_of_meals

    if number_of_meals == 3:
        meals_calories_perc = {
            'breakfast': 0.35,
            'lunch': 0.40,
            'dinner': 0.25
        }
    elif number_of_meals == 4:
        meals_calories_perc = {
            'breakfast': 0.30,
            'morning snack': 0.05,
            'lunch': 0.40,
            'dinner': 0.25
        }
    else:
        meals_calories_perc = {
            'breakfast': 0.30,
            'morning snack': 0.05,
            'lunch': 0.40,
            'afternoon snack': 0.05,
            'dinner': 0.20
        }

    weight_loss_plan = RepasPredictionIn.weight_loss_plan

    person = Person(
        age,
        height,
        weight,
        gender,
        activity,
        meals_calories_perc,
        weight_loss_plan
    )

    output = generate_repas_programme(dataset, person)

    if output is None:
        return {
            "Message": "Not found",
            "output": None
        }
    else:
        return {
            "Message": "Get recipes successfully",
            "output": output
        }
