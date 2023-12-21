from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist, ValidationError, validator
from typing import Dict, List, Optional
import pandas as pd
from recipes_suggestion import generate_recipes_suggestions
from repas_suggestion import generate_repas_programme
from Person import Person
from model import get_similar_recipe, generate

dataset = pd.read_csv('./Data/dataset.csv', compression='gzip')

app = FastAPI()


class params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False


class Recipe(BaseModel):
    Recipe_Name: str
    Recipe_Image_link: str
    Recipe_nutritions_values: Dict[str, float]
    RecipeIngredients: List[str]
    RecipeInstructions: List[str]
    CookTime: str
    PrepTime: str
    TotalTime: str

    @validator('Recipe_nutritions_values')
    def validate_nutrition_keys(cls, value):
        required_keys = [
            'Calories', 'FatContent', 'SaturatedFatContent',
            'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
            'FiberContent', 'SugarContent', 'ProteinContent'
        ]

        if set(value.keys()) != set(required_keys):
            raise ValidationError("Invalid nutrition keys")

        return value


class RecipePredictionIn(BaseModel):
    nutrition_input: conlist(float, min_items=9, max_items=9)
    number_of_recommendations: int
    ingredients: List[str] = []


class RecipePredictionOut(BaseModel):
    Message: str
    output: Optional[List[Recipe]] = None


@app.get("/")
def home():
    return {"Food Recommendation System": "OK"}


@app.post("/Recipe_suggestions/", response_model=RecipePredictionOut)
def predict_recipes(prediction_input: RecipePredictionIn):
    # try:
    output = generate_recipes_suggestions(
        dataset,
        prediction_input.nutrition_input,
        prediction_input.number_of_recommendations,
        prediction_input.ingredients
    )

    if output is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "Message": "Get recipes successfully",
        "output": output
    }

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


class RepasPredictionIn(BaseModel):
    age: int
    height: int
    weight: int
    gender: str
    activity: str
    number_of_meals: int
    weight_loss_plan: str


class NutritionProgramme(BaseModel):
    BMI: str
    BMICategory: str
    CaloriesPerDay: str
    Repas_Programme: Dict[str, List[Recipe]]


class RepasPredictionOut(BaseModel):
    Message: str
    output: Optional[NutritionProgramme] = None

@app.post("/Repas_suggestions/", response_model=RepasPredictionOut)
def predict_repas(prediction_input: RepasPredictionIn):
    try:
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
             raise HTTPException(status_code=404, detail="Not found")
        else:
            return {
                "Message": "Get recipes successfully",
                "output": output
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SimilarRecipeInput(BaseModel):
    recipe_info: Recipe
    number: int
    num_similar: int


class SimilarRecipeOutput(BaseModel):
    Message: str
    output: Optional[List[Recipe]] = None

@app.post("/get_similar_recipe/", response_model=SimilarRecipeOutput)
def get_similar_recipe_endpoint(similar_recipe_input: SimilarRecipeInput):
    try:
        recipe_info = similar_recipe_input.recipe_info
        number = similar_recipe_input.number
        num_similar = similar_recipe_input.num_similar

        similar_recipes = get_similar_recipe(dataset,
                                             recipe_info.dict(),
                                             number,
                                             num_similar)

        if similar_recipes is not None:
            return {
                "Message": "Get similar recipes successfully",
                "output": similar_recipes
            }
        else:
            raise HTTPException(status_code=404, detail="Not found")


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
