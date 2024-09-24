from fastapi import FastAPI,Cookie,Header
from pydantic import BaseModel

app=FastAPI()
@app.get("/items")
async def read_items(cookie_id:str | None=Cookie(None),user_agent:str|None=Header(None)):
        return {"cookie":cookie_id,"user_Agent":user_agent}