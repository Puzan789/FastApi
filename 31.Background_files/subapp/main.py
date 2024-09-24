from fastapi import FastAPI,Depends
from .dependencies import get_query_token,get_token_header
from .routers import users,items
# from router.users import router as user_router #esari ni garna sakinxa
# we cann do in __init_- ma



app=FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
