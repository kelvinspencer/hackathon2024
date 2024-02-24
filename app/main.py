from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
import pandas as pd

app = FastAPI()
LOCAL_DATABASE = "./app/data_base.csv"


def init_bd():
    dictionary = {"name": ["Computer"], "description": ["Macbook"], "price": [1000], "tax": [5]}
    base_data = pd.DataFrame.from_dict(dictionary)
    return base_data


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/make_add")
def make_add():
    return {"add": 4 + 6}

@app.post("/items/", status_code=201)
async def create_item(item: Item = Body(...)):
    base_data = init_bd()
    base_data = base_data._append(item.__dict__, ignore_index=True)
    base_data.to_csv(LOCAL_DATABASE, index_label="id")
    return item