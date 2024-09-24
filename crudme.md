
### Step 1: Install Required Libraries

First, install the necessary packages:

```bash
pip install fastapi uvicorn sqlalchemy sqlite pydantic
```

### Step 2: Setting Up the Project Structure

Your project structure should look something like this:

```
.
├── main.py           # FastAPI app file
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas for validation
├── database.py       # Database connection and session management
└── db.sqlite         # SQLite database file (auto-created when you run the app)
```

### Step 3: Setting Up the Database (SQLAlchemy + SQLite)

#### `database.py`

This file handles the connection to the SQLite database and the session management.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session for the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for ORM models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 4: Define the Student Model (SQLAlchemy)

#### `models.py`

Define the `Student` model for storing student information in the database.

```python
from sqlalchemy import Column, Integer, String
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    course = Column(String)
```

### Step 5: Define Pydantic Schemas for Request and Response

#### `schemas.py`

Define the **Pydantic models** that will be used to validate input and format responses.

```python
from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    age: int
    email: str
    course: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True
```

### Step 6: Implement CRUD Operations in FastAPI

#### `main.py`

Here we define the API endpoints for creating, reading, updating, and deleting students.

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CREATE a new student
@app.post("/students/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# READ all students
@app.get("/students/", response_model=list[schemas.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# READ a specific student by ID
@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# UPDATE a student
@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return {"detail": "Student deleted successfully"}
```

### Step 7: Running the Application

You can now run the FastAPI app using Uvicorn:

```bash
uvicorn main:app --reload
```

- **URL**: The app will be running on `http://127.0.0.1:8000`.
- **Interactive API Docs**: FastAPI automatically generates Swagger UI, which you can access at `http://127.0.0.1:8000/docs`.

### Step 8: Example Requests

- **Create a new student**:
  - **Endpoint**: `POST /students/`
  - **Body**:
    ```json
    {
      "name": "John Doe",
      "age": 21,
      "email": "johndoe@example.com",
      "course": "Computer Science"
    }
    ```

- **Get all students**:
  - **Endpoint**: `GET /students/`

- **Get a specific student**:
  - **Endpoint**: `GET /students/{student_id}`

- **Update a student**:
  - **Endpoint**: `PUT /students/{student_id}`
  - **Body**:
    ```json
    {
      "name": "Jane Doe",
      "age": 22,
      "email": "janedoe@example.com",
      "course": "Mathematics"
    }
    ```

- **Delete a student**:
  - **Endpoint**: `DELETE /students/{student_id}`

