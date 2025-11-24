from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/books", tags=["Books"])


# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.BookListResponse)
def read_books(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    """
    Получить список всех книг с пагинацией
    
    - **page**: номер страницы (начиная с 1)
    - **size**: количество книг на странице
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if size < 1 or size > 100:
        raise HTTPException(status_code=400, detail="Size must be between 1 and 100")
    
    skip = (page - 1) * size
    result = crud.get_books(db, skip=skip, limit=size)
    
    return {
        "items": result["items"],
        "page": page,
        "size": size,
        "total": result["total"],
    }


@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    return crud.create_book(db=db, book=book)


@router.patch("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Частично обновить книгу"""
    db_book = crud.update_book(db, book_id=book_id, book_update=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    success = crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
