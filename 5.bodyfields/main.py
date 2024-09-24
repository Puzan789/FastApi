from fastapi import FastAPI,Body,Path
from pydantic import BaseModel,Field
app=FastAPI()
class Item(BaseModel):
    name:str
    description:str | None=Field(None,title="Thedescription of the items",max_length=300)
    price:float=Field(...,description="Theprice of the item",gt=0)
    tax:float |None=None


@app.put("/items/{item_id}")
async def update_item(item_id:int,item:Item=Body(...,embed=True)):
    results={"items":item_id,"item":item}
    return results