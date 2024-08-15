from fastapi import FastAPI,HTTPException
from enum import Enum 

app=FastAPI()

class General_url_choices(Enum):
    ROCK = 'rock'
    ELECTRONICS = 'electronic'
    METAL = 'metal'
    SMOOTH = 'soothing'

BANDS = [
    {"id": 1, "name": 'the kinks', "genre": 'Rock'},
    {"id": 2, "name": 'Albatross', "genre": 'Electronic'},
    {"id": 3, "name": 'The edge', "genre": 'soothing'},
    {"id": 4, "name": '1974 AD', "genre": 'metal'},
]


@app.get("/bands")
async def Bands() -> list[dict]:
    return BANDS

@app.get("/bands/{band_id}")
async def band(band_id: int) -> dict:
    band=next((b for b in BANDS if b["id"]==band_id),None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.get("/bands/genre/{genre}")
async def band_for_genre(genre:General_url_choices) -> list[dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value.lower()
    ]
