from fastapi import FastAPI,Body
from pydantic import BaseModel,Field

app=FastAPI()

class Item(BaseModel):
    # name:str=Field(...,example="foo")
    # description: str | None= Field(None,example="desc:")
    # price:float
    # tax:float | None=None
    name:str
    description: str | None=None
    price:float
    tax:float | None=None

    # class Config:
    #     model_config = {

    #     "json_schema_extra": {

    #         "example": {

    #             "name": "Foo",
 
    #             "description": "A very nice Item",

    #             "price": 16.25,

    #             "tax": 1.67

    #         }

    #     }

    # }


# Path parameter
@app.put("/items/{item_id}")
async def update_item(item_id:int, item:Item=Body(...,example={"name":"fourier transformer", "description":"shockolocjolo","price":"noneoftheproce","tax":"noneoftheproce"})):
    results={"item_id":item_id,"item":item}
    return results