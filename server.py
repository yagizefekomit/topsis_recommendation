from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import topsis_application as ts
app = FastAPI()

df = pd.read_csv('Finalized_numeric.csv')

class Request(BaseModel):
    display: int
    performance: int
    battery: int
    camera: int
    memory: int
    storage: int
    weight: int
    price: int


@app.post("/recommend/")
async def create_item(request: Request):
    weight_mt = [
        request.display,
        request.performance,
        request.battery,
        request.camera,
        request.memory,
        request.storage,
        request.weight,
        request.price
    ]
    _, scores = ts.topsis_recommendation(df, weight_mt, ts.benefit_criteria)
    return scores