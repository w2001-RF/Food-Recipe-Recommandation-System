from random import uniform as rnd
from ImageFinder.ImageFinder import get_images_links as find_image
from model import generate


Weights = {
    "Maintain weight": 1,
    "Mild weight loss": 0.9,
    "Weight loss": 0.8,
    "Extreme weight loss": 0.6
}
nutritions_values = [
    'Calories', 'FatContent', 'SaturatedFatContent',
    'CholesterolContent', 'SodiumContent', 'CarbohydrateContent',
    'FiberContent', 'SugarContent', 'ProteinContent'
]
losses = ['-0 kg/week', '-0.25 kg/week', '-0.5 kg/week', '-1 kg/week']


def generate_recommendations(dataframe, person):
    total_calories = Weights[person.weight_loss_plan] * \
        person.calories_calculator()
    recommendations = []
    for meal in person.meals_calories_perc:
        meal_calories = person.meals_calories_perc[meal] * total_calories
        if meal == 'breakfast':
            recommended_nutrition = [meal_calories, rnd(10, 30), rnd(0, 4), rnd(
                0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 10), rnd(0, 10), rnd(30, 100)]
        elif meal == 'launch':
            recommended_nutrition = [meal_calories, rnd(20, 40), rnd(0, 4), rnd(
                0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(50, 175)]
        elif meal == 'dinner':
            recommended_nutrition = [meal_calories, rnd(20, 40), rnd(0, 4), rnd(
                0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(50, 175)]
        else:
            recommended_nutrition = [meal_calories, rnd(10, 30), rnd(0, 4), rnd(
                0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 10), rnd(0, 10), rnd(30, 100)]

        recommended_recipes = generate(dataframe, recommended_nutrition)
        recommendations.append(recommended_recipes)

    return recommendations


def generate_repas_programme(dataframe, person):
    bmi_string, category = person.get_bmi_string_and_category()
    maintain_calories = person.calories_calculator()
    meals = person.meals_calories_perc
    recommendations = generate_recommendations(dataframe, person)

    if recommendations is None:
        return None

    return {
        "BMI": bmi_string,
        "BMICategory": category,
        "CaloriesPerDay": f'{round(maintain_calories * Weights[person.weight_loss_plan])} Calories/day',
        "Repas_Programme": {
            meal_name: [
                {
                    "Recipe_Id": recipe["RecipeId"],
                    "Recipe_Name": recipe["Name"],
                    "Recipe_Image_link": recipe["Image_link"],
                    "Recipe_nutritions_values": {
                        value: recipe[value]
                        for value in nutritions_values
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
                for recipe in recommendation
            ]
            for meal_name, recommendation in zip(meals, recommendations)
        }
    }
