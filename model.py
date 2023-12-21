import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.neighbors import NearestNeighbors


def scaling(dataframe):
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 6:15].to_numpy())
    return prep_data, scaler


def build_pipeline(neigh, scaler, params):
    transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
    pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])
    return pipeline


def extract_ingredient_filtered_data(dataframe, ingredients):
    extracted_data = dataframe.copy()
    regex_string = ''.join(map(lambda x: f'(?=.*{x})', ingredients))
    extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(
        regex_string, regex=True, flags=re.IGNORECASE)]
    return extracted_data


def extract_quoted_strings(s):
    strings = re.findall(r'"([^"]*)"', s)
    return strings


def recommend(dataframe, _input, ingredients=[], params={'n_neighbors': 5, 'return_distance': False}):
    extracted_data = extract_ingredient_filtered_data(dataframe, ingredients)

    if extracted_data.shape[0] >= params['n_neighbors']:
        prep_data, scaler = scaling(extracted_data)
        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data)
        pipeline = build_pipeline(neigh, scaler, params)
        _input = np.array(_input).reshape(1, -1)
        return extracted_data.iloc[pipeline.transform(_input)[0]]

    else:
        return None


def output_recommended_recipes(dataframe):
    if dataframe is not None:
        output = dataframe.copy()
        output = output.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts'] = extract_quoted_strings(
                recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions'] = extract_quoted_strings(
                recipe['RecipeInstructions'])
    else:
        output = None
    return output


def generate(dataframe, nutrition_input: list, ingredients: list = [], params: dict = {'n_neighbors': 5, 'return_distance': False}):
    recommendation_dataframe = recommend(
        dataframe,
        nutrition_input,
        ingredients,
        params.dict()
    )

    generated_recipes = output_recommended_recipes(recommendation_dataframe)

    return generated_recipes.json()

def get_similar_recipe(dataframe, recipe_info: dict, number: int, num_similar: int):
    nutrition_input = recipe_info['Recipe_nutritions_values']
    ingredients = recipe_info['RecipeIngredient']
    params = {'n_neighbors': num_similar, 'return_distance': False}
    similar_recipes_dataframe = recommend(dataframe, nutrition_input, ingredients, params)

    if similar_recipes_dataframe is not None:
        similar_recipes = output_recommended_recipes(similar_recipes_dataframe)
        return similar_recipes[:number]
    else:
        return None
