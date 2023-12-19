from model import generate
from ImageFinder.ImageFinder import get_images_links as find_image

nutrition_values = [
    'Calories','FatContent','SaturatedFatContent',
    'CholesterolContent','SodiumContent','CarbohydrateContent',
    'FiberContent','SugarContent','ProteinContent'
]

class Recommendation:
    def __init__(self,dataframe, nutrition_list,nb_recommendations,ingredients):
        self.nutrition_list=nutrition_list
        self.nb_recommendations=nb_recommendations
        self.ingredients=ingredients
        self.dataframe = dataframe
        pass

    def generate(self,):
        params={'n_neighbors':self.nb_recommendations,'return_distance':False}
        recommendations = generate(self.dataframe,
                                   self.nutrition_list,
                                   self.ingredients,
                                   params)

        if recommendations!=None:
            for recipe in recommendations:
                recipe['image_link']=find_image(recipe['Name'])
        return recommendations


def generate_recipes_suggestions(dataframe, nutrition_list,  number_of_recommendations, ingredients):
    recommendation=Recommendation(dataframe, nutrition_list, number_of_recommendations, ingredients)
    recommendations=recommendation.generate()

    return [
        {
            "Recipe_Name" : recipe["Name"],
            "Recipe_Image_link": recipe["Image_link"],
            "Recipe_nutritions_values": {
                value:[recipe[value]]
                for value in nutrition_values
            },
            "RecipesIngredients" : [
                ingredient
                for ingredient in recipe['RecipeIngredientParts']
            ],
            "RecipeInstructions" : [
                instruction
                for instruction in recipe['RecipeInstructions']
            ],
            "CookTime": f'{recipe["CookTime"]} min',
            "PreparationTime": f'{recipe["PrepTime"]} min',
            "TotalTime ": f'{recipe["TotalTime"]} min'
        }
        for recipe in recommendations
    ]
