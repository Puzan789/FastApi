from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

@app.get("/",description="This is our first route",deprecated=True ) 
async def root():
    return {"message": "Welcome to the FastAPI API"}

@app.post("/")
async def post():
    return {"message": "You've posted a request"}

@app.put("")
async def put():
    return {"message": "You've updated a request"}

@app.get("/users")
async def read_items():
    return {"message":"users all the items"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "me is the user" }

@app.get("/users/{item_id}")
async def get_items(item_id:str):
    return {"users_id": item_id}


class FoodEnum(str,Enum):
    fruits="fruits"
    vegetables="vegetables"
    dairy="dairy"

@app.get("/food/{food_name}")
async def get_food(food_name:FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {
            "food_name":food_name,
                "message":'you are helathy' 
                }
    if food_name == FoodEnum.fruits:
        return {
            "food_name":food_name,
                "message":'you are not helathy' 
                }
    
    return {
            "food_name":food_name,
                "message":'you are not helathy' 
                }

fakes_db=[{'item_name':'food'},{'item_name':'snickers'},{'item_name':'fmilk'},{'item_name':'fk'},{'item_name':'cheese'},{'item_name':'rosindey'},{'item_name':'cakra'}]
@app.get("/items")
async def get_items(skip:int=0,limit:int=10):#http://127.0.0.1:8000/items?skip=2&&limit=1
 return fakes_db[skip:skip+limit]

@app.get("/items/{item_id}")
async def get_item(item_id:str,q :Optional[str]=None,short:bool=False):
    item={"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({'description':f'This is the description of {item_id}'})
    return item

class Item(BaseModel):
    name:str
    description:str|None=None
    price:int
    tax:float|None=None


# REquestbody
@app.post("/items")
async def create_item(item:Item):
    item_dic= item.model_dump()
    if item.tax:
        price_with_tax= item.price+item.tax
        return {**item_dic, "Price_with_tax": price_with_tax}   
     
    else:
        return item_dic

@app.put("/items/{item_id}" )
async def create_item_put(item_id:int,items:Item,q:str |None=None):
    result={"item_id":item_id,**items.model_dump()}
    if q:
        result.update({"q":q})
    return result