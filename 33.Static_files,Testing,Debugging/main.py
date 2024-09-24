from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel

app=FastAPI()

fake_secret_token="thegreathammer"

fake_db=dict(
    foo=dict(id="bar",title="foo",description="root"),
    bar=dict(id="qux",title="bar",description="child"),
    qux=dict(id="quxx",title="qux",description="grandchild"),
)

class Item(BaseModel):
    id:str
    title:str
    description:str | None=None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id:str,x_token:str=Header(...)):
    if x_token!=fake_secret_token:
        raise HTTPException(status_code=401, detail="X-Token header invalid")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items",response_model=Item)
async def create_item(item:Item, x_token:str=Header(...)):
    if x_token!=fake_secret_token:
        raise HTTPException(status_code=401, detail="X-Token header invalid")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id]=item
    return item