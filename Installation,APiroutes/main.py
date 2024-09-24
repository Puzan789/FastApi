from fastapi import FastAPI
app=FastAPI()


@app.get("/")
async def index() -> dict[str,str]:
    return {"message": "Welcome to the FastAPI API!"}

@app.get("/about")
async def aboutpage() -> str:
    return "An exceptional company"