from fastapi import FastAPI
from pydantic import BaseModel,conlist
from typing import List,Optional
import pandas as pd


dataset=pd.read_csv('./Data/dataset.csv',compression='gzip')

app = FastAPI()

@app.get("/")
def home():
    return {"Food Recommendation System": "OK"}
