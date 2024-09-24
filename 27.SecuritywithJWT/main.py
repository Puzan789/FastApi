from fastapi import FastAPI,Depends,status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from datetime import datetime,timedelta,timezone

app = FastAPI()


SECRET_KEY="thequickbrownfoxjumpsoverthelazydog"
ALGORITHM="HS256"
ACCESS_TOKENS_EXPIRATION_MINUTE=30

fake_user_db=dict(
    johndoe=dict(
        username="johndoe",
        email="johndoe@example.com",
        full_name="John Doe",
        hashed_password="$2b$12$Ldyk/LotIItBJGTh1MlLAuzxFWs9Fh2kmAjG5zRpEdjGMeYvb74F6",
        disabled=False,
    )
)

class Token(BaseModel):
    access_token:str
    token_type:str

class token_Data(BaseModel):
    username:str |None=None
    
class User(BaseModel):
    username:str
    email:str|None=None
    full_name:str|None=None
    disabled:bool|None=None

class UserInDB(User):
    hashed_password:str

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db,username):
    if username in db:
        user_dict=db[username]
        print(user_dict)
        return UserInDB(**user_dict)

def authenticate_user(fake_db,username:str,password:str):
    user=get_user(fake_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user 

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc) + expires_delta
    else:
        expire=datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token",response_model=Token)
async def login_for_access_token(form_Data:OAuth2PasswordRequestForm=Depends()):
    user=authenticate_user(fake_user_db,form_Data.username,form_Data.password)
    if not user:
        raise HTTPException(status_code=400,detail="Invalid username or password")
    access_token_expires=timedelta(minutes=ACCESS_TOKENS_EXPIRATION_MINUTE)
    acess_token=create_access_token(
        data={"sub":user.username}, expires_delta=access_token_expires
    )
    return {"access_token": acess_token, "token_type": "bearer"}

async def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_Exception=HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
       detail="Could not Validate Credentials",
       headers={"www-Authenticate": "Bearer"}
   )
    try:
       payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
       username:str=payload.get("sub")
       if username is not None:
           raise credential_Exception
       token_data=token_Data(username)
    except JWTError:
        raise credential_Exception
    user=get_user(fake_user_db,username=token_data.username)



async def get_current_active_user(current_user:User=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
    
@app.get("/users/me",response_model=User)
async def get_me(current_user:User=Depends(get_current_active_user)):
    return current_user

@app.get("users/me/items")
async def read_own_items(current_user:User=Depends(get_current_active_user)) :
    return [{"item_id":"foo","owner":current_user.username}]