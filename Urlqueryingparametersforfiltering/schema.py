from enum import Enum
from pydantic import BaseModel
from datetime import date

class General_url_choices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    SOOTHING= 'soothing'

class Album(BaseModel):
    title:str
    release_date:date


class Band(BaseModel):
    #{"id": 1, "name": 'the kinks', "genre": 'Rock'},
    id :int
    name:str
    genre:str
    albums:list[Album]=[]



