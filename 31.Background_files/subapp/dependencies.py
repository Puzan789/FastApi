from fastapi import Header,HTTPException

async def get_token_header(x_token:str=Header(...)):
    if x_token != 'fake':
        raise HTTPException(status_code=400,detail="X-token is not a valid")
    

async def get_query_token(token:str):
    if token != 'fakey':
        raise HTTPException(status_code=400, detail="No fakey provided")
    
