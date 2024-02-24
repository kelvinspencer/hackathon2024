
from pydantic import BaseModel
from typing import Optional
import pandas as pd



class ItemModel():
    def __init__(self, db_type):
        self.initalize()

    def initalize():
        dictionary = {"name": ["Computer"], "description": ["Macbook"], "price": [1000], "tax": [5]}
        base_data = pd.DataFrame.from_dict(dictionary)
        return base_data
    
    def load_csv(csv_location):
        base_data = pd.read_csv(csv_location)
        return base_data

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None