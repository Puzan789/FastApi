from fastapi import FastAPI,Path,Query,Body
from pydantic import BaseModel,Field,HttpUrl

from typing import List
import re
app=FastAPI()

from pydantic import BaseModel, Field

class Image(BaseModel):
    url: HttpUrl  
    username: str


class Item(BaseModel):
    name:str
    description:str | None=None
    price:float
    tax:float | None=None
    # tags:list[str]=[]
    # tags:set[str]=set()
    image:List[Image] | None=None

class offer(BaseModel):
    name:str
    description:str | None=None
    price:float
    items:List[Item] 

@app.put("/items/{item_id}")
async def update_item(item_id:int,item:Item):
    results={"item_id":item_id,"item":item}
    return results

@app.post("/offers")
async def create_offer(offer: offer=Body(...,embed=True)):
    return offer

@app.post("images/multiple")
async def create_multiple_images(images:List[Image]=Body(...,embed=True)):
    return {"images":images}