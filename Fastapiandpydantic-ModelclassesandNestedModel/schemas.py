from enum import Enum
from pydantic import BaseModel
from datetime import date

class General_url_choices(Enum):
    ROCK = 'rock'
    ELECTRONICS = 'electronic'
    METAL = 'metal'
    SMOOTH = 'soothing'



class Album(BaseModel):
    id:int
    title:str
    release_date:date


class Band(BaseModel):
    #{"id": 1, "name": 'the kinks', "genre": 'Rock'},
    id :int
    name:str
    genre:str
    albums:list[Album]=[Album]



