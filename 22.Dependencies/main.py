from fastapi import FastAPI,Depends
from pydantic import BaseModel

app=FastAPI()


async def commonparameters(q:str|None=None,skip:int=0,limit:int=100):
    return {"q":q, "skip":skip, "limit":limit}

@app.get("/items/")
async def read_items(commons:dict=Depends(commonparameters)):
    return commons
    
@app.get("/users/")
async def read_items(q:str|None=None,skip:int=0,limit:int=100):
    return {"q":q, "skip":skip, "limit":limit}  