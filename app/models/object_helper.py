
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

class ItemModel():
    def __init__(self, db_type):
        self.initalize()

    def initalize():
        dictionary = {"documents": ["documents"], "metadatas": ["metadatas"], "ids": ["ids"]}
        # documents=["This is document1", "This is document2", "document3"], 
        # metadatas=[{"source": "notion"}, {"source": "google-docs"}, {"source": "custom-docs"}], 
        # ids=["doc1","doc2"]
        base_data = pd.DataFrame.from_dict(dictionary)
        return base_data
    
    def load_csv(csv_location):
        base_data = pd.read_csv(csv_location)
        return base_data

class Metadataitem(BaseModel):
    source: str

class tags(BaseModel):
    source: str

class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None

class Doc(BaseModel):
    documents: Optional[List[str]] = None
    metadatas: Optional[List[str]] = None
    ids: Optional[List[str]] = None