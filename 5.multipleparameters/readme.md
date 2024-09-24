

### **1. Handling Multiple Parameters (Path + Query + Body)**

In FastAPI, you can easily combine **path**, **query**, and **body** parameters in a single endpoint.

### Example:
```python
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., title="The ID of the item to update", ge=1),
    q: str | None = Query(None, max_length=50),
    item: Item = Body(...)
):
    return {"item_id": item_id, "q": q, "item": item}
```

### Explanation:
- **Path Parameter** (`item_id`): Extracted from the URL (`/items/{item_id}`).
- **Query Parameter** (`q`): Optional query parameter (`?q=something`).
- **Body Parameter** (`item`): Parsed from the request body (e.g., JSON).

### Sample Request:
```
PUT /items/5?q=search_term
```

Request body:
```json
{
  "name": "Updated Item",
  "price": 19.99,
  "description": "An updated description"
}
```

### Response:
```json
{
  "item_id": 5,
  "q": "search_term",
  "item": {
    "name": "Updated Item",
    "price": 19.99,
    "description": "An updated description"
  }
}
```

---

### **2. Combining Path and Query Parameters**

If you don’t need body parameters, you can still combine **path** and **query** parameters.

### Example:
```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item"),
    q: str | None = Query(None, title="Query string")
):
    return {"item_id": item_id, "q": q}
```

### Sample Request:
```
GET /items/10?q=fastapi
```

### Response:
```json
{
  "item_id": 10,
  "q": "fastapi"
}
```

---

### **3. Combining Path and Body Parameters**

When you need to send data via both the path and the request body (like in a `PUT` or `PATCH` request):

### Example:
```python
@app.put("/users/{user_id}")
async def update_user(
    user_id: int = Path(..., title="The ID of the user"),
    user: Item = Body(...)
):
    return {"user_id": user_id, "user": user}
```

### Sample Request:
```
PUT /users/25
```

Request body:
```json
{
  "name": "John Doe",
  "price": 100,
  "description": "A sample user"
}
```

### Response:
```json
{
  "user_id": 25,
  "user": {
    "name": "John Doe",
    "price": 100,
    "description": "A sample user"
  }
}
```

---

### **4. Combining Path, Query, and Body**

FastAPI lets you combine all three types of parameters in one endpoint.

### Example:
```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(...),
    q: str | None = Query(None),
    item: Item = Body(...)
):
    return {"item_id": item_id, "q": q, "item": item}
```

This is similar to the first example but showcases how all three parameter types work together in a `PUT` request.

---

### **Summary**

- **Path Parameters** (`Path`): Extracted from the URL path, often used to identify resources (`/items/{item_id}`).
- **Query Parameters** (`Query`): Optional data in the URL query string (`?q=something`).
- **Body Parameters** (`Body`): Used to send JSON or other data in the request body, typically for `POST`, `PUT`, or `PATCH` requests.

