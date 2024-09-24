from fastapi import FastAPI,Depends
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()

fake_user_db={
    "johndoe": dict(
        username="johndoe",
        email="johndoe@example.com",
        hashed_password="fakehashedsecret",
        fullname="John Doe",
        disabled=False,
    ),
    "alice": dict(
        username="alice",
        email="alice@example.com",
        hashed_password="fakehashedsecret2",
        disabled=True,
        fullname="Alice Smith")

}
def fake_hashed_password(password:str):
    return f"fakehashed{password}"



oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username:str
    email:str|None=None
    fullname:str|None=None
    disabled:bool|None=None

class Userindb(User):
    hashed_password:str

def get_user_indatabase(db,username:str):
    if username in db :
        user_dict=db[username]
        return Userindb(**user_dict)
    
def fake_decode_token(token):
    return get_user_indatabase(fake_user_db,token)


async def create_current_user(token:str=Depends(oauth2_scheme)):
    user=fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token",headers={"WWW-Authenticate":"Bearer"})
    return fake_decode_token(token)


@app.post("/token")
async def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user_dict=fake_user_db.get(form_data.username)  # form bhaneko authorization ko forms
    if not user_dict :
        raise HTTPException(status_code=400,detail="Incorrect username or password")
    user=Userindb(**user_dict) # user
    hashed_password=fake_hashed_password(form_data.password)
    if not user.hashed_password == hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type":"bearer"}
                


async def get_current_active_users(current_user:User=Depends(create_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def get_user_me(currentuser:User=Depends(get_current_active_users)):
    return currentuser

@app.get("/items/")
async def read_items(token:str=Depends(oauth2_scheme)):
    return{"tokens":token}

