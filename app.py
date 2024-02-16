# Import necessary modules
from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create FastAPI app instance
app = FastAPI()

# Dependency function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home route
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    # Retrieve all todos from the database
    todos = db.query(models.Todo).all()
    # Render the base.html template with the request and todo_list
    return templates.TemplateResponse("base.html", {"request": request, "todo_list": todos})


@app.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    # Create a new Todo instance with the provided title
    new_todo = models.Todo(title=title)
    # Add the new_todo to the database
    db.add(new_todo)
    # Commit the changes to the database
    db.commit()
    # Redirect the user to the home route
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# Example routes (commented out)
# @app.get("/")
# def home():
#     return {"Hello": "World"}

# @app.get(f"/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}