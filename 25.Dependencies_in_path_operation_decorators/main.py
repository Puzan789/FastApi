from fastapi import FastAPI,Header,Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel



async def verify_token(x_token:str=Header(...)):
    print(x_token)
    if x_token != "token":
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_key(x_key:str=Header(...)):
    if x_key != "key":
        raise HTTPException(status_code=401, detail="Invalid key")
    return x_key

app=FastAPI(dependencies=[Depends(verify_token),Depends(verify_key)])

@app.get('/items')
async def read_items():
    return [{'items':'foo'},{"items':'bar'}"}]

@app.get("/users")
async def read_users():
    return [{"username":"Rick"},{"password":"morty"}]