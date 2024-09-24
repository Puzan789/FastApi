

### **1. Project Structure**

```bash
transformer_translation_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI entry point
│   ├── config.py                     # Configurations (JWT, API Keys, etc.)
│   ├── models.py                     # Pydantic models for request/response
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py                   # JWT-based authentication logic
│   │   ├── users.py                  # User registration/login/logout logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── translation.py            # Translation endpoint for model inference
│   │   ├── api_key.py                # API key generation and validation logic
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── model.py                  # Transformer model loading and inference
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                # Utility functions (hashing, token generation, etc.)
│
├── tests/
│   ├── test_auth.py                  # Tests for authentication
│   ├── test_translation.py           # Tests for translation
│
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── .env                              # Environment variables (JWT secret, API keys)
```

---

### **2. Explanation of Each Component**

- **`app/main.py`**: Entry point for FastAPI, where all the routers (authentication, translation, API key generation) are included.
- **`app/auth/auth.py`**: Contains JWT-based authentication logic (login, logout, token verification).
- **`app/auth/users.py`**: Manages user registration and login.
- **`app/routes/translation.py`**: Handles requests for translation via the transformer model.
- **`app/routes/api_key.py`**: Generates API keys for authenticated users.
- **`app/transformers/model.py`**: Handles the loading and inference of the transformer translation model.
- **`app/utils/helpers.py`**: Contains helper functions like password hashing, token creation, and API key generation.

---

### **3. Step-by-Step Implementation**

#### **1. JWT Authentication and User Management (Login, Logout)**

We will set up a simple **JWT-based authentication** system with login/logout functionality.

#### **`auth/auth.py`** (JWT Token Creation and Verification)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_id
```

#### **`auth/users.py`** (User Registration and Login)

```python
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.utils.helpers import hash_password, verify_password
from app.auth.auth import create_access_token
from datetime import timedelta

router = APIRouter()

# In-memory user database (replace with a real DB)
fake_users_db = {}

class User(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register_user(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "password": hashed_password}
    return {"msg": "User registered successfully"}

@router.post("/login")
async def login_user(request: LoginRequest):
    user = fake_users_db.get(request.username)
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
```

#### **2. Transformer Model for Translation**

Let’s load the transformer model (e.g., MarianMT, a model for machine translation).

#### **`transformers/model.py`**

```python
from transformers import MarianMTModel, MarianTokenizer

class TransformerModel:
    def __init__(self, model_name: str):
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def translate(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt")
        translated_tokens = self.model.generate(**inputs)
        return self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
```

---

#### **3. API for Translation and API Key Generation**

#### **`routes/translation.py`** (Protected Translation Endpoint)

```python
from fastapi import APIRouter, Depends
from app.auth.auth import verify_token
from app.transformers.model import TransformerModel

router = APIRouter()

# Load your model (e.g., MarianMT for English to French translation)
model = TransformerModel("Helsinki-NLP/opus-mt-en-fr")

@router.post("/translate")
async def translate_text(text: str, token: str = Depends(verify_token)):
    translation = model.translate(text)
    return {"original": text, "translated": translation}
```

#### **`routes/api_key.py`** (Generate API Key)

Authenticated users will be able to generate their own API key for later use in other web apps or services.

```python
from fastapi import APIRouter, Depends
from app.auth.auth import verify_token
import secrets

router = APIRouter()

api_keys_db = {}

@router.post("/generate-apikey")
async def generate_api_key(token: str = Depends(verify_token)):
    user_id = token
    api_key = secrets.token_hex(16)  # Generate a random API key
    api_keys_db[user_id] = api_key
    return {"api_key": api_key}
```

You can store API keys in a more persistent storage, such as a database.

---

#### **4. API Key Validation for Third-Party Use**

Once the user has their API key, they can embed it in requests to a protected translation service.

#### **`utils/helpers.py`** (API Key Validation Helper)

```python
from fastapi import HTTPException

def verify_api_key(api_key: str):
    for user, key in api_keys_db.items():
        if key == api_key:
            return user
    raise HTTPException(status_code=403, detail="Invalid API key")
```

#### **`routes/translation.py` (Modified to Support API Key)**

We modify the translation route to accept **API keys**:

```python
@router.post("/translate-with-key")
async def translate_with_api_key(text: str, api_key: str):
    user = verify_api_key(api_key)
    translation = model.translate(text)
    return {"user": user, "original": text, "translated": translation}
```

---

### **4. `main.py`: Entry Point**

Finally, bring everything together in the `main.py`:

```python
from fastapi import FastAPI
from app.routes.translation import router as translation_router
from app.routes.api_key import router as api_key_router
from app.auth.users import router as users_router

app = FastAPI()

# Include all the routers
app.include_router(users_router, prefix="/auth")
app.include_router(translation_router, prefix="/translation")
app.include_router(api_key_router, prefix="/apikey")

@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
```

---

### **5. Testing the Workflow**

1. **User Registration/Login**:
   - Register a user: `POST /auth/register`.
   - Log in the user: `POST /auth/login` (this will return the JWT token).

2. **Generate API Key**:
   - After logging in, the user can generate an API key: `POST

 /apikey/generate-apikey`.

3. **Use API Key for Translation**:
   - The user can now use their API key to access the `/translate-with-key` endpoint:
   ```bash
   curl -X POST "http://localhost:8000/translation/translate-with-key" -H "Authorization: Bearer <API_KEY>" -d "text=Hello World"
   ```

---

### Building a Platform for User API Key Management

Now, let's enhance the platform by adding **API Key management** similar to platforms like **ChatGPT** or **OpenAI**. Users can:

1. **Register/Login**.
2. **Create API keys**.
3. **Manage API keys** (view, regenerate, or revoke).
4. **Use the API key** in third-party applications for accessing services like translation.

In addition to this, I'll show where and how to include the web-based frontend.

---

### **1. Project Structure (with Web Interface)**

In this structure, we will include both the FastAPI backend and a simple web-based frontend for managing API keys.

```
transformer_translation_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI entry point
│   ├── config.py                     # Configurations (JWT, API keys, etc.)
│   ├── models.py                     # Pydantic models for request/response
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py                   # JWT-based authentication logic
│   │   ├── users.py                  # User registration/login/logout logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── translation.py            # Translation endpoint for model inference
│   │   ├── api_key.py                # API key generation and management
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── model.py                  # Transformer model loading and inference
│   ├── templates/                    # HTML templates for web-based API key management
│   │   ├── login.html                # Login page
│   │   ├── dashboard.html            # Dashboard for managing API keys
│   ├── static/                       # Static files (CSS, JS)
│   │   ├── styles.css                # Basic styling for frontend
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                # Utility functions
│
├── tests/
├── requirements.txt
├── README.md
└── .env
```

### **2. FastAPI Backend - API Key Management**

---

#### **Step 1: Modify the API Key Logic**

First, we need to add logic to allow users to generate and manage their API keys. We'll allow actions like **viewing**, **regenerating**, or **revoking** API keys from a **web-based frontend**.

#### **`routes/api_key.py`** (Manage API Keys)

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from app.auth.auth import verify_token
import secrets

router = APIRouter()

# In-memory API keys database (replace with real DB in production)
api_keys_db = {}

@router.post("/generate-apikey")
async def generate_api_key(token: str = Depends(verify_token)):
    user_id = token
    api_key = secrets.token_hex(16)  # Generate random API key
    api_keys_db[user_id] = api_key
    return {"api_key": api_key}

@router.get("/view-apikey")
async def view_api_key(token: str = Depends(verify_token)):
    user_id = token
    api_key = api_keys_db.get(user_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"api_key": api_key}

@router.post("/revoke-apikey")
async def revoke_api_key(token: str = Depends(verify_token)):
    user_id = token
    if user_id in api_keys_db:
        del api_keys_db[user_id]
    return {"msg": "API key revoked"}

@router.post("/regenerate-apikey")
async def regenerate_api_key(token: str = Depends(verify_token)):
    user_id = token
    new_api_key = secrets.token_hex(16)  # Generate new API key
    api_keys_db[user_id] = new_api_key
    return {"api_key": new_api_key}
```

---

### **3. Frontend Integration Using HTML Templates**

To integrate the web-based frontend where users can **login** and **manage their API keys**, we will use **Jinja2 templates** in FastAPI to render HTML pages.

FastAPI supports rendering HTML pages using the `Jinja2` templating engine.

#### **Step 2: Setting Up the Frontend Pages**

- **Login Page**: Allows users to login and get an API key.
- **Dashboard Page**: Displays the API key and provides options to regenerate or revoke the API key.

#### **`templates/login.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>Login to Access API Keys</h1>
    <form action="/auth/login" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

#### **`templates/dashboard.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Key Dashboard</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>API Key Management</h1>
    <div>
        <h2>Your API Key:</h2>
        <p id="apikey">{{ api_key }}</p>
    </div>
    <div>
        <form action="/apikey/regenerate-apikey" method="post">
            <button type="submit">Regenerate API Key</button>
        </form>
        <form action="/apikey/revoke-apikey" method="post">
            <button type="submit">Revoke API Key</button>
        </form>
    </div>
</body>
</html>
```

---

### **4. Serving the Frontend**

#### **Step 3: FastAPI Backend for Serving HTML Pages**

We’ll modify the `main.py` to serve the **login** and **dashboard** pages and handle the user's API key management actions.

#### **`main.py`**

```python
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth.users import router as users_router
from app.routes.api_key import router as api_key_router
from app.auth.auth import verify_token

app = FastAPI()

# Mount static directory for CSS and other assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(users_router, prefix="/auth")
app.include_router(api_key_router, prefix="/apikey")

# Serve login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Serve dashboard page (requires login)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, token: str = Depends(verify_token)):
    api_key = api_keys_db.get(token)
    return templates.TemplateResponse("dashboard.html", {"request": request, "api_key": api_key})

# Health check route
@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
```

### **5. Example Workflow**

#### **User Workflow**:

1. **Login**:
   - User visits the `/login` page.
   - They enter their credentials (username and password).
   - If successful, they are redirected to the `/dashboard` page, where they can see their API key.

2. **Generate API Key**:
   - The dashboard displays their current API key (or provides the option to generate a new one).
   - The user can click on **Regenerate API Key** or **Revoke API Key** from the dashboard.

3. **Copy API Key**:
   - The user copies the API key from the dashboard and includes it in their web app for making API requests.

---

### **6. Example of How Users Can Include the API Key in Their Web App**

After a user obtains their API key from the dashboard, they can use it to make API requests to your service. Here's an example of how they might include the API key in their JavaScript-based web application for translation purposes.

#### **JavaScript Example for Translation API**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Translation Web App</title>
</head>
<body>
    <h1>Translation</h1>
    <textarea id="text-to-translate" placeholder="Enter text to translate"></textarea>
    <button onclick="translateText()">Translate</button>


    <p id="translation-result"></p>

    <script>
        async function translateText() {
            const text = document.getElementById("text-to-translate").value;
            const apiKey = "your_api_key";  // Replace with the user's actual API key
            
            const response = await fetch("http://localhost:8000/translation/translate-with-key", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: text,
                    api_key: apiKey
                })
            });

            const result = await response.json();
            document.getElementById("translation-result").innerText = result.translated;
        }
    </script>
</body>
</html>
```

### **Summary of Key Features**:

1. **Web-based API key management**:
   - Users can log in, view, regenerate, or revoke their API key.
   - API keys are generated and stored securely in memory (or a database in production).
   
2. **Frontend and Backend**:
   - The frontend provides a simple dashboard for managing API keys using HTML and CSS.
   - The backend is responsible for user authentication, API key generation, and translation services.

3. **Usage in Web Apps**:
   - Users can integrate their API keys into their own web applications to access translation services securely.

This structure provides a strong foundation for building a platform similar to how ChatGPT handles API key management, where users can securely manage their keys and use them in their apps.

Sure! Here's a Python-based example of how users can include the **API key** in their web app using Python’s `requests` library. This can be used to interact with your FastAPI translation service that requires an API key.

### Python Example: Making Requests with API Key

```python
import requests

# User's API Key (they obtain this from your platform after login)
API_KEY = "your_api_key"  # Replace with the actual API key

# URL of your translation API
API_URL = "http://localhost:8000/translation/translate-with-key"

# Text to translate
text_to_translate = "Hello, how are you?"

# Making the API request
response = requests.post(
    API_URL,
    json={"text": text_to_translate, "api_key": API_KEY}
)

# Checking if the request was successful
if response.status_code == 200:
    # Print the translated text
    result = response.json()
    print("Translated Text:", result["translated"])
else:
    # Handle the error
    print(f"Error: {response.status_code}", response.json())
```

### Steps the User Would Follow:
1. **Obtain API Key**: The user logs into your web platform, navigates to the dashboard, and copies their API key.
2. **Include API Key**: The user includes the API key in their Python code by replacing the placeholder in `API_KEY`.
3. **Make API Requests**: The user can now make requests to your translation service using their API key to authenticate and access the service.

### Key Elements:
- **API Key**: Used in the request body to authenticate the user.
- **`requests.post`**: Sends a POST request with the text to be translated and the API key.
- **Error Handling**: If the API key is invalid or the request fails, the user gets feedback via status codes.

This is a simple Python client that users can run in their environment to interact with your translation service, authenticated via their unique API key.