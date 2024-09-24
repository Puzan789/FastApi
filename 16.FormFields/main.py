from fastapi import FastAPI,Form,Body
from pydantic import BaseModel

app=FastAPI()





@app.post("/login/")
async def login(usename:str =Form(...),password:str=Form(...)):
    print("password",password)
    return {"username":usename}



class User(BaseModel):
    username:str
    password:str


@app.post("/login-json/")
async def login_json(username:str=Body(...,)):
    print("password",username)
    return username 