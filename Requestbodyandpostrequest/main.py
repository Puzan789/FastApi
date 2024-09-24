from fastapi import FastAPI,HTTPException
from enum import Enum 
from schema import Band,General_url_choices,BandBase,BandCreate,Bandwithid

app=FastAPI()



BANDS = [
    {"id": 1, "name": 'the kinks', "genre": 'Rock'},
    {"id": 2, "name": 'Albatross', "genre": 'Electronic'},
    {"id": 3, "name": 'The edge', "genre": 'soothing','albums':
        [
            {'title': "Master of reality","release_date":"1982-09-12"}
        ]},
    {"id": 4, "name": '1974 AD', "genre": 'metal'},
    {"id": 5, "name": 'the colorado', "genre": 'Rock'},

]


@app.get("/bands")
async def Bands(genre : General_url_choices |None=None,has_albums:bool=False) -> list[Bandwithid]:
    band_list=[Bandwithid(**b) for b in BANDS]
    if genre: 
        band_list=[b for b in band_list if b.genre.lower() == genre.value ]# if query parameters
    if has_albums:
        band_list=[b for b in band_list if len(b.albums) >0]
    return band_list
    

@app.get("/bands/{band_id}")
async def band(band_id: int) -> Bandwithid:
    band=next((Bandwithid(**b) for b in BANDS if b["id"]==band_id),None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.get("/bands/genre/{genre}")
async def band_for_genre(genre:General_url_choices) -> list[dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value.lower()
    ]


@app.post("/bands")
async def create_band(band_data: BandCreate) -> Bandwithid:
    id =BANDS[-1]['id']+1
    band=Bandwithid(id=id,**band_data.model_dump())
