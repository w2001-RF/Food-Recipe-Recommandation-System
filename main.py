from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def home():
    return {"Food Recommendation System": "OK"}
