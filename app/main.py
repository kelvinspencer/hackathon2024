import json
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union, List

from app.db_helper import DBQuery
from app.models.object_helper import Doc, Item

app = FastAPI()
db_conn = DBQuery("chromadb")

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryPayload(BaseModel):
    tags: Optional[List[str]] = None
    query: Optional[str] = None

@app.get("/")
def read_root():
    return {"OK": "200"}

@app.post("/docs/query")
async def docs_query(query: QueryPayload):
    tags = query.tags
    docs = db_conn.get_docs_by_tags(tags)
    return {"result": docs}
    

@app.get("/docs/tags")
async def docs_tags():
    response = db_conn.get_tags()
    return {"result": response}

# Same as docs_query
@app.get("/find_by_str/{item_value}")
def read_item(item_value: Union[str, None] = None):
    entries = db_conn.search_for_string(item_value)
    json_entries = json.dumps(entries)
    return {"item_value": json_entries}

# CSV only
# @app.get("/find_by_id/{item_id}")
# def read_item(item_id: Union[str, None] = None):
#     entries = db_conn.find_by_id(item_id)
#     json_entries = json.dumps(entries)
#     return {"value": json_entries}

# @app.api_route('/items', methods=['POST', 'OPTIONS', 'HEAD'])
@app.post("/add_doc/", status_code=201)
async def create_item(item: Doc = Body(...)):
    db_conn.create_doc(item)


@app.get("/delete_all_docs")
def delete_all_docs():
    db_conn.delete_all_docs()
    return True


