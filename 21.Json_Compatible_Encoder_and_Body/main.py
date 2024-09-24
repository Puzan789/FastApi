from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.encoders import jsonable_encoder
app=FastAPI()

fake_db={}

class Item(BaseModel):
    name:str |None =None
    description:str | None=None
    price:float | None=None
    tax:float =10.5
    tags:list[str]=[]

items={
    "foo":{"name":"bar","price":0.35},
    "barks":{"name":"cat","price":0.5,"description":"hello rowdy rahtore"},
    "bax":{"name":"dog","price":0.75,"tax":20.0},
    "poxx":{"name":"mouse","description":None,"price":0.25}
}
@app.get("/items/{item_id}",response_model=Item)
async def read_item(item_id:str):
    return items.get(item_id)




@app.put("/items/{item_id}")
def update_item(item_id:str,item:Item):
    json_compatible_item_data=jsonable_encoder(item)
    items[item_id]=json_compatible_item_data
    return json_compatible_item_data

@app.patch("/items/{item_id}",response_model=Item)
async def update_item_partial(item_id:str,item:Item):
    strored_itemsd_Data=items.get(item_id)
    if strored_itemsd_Data is not None:
        stored_item_model=Item(**strored_itemsd_Data)
    else:
        stored_item_model=Item()
    update_data=item.model_dump(exclude_unset=True)
    update_item=stored_item_model.model_copy(update=update_data)
    items[item_id]=jsonable_encoder(update_item)
    print(items)
    return update_item  