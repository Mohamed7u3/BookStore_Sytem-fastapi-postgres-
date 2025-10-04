from models import Book
from sqlalchemy.orm import Session
from schemas import BookCreate

def create_book(db: Session, data: BookCreate):
    book_isinstance = Book(**data.model_dump())
    db.add(book_isinstance)
    db.commit()
    db.refresh(book_isinstance)
    return book_isinstance

def get_books(db: Session):
    return db.query(Book).all()
def get_book(db: Session, book_id = int):
    return db.query(Book).filter(Book.id == book_id).first()
def update_book(db: Session, book = BookCreate, book_id = int):
    book_quaryset = db.query(Book).filter(Book.id == book_id).first()
    if book_quaryset:
        for key, value in book.model_dump().items():
            setattr(book_quaryset, key, value)
        db.commit()
        db.refresh(book_quaryset)

    return book_quaryset

def delete_book(db: Session, id: int):
    book_quaryset = db.query(Book).filter(Book.id == id).first()
    if book_quaryset:
        db.delete(book_quaryset)
        db.commit()
    return book_quaryset
