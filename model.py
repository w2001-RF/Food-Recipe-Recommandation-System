import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.neighbors import NearestNeighbors
from ImageFinder.ImageFinder import get_images_links as find_image


def scaling(dataframe):
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 6:15].to_numpy())
    return prep_data, scaler


def build_pipeline(neigh, scaler, params):
    transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
    pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])
    return pipeline


async def extract_ingredient_filtered_data(dataframe, ingredients):
    if not ingredients or len(ingredients) == 0:
        return dataframe.copy()

    extracted_data = dataframe.copy()
    regex_string = ''.join(map(lambda x: f'(?=.*{x})', ingredients))
    extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(
        regex_string, regex=True, flags=re.IGNORECASE)]
    return extracted_data


def extract_quoted_strings(s):
    strings = re.findall(r'"([^"]*)"', s)
    return strings


async def recommend(dataframe, _input: list, ingredients=[], params={'n_neighbors': 5, 'return_distance': False}):
    extracted_data = await extract_ingredient_filtered_data(dataframe, ingredients)
    if extracted_data.shape[0] >= params['n_neighbors']:
        prep_data, scaler = scaling(extracted_data)
        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data)
        pipeline = build_pipeline(neigh, scaler, params)
        _input = np.array(_input).reshape(1, -1)
        return extracted_data.iloc[pipeline.transform(_input)[0]]

    else:
        return None


async def output_recommended_recipes(dataframe):
    if dataframe is not None:
        output = dataframe.copy()
        output = output.to_dict("records")
        for recipe in output:
            recipe['Image_link'] = find_image(recipe['Name'])
            recipe['RecipeIngredientParts'] = extract_quoted_strings(
                recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions'] = extract_quoted_strings(
                recipe['RecipeInstructions'])
    else:
        output = None
    return output


async def generate(dataframe, nutrition_input: list, ingredients: list = [], params: dict = {'n_neighbors': 3, 'return_distance': False}):
    recommendation_dataframe = await recommend(
        dataframe,
        nutrition_input,
        ingredients,
        params
    )

    generated_recipes = await output_recommended_recipes(recommendation_dataframe)

    return generated_recipes
