from pydantic import BaseModel

class Itembase(BaseModel):
    title:str
    description:str | None=None


class ItemCreate(Itembase):
    pass

class Item(Itembase):
    id:int
    owner_id:int
    class Config:
        orm_mode=True


class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password:str


class User(UserBase):
    id:int
    is_active:bool
    items:list[Item] = []

    class Config:
        orm_mode=True # it allows us to treat like a.key_a instead of data["Key_a"]

