from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr
from typing import Literal

app=FastAPI()

class Item(BaseModel):
    name:str
    description:str | None=None
    price:float
    tax:float =10.5
    tags:list[str]=[]

items={
    "foo":{"name":"foo","price":50.2},
    "barks":{"name":"pus","description":"the thunder arm thats gonna be lit","price":65,"tax":20.2},
    "bax":{"name":"dsfdsf","description":"the dsdsf has the funcking best dsds in the world","price":100,"tax":10.5},
    "poxx":{"name":"marchus","description":None,"price":10,"tax":1.5}

}
@app.get("/items/{item_id}",response_model=Item,response_model_exclude_unset=True) # jastai unset gareko null rakheko lai uta api ma dekhaudaina 
async def read_items(item_id:Literal["foo","barks","bax","poxx"]):
    return items[item_id]

@app.post("/items/")
async def create_item(item:Item):
    return item

class UserBaseModel(BaseModel):
    username:str
    email:EmailStr
    fullname:str | None=None


class userin(UserBaseModel):
    password:str

class userout(UserBaseModel):
    pass
   

@app.post("/user",response_model=userout) 
async def create_user(user:userout):
    return user

@app.get("/items/{item_id}/name",response_model=Item,response_model_exclude=["tax"])
async def read_item_name(item_id:Literal["foo","barks","bax","poxx"]):
    return items[item_id]

@app.get("/ items/{item_id}/public",response_model=Item,response_model_include=['name','description'])
async def read_item_public(item_id:Literal["foo","barks","bax","poxx"]):
    return items[item_id]