from fastapi import FastAPI
from pydantic import BaseModel,conlist
from typing import List,Optional
import pandas as pd


dataset=pd.read_csv('./Data/dataset.csv',compression='gzip')

app = FastAPI()


class params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False



@app.get("/")
def home():
    return {"Food Recommendation System": "OK"}
