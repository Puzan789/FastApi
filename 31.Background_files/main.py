from fastapi import FastAPI,Depends
from datetime import datetime
from fastapi import BackgroundTasks
import time
app=FastAPI()



def write_notification(message:str):
    with open ("log.txt", "a") as log:
        log.write(message)


def get_query(backgroundtasks:BackgroundTasks,q:str|None=None):
    if q:
        message=f"found query :{q} \n"
        backgroundtasks.add_task(write_notification, message)
    return q

@app.post("/send-notification{email}",status_code=202)
async def send_notification(email:str,background_task:BackgroundTasks,q:str=Depends(get_query)):
    message = f"Background task started for {email}\n"
    background_task.add_task(write_notification, message)
    return {"message": f"Notification sent "}