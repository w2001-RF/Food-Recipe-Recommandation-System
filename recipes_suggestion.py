from model import generate
from ImageFinder.ImageFinder import get_images_links as find_image

nutrition_values = [
    'Calories', 'FatContent', 'SaturatedFatContent',
    'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
    'FiberContent', 'SugarContent', 'ProteinContent'
]

def generate_recipes_suggestions(dataframe, nutrition_list,  number_of_recommendations, ingredients):

    params = {
        'n_neighbors': number_of_recommendations,
        'return_distance': False
    }

    recommendations = generate(dataframe, nutrition_list, ingredients, params)

    if recommendations is None:
        return None

    return [
        {
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
            # "RecipeIngredientQuantities": [
            #     quantity
            #     for quantity in recipe['RecipeIngredientQuantities']
            # ],
            "RecipeInstructions": [
                instruction
                for instruction in recipe['RecipeInstructions']
            ],
            "CookTime": f'{recipe["CookTime"]} min',
            "PrepTime": f'{recipe["PrepTime"]} min',
            "TotalTime": f'{recipe["TotalTime"]} min'
        }
        for recipe in recommendations
    ]
