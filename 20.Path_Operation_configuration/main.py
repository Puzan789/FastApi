from fastapi import FastAPI,status
from pydantic import BaseModel
from enum import Enum
app=FastAPI()

class Item(BaseModel):
    name:str
    description:str | None=None
    price:float
    tax:float | None=None
    tags:set[str]=set()


class Tags(Enum):
    items="items"
    users="users"

 # _ shows italic
@app.post("/items/",response_model=Item,status_code=status.HTTP_201_CREATED,tags=[Tags.items],summary="Creates an item",response_description="the item is created")

async def create_item(item:Item):
    """
    Create an item with all the information.

    - _name_: Name of the item.
    - __description__: Description of the item.
    - **price**: Price of the item. *(required)*
    - **tax**: Tax of the item.
    - **tags**: Tags of the item which must be unique.
    """
    return item


# @app.post("/items1/", response_model=Item,status_code=status.HTTP_201_CREATED)
# async def create_item(item: Item):
#     return {"name": "halal", "price": 89, "internal_id": 123}


@app.get("/items/",tags=[Tags.items])
async def read_items():
    return [{"name": "halal", "price":42}]

@app.get("/users/",tags=[Tags.users])
async def read_users():
    return [{"username": "johndoe", "email": "john@example.com"}]



@app.get("/usersop/",tags=[Tags.users],deprecated=True)
async def read_users():
    return [{"username": "johndoe", "email": "john@example.com"}]