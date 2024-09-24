from fastapi import FastAPI,Query,Path

app=FastAPI()

@app.get("/items_validation/{item_id}")#*chai q:str ley default parameter bhanda aagadi aauna parxa teibhara  *
async def items_validation(
    *,
    item_id:int=Path(...,title="this is jsut a fucking game",le=34),
    q:str="hello",
    ):
    result={"item_id":item_id}
    if q:
        result.update({"q":q})
    return result
