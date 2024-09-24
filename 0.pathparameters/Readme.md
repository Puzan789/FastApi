

# FastAPI Path Parameters Cheatsheet

## **1. Path Parameters (Basics)**

Path parameters are values that are part of the URL path. In FastAPI, you can extract and validate these values using the `Path` function.

### **Example of Path Parameters** in a `GET` request:

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(..., title="The ID of the item", ge=1)):
    return {"item_id": item_id}
```

- **`{item_id}`**: This is a path parameter in the URL, which is extracted using `Path`.
- **Path(...):** The ellipsis (`...`) means this parameter is required.
- **Validation**: You can add constraints such as `ge=1` (greater than or equal to 1).

### **Validation Options** for Path:
- `gt` = Greater than
- `ge` = Greater than or equal to
- `lt` = Less than
- `le` = Less than or equal to
- `title`, `description`: Meta-data for documentation.

---

## **2. HTTP Methods with Path Parameters**

FastAPI supports multiple HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) with path parameters.

### **GET Example:**
Retrieves a resource by `item_id`.

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., description="The ID of the item")):
    return {"item_id": item_id}
```

### **PUT Example:**
Updates the entire resource identified by `item_id`.

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int = Path(...), name: str):
    return {"item_id": item_id, "name": name}
```

- **PUT**: Used for **complete replacement** of the resource.
- The entire resource is updated or replaced, so the client should send all relevant fields.

### **PATCH Example:**
Partially updates the resource identified by `item_id`.

```python
@app.patch("/items/{item_id}")
async def patch_item(item_id: int = Path(...), name: str | None = None):
    return {"item_id": item_id, "name": name}
```

- **PATCH**: Used for **partial updates** of the resource.
- The client only needs to send the fields that need to be updated.

### **DELETE Example:**
Deletes the resource identified by `item_id`.

```python
@app.delete("/items/{item_id}")
async def delete_item(item_id: int = Path(...)):
    return {"item_id": item_id, "status": "deleted"}
```

- **DELETE**: Deletes the resource corresponding to `item_id`.

---

## **3. Path Parameters with Validations**

You can add custom validations to your path parameters using `Path`.

### Example with Validation:
```python
@app.get("/users/{user_id}")
async def read_user(user_id: int = Path(..., title="The ID of the user", ge=1, le=1000)):
    return {"user_id": user_id}
```
- **ge=1**: Ensures `user_id` is at least 1.
- **le=1000**: Ensures `user_id` is at most 1000.

### Full Example:
```python
@app.get("/products/{product_id}")
async def get_product(product_id: int = Path(..., title="Product ID", gt=0)):
    return {"product_id": product_id}
```

In this case, the **product_id** must be:
- **`gt=0`**: Greater than 0.

---

## **4. Combining Path and Query Parameters**

Path parameters can be combined with query parameters for more complex operations.

### Example:
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(...), q: str | None = None):
    return {"item_id": item_id, "q": q}
```

- **`item_id`**: A path parameter (required).
- **`q`**: A query parameter (optional).

### Request Example:
```
GET /items/5?q=some_query
```

Response:
```json
{
  "item_id": 5,
  "q": "some_query"
}
```

---

## **5. Path Parameters in PUT, PATCH, and DELETE**

Here's a combined example showing how to use **path parameters** in different HTTP methods.

### Example of All Methods:

```python
from fastapi import FastAPI, Path

app = FastAPI()

# GET Request
@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., title="Item ID", gt=0)):
    return {"item_id": item_id}

# PUT Request
@app.put("/items/{item_id}")
async def put_item(item_id: int = Path(...), name: str):
    return {"item_id": item_id, "name": name}

# PATCH Request
@app.patch("/items/{item_id}")
async def patch_item(item_id: int = Path(...), name: str | None = None):
    return {"item_id": item_id, "name": name}

# DELETE Request
@app.delete("/items/{item_id}")
async def delete_item(item_id: int = Path(...)):
    return {"item_id": item_id, "status": "deleted"}
```

### Sample Requests:

1. **GET** `/items/1`
2. **PUT** `/items/1` with body:
   ```json
   {
     "name": "Updated Item"
   }
   ```
3. **PATCH** `/items/1` with body:
   ```json
   {
     "name": "Partial Update"
   }
   ```
4. **DELETE** `/items/1`

---

## **6. Summary of Path Parameters in HTTP Methods**

| HTTP Method | Example URL                | Action                                                   |
|-------------|----------------------------|----------------------------------------------------------|
| **GET**     | `/items/{item_id}`          | Retrieve a resource by `item_id`                          |
| **PUT**     | `/items/{item_id}`          | Fully update or replace the resource identified by `item_id` |
| **PATCH**   | `/items/{item_id}`          | Partially update the resource identified by `item_id`     |
| **DELETE**  | `/items/{item_id}`          | Delete the resource identified by `item_id`               |

---

### Path Parameter Validations:
- `ge=...` (greater than or equal to)
- `le=...` (less than or equal to)
- `gt=...` (greater than)
- `lt=...` (less than)
- `title="..."` and `description="..."` (for documentation)

