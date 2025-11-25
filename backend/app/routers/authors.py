from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/authors", tags=["Authors"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.AuthorListResponse)
def read_authors(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    """
    Получить список всех авторов с пагинацией
    
    - **page**: номер страницы (начиная с 1)
    - **size**: количество авторов на странице
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if size < 1 or size > 100:
        raise HTTPException(status_code=400, detail="Size must be between 1 and 100")
    
    skip = (page - 1) * size
    result = crud.get_authors(db, skip=skip, limit=size)
    
    return {
        "items": result["items"],
        "page": page,
        "size": size,
        "total": result["total"],
    }


@router.get("/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Получить автора по ID"""
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Создать нового автора"""
    return crud.create_author(db=db, author=author)


@router.patch("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    """Частично обновить автора"""
    db_author = crud.update_author(db, author_id=author_id, author_update=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Удалить автора"""
    success = crud.delete_author(db, author_id=author_id)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    return None