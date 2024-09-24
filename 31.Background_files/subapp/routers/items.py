from fastapi import APIRouter,Depends,HTTPException
from ..dependencies import get_token_header

router=APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {
    "items": {
        "name": "rokey",
        "gun": "gunicorn"
    }
}

@router.get('/')
async def read_items():
    return fake_items_db['items']

@router.get('/{item_id}')
async def read_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]['name'],"item_id":item_id}

@router.put('/{item_id}', tags=['custom'], responses={403: {"description": "Operation forbidden"}})
async def update_item(item_id:str):
    if item_id!="items":
        raise HTTPException(status_code=403, detail="Operation forbidden")
    return {"item_id": item_id, "name":"updated item of the items"}
    
