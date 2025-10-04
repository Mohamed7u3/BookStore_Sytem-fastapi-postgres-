from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import services, schemas, models
from database import get_db, engine
from sqlalchemy.orm import Session
from backup import backup_database

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")

# Mount static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# ----------------- FRONTEND -------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------------- API -------------------
@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return services.get_books(db)

@app.get("/books/{id}", response_model=schemas.Book)
def get_book_id(id: int, db: Session = Depends(get_db)):
    book = services.get_book(db, id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Invalid book id provided")

@app.post("/books/", response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return services.create_book(db, book)

@app.put("/books/{id}", response_model=schemas.Book)
def update_book(id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = services.update_book(db, book, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{id}", response_model=schemas.Book)
def delete_book(id: int, db: Session = Depends(get_db)):
    db_book = services.delete_book(db, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
@app.post("/backup/")
def create_backup():
    path = backup_database()
    return {"message": "Backup created successfully", "file": path}
