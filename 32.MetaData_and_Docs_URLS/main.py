from fastapi import FastAPI


description= """
The app that is good and responsiblefor the whole world.
## Items 
you can **read Items**

## users 
**create users** (_not implemented_).
"""
tags_metadata=[
    dict(name="users", description="operations with the users,the happy fucking genius user who. The **login** logic is also here"),
    dict(name="items", description="You can **read items**"),
    dict(name="tags", description="You can **read tags**"),
    dict(name="comments", description="You can **read comments**"),
    dict(name="orders", description="You can **read orders**"),
    dict(name="cart", description="You can **read cart**"),
]

app=FastAPI(title="chimichang app", description=description, version="0.01",terms_of_service="http://example.com",contact=dict(name="deedpolio psychic"),license_info=dict(name="Apache2.0",url="https://www.apache.org/licenses/"),openapi_tags=tags_metadata,openapi_url="/api/v1/openapi.json")


@app.get("/items/",tags=['items','comments'])
async def read_whole():
    return {"message": "Welcome to chimichang app"}
