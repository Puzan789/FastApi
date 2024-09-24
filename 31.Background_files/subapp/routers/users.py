from fastapi import APIRouter


router = APIRouter()

@router.get("/users/",tags=["users"])
async def read_users():
    return [{"username": "username"},{"username": "ricky"}]


@router.get("/users/me",tags=["users"])
async def read_user_me():
    return {"user_id": "me"}

@router.get("/users/{username}",tags=["users"])
async def read_user(username:str):
    return {"username": username}