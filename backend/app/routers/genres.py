from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/genres", tags=["Genres"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.GenreListResponse)
def read_genres(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    """
    Получить список всех жанров с пагинацией
    
    - **page**: номер страницы (начиная с 1)
    - **size**: количество жанров на странице
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if size < 1 or size > 100:
        raise HTTPException(status_code=400, detail="Size must be between 1 and 100")
    
    skip = (page - 1) * size
    result = crud.get_genres(db, skip=skip, limit=size)
    
    return {
        "items": result["items"],
        "page": page,
        "size": size,
        "total": result["total"],
    }


@router.get("/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    """Получить жанр по ID"""
    db_genre = crud.get_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre


@router.post("/", response_model=schemas.Genre, status_code=status.HTTP_201_CREATED)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    """Создать новый жанр"""
    return crud.create_genre(db=db, genre=genre)


@router.patch("/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: int, genre: schemas.GenreUpdate, db: Session = Depends(get_db)):
    """Частично обновить жанр"""
    db_genre = crud.update_genre(db, genre_id=genre_id, genre_update=genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """Удалить жанр"""
    success = crud.delete_genre(db, genre_id=genre_id)
    if not success:
        raise HTTPException(status_code=404, detail="Genre not found")
    return None
