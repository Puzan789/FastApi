from fastapi import FastAPI 
from pydantic import BaseModel, Field,EmailStr
from typing import Union,Literal
app=FastAPI()



class Userbase(BaseModel):
    username:str
    email:EmailStr
    full_name:str|None=None

class UserIn(Userbase):
    password:str


class UserOut(Userbase):
    pass

class UserInDB(Userbase):
    hashed_password:str
   


def fake_password_hasher(raw_password:str):
    return f"superpassword{raw_password}"
    
def fake_save_user(user_in:UserIn):
    hashed_password=fake_password_hasher(user_in.password)
    user_in_db=UserInDB(**user_in.model_dump(),hashed_password=hashed_password)
    print(type(user_in_db.model_dump()))
    print("userin.dict",user_in_db)
    print("User_db_updated")
    return user_in_db

@app.post("/user/",response_model=UserOut)
async def create_user(user_in:UserIn):
    user_in_db=fake_save_user(user_in)
    return user_in_db

class Baseitem(BaseModel):
    description:str
    type:str

class caritem(Baseitem):
    type:str="car"

class PlaneITem(Baseitem):
    type:str="plane"
    size:int


items={
    "item1":{"description":"ALL my frinends are gay","type":"car"},
    "item2":{"description":"I am the aeroplane","type":"plane","size":300},
    "item3":{"description":"I am the best","type":"car"}, 
    "item4":{"description":"I am the worst","type":"plane","size":150}
}
@app.get("/items/{item_id}",response_model=Union[PlaneITem,caritem])
async def read_item(item_id:Literal["item1","item2","item3","item4"]):
    return items[item_id]

class Listitem(BaseModel):
    name:str
    description:str

list_items=[
    {"name":"all","description":"elaleluwa"},
    {"name":"makiaei","description":"emunahcuara"}
]

@app.get("/list_items/",response_model=list[Listitem])
async def read_list_items():
    return items

@app.get("/arbitary",response_model=dict[str,float]) # key chai string aani value chai float
async def get_arbitary() :
    return {"bar":20.0}
