from sqlalchemy.orm import Session
from . import models,schemas

def get_user(db:Session,user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first() # will use the f

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db:Session,skip:int=0,limit:int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    fake_hashed_passsword = user.password+"nothashed"
    db_user=models.User(email=user.email,hashed_password=fake_hashed_passsword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db:Session,skip:int=0,limit:int=100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db:Session,item:schemas.ItemCreate,user_id:int):
    db_items=models.Item(**item.model_dump(),owner_id=user_id)
    db.add(db_items)
    db.commit()
    db.refresh(db_items)
    return db_items