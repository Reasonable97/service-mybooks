from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# Схема для автора (базовая информация)
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=5000)


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy 2.0


# Схема для жанра
class GenreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схема для книги
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    year: Optional[int] = Field(None, ge=1000, le=2100)


class BookCreate(BookBase):
    """Схема для создания книги: нужны только title, year, списки ID авторов и жанров"""
    author_ids: List[int] = Field(default_factory=list)
    genre_ids: List[int] = Field(default_factory=list)


class BookUpdate(BaseModel):
    """Схема для PATCH-обновления: все поля опциональны"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    year: Optional[int] = Field(None, ge=1000, le=2100)
    author_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None


class Book(BookBase):
    """Схема для чтения книги из БД (с авторами и жанрами)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    authors: List[Author] = []
    genres: List[Genre] = []

    class Config:
        from_attributes = True
