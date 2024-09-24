from fastapi import FastAPI,Depends,Body
from pydantic import BaseModel

app = FastAPI()

def query_extractor(q:str | None=None):
    return q

def query_or_body_extractor(q:str=Depends(query_extractor),last_query:str|None=Body(None)):
    if not q:
        return last_query
    return q

@app.post("/items")
async def try_query(query_or_body:str=Depends(query_or_body_extractor)):
    return {"query_or_body": query_or_body}
        