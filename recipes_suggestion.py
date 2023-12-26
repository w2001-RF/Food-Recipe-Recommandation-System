from model import generate
from ImageFinder.ImageFinder import get_images_links as find_image
import asyncio

nutrition_values = [
    'Calories', 'FatContent', 'SaturatedFatContent',
    'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
    'FiberContent', 'SugarContent', 'ProteinContent'
]

async def generate_recipes_suggestions(dataframe, nutrition_list, number_of_recommendations, ingredients):
    params = {
        'n_neighbors': number_of_recommendations,
        'return_distance': False
    }

    loop = asyncio.get_event_loop()
    recommendations_coroutine = generate(dataframe, nutrition_list, ingredients, params)
    recommendations = await loop.create_task(recommendations_coroutine)

    if recommendations is None:
        return None

    result = []
    for recipe in recommendations:
        result.append({
            "Recipe_Id": recipe["RecipeId"],
            "Recipe_Name": recipe["Name"],
            "Recipe_Image_link": recipe["Image_link"],
            "Recipe_nutritions_values": {
                value: recipe[value]
                for value in nutrition_values
            },
            "RecipeIngredients": [
                ingredient
                for ingredient in recipe['RecipeIngredientParts']
            ],
            "RecipeInstructions": [
                instruction
                for instruction in recipe['RecipeInstructions']
            ],
            "CookTime": f'{recipe["CookTime"]} min',
            "PrepTime": f'{recipe["PrepTime"]} min',
            "TotalTime": f'{recipe["TotalTime"]} min'
        })

    return result

