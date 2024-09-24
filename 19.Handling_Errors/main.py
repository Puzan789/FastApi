from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse,PlainTextResponse
from fastapi.exceptions import RequestValidationError
app=FastAPI()

items={"foo": "The foo wrestkers"}

@app.get("/items/{item_id}")
async def read_item(item_id:str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found",headers={"X-errortype": "There is my error bud"})
    
    else:
        return {"name": items[item_id]}
    

class UnicornException(Exception):
    def __init__(self,name:str):
        self.name = name
    

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request:Request,exc:UnicornException):
    return JSONResponse(status_code=218,content={"message":f"{exc.name}"})

@app.get("unicorns/{name}")
async def read_unicorns(name:str):        
    if name=="yolo":
        raise UnicornException(name=name)
    else:
        return {"unicorn_name": name}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc):
    return PlainTextResponse(str(exc),status_code=400)


@app.get("/validation_items/{item_id}")
async def read_validation_items(item_id:int):
    if item_id==3:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"validation_items":item_id}
 
 # see handlingerror JVP