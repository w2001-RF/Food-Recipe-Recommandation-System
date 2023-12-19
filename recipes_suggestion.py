from model import generate
from ImageFinder.ImageFinder import get_images_links as find_image

class Recommendation:
    def __init__(self,dataframe, nutrition_list,nb_recommendations,ingredient_txt):
        self.nutrition_list=nutrition_list
        self.nb_recommendations=nb_recommendations
        self.ingredient_txt=ingredient_txt
        self.dataframe = dataframe
        pass

    def generate(self,):
        params={'n_neighbors':self.nb_recommendations,'return_distance':False}
        ingredients=self.ingredient_txt.split(';')
        recommendations = generate(self.dataframe,
                                   self.nutrition_list,ingredients,
                                   params)

        if recommendations!=None:
            for recipe in recommendations:
                recipe['image_link']=find_image(recipe['Name'])
        return recommendations
