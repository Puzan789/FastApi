from fastapi import FastAPI, Response,status

app = FastAPI()

# @app.get("/new-items/")
# async def new_items():
#     return {"items": ["item1", "item2", "item3"]}

# @app.get("/old-items/", status_code=301)
# async def redirect_old_to_new():
#     # Returning a Response with the redirect status and Location header
#     return Response(status_code=301, headers={"Location": "/new-items/"})


@app.post("/items/",status_code=201)
async def read_item_redirect(name:str):
    return name

@app.get("/items/",status_code=status.HTTP_302_FOUND)
async def read_item_redirect():
    return {"hello":"world"}