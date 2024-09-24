from fastapi import FastAPI
from enum import Enum

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