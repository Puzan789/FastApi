from fastapi import FastAPI,Request
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import time


app=FastAPI()


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request,call_next):
        start_time=time.time()
        response=await call_next(request)
        process_time=time.time()-start_time
        response.headers["X-Process-time"]=str(process_time)
        return response
    

origins=["https://localhost:8000","http://localhost:3000"]

app.add_middleware(MyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,)

@app.get("/blah")
async def blah():
    return {"hello":"world"}



