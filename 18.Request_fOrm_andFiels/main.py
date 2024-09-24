from fastapi import FastAPI,File,Form,UploadFile,Body
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    pass

@app.post("/create/")
async def create_files(*,file:bytes=File(...,),fileb:UploadFile=File(...,),token:str=Form(...),hello:str=Body(...)):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
        "Body":hello

    }
