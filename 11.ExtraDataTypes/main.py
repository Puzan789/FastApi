from fastapi import FastAPI,Body,Path,Query
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime,timedelta
app=FastAPI()



@app.put("items/{item_id}")
async def read_items(item_id:UUID,start_date:datetime | None=Body(None),end_date:datetime | None=Body(None),repat_time:datetime | None=Body(None),mytime:timedelta|None=Body(None)):
    return {"item_id":item_id, "start_date":start_date,"end_date":end_date,"repeat_at":repat_time,"mytime":mytime}