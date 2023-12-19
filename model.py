import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

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

