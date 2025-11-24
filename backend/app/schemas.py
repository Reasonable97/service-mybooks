from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# ========== Схемы для автора ==========

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
        from_attributes = True


# ========== Схемы для жанра ==========

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


# ========== Схемы для книги ==========

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    year: Optional[int] = Field(None, ge=1000, le=2100)


class BookCreate(BookBase):
    """Схема для создания книги"""
    author_ids: List[int] = Field(default_factory=list)
    genre_ids: List[int] = Field(default_factory=list)


class BookUpdate(BaseModel):
    """Схема для PATCH-обновления: все поля опциональны"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    year: Optional[int] = Field(None, ge=1000, le=2100)
    author_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None


class Book(BookBase):
    """Схема для чтения книги из БД"""
    id: int  # id на первом месте
    title: str
    year: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    authors: List[Author] = []
    genres: List[Genre] = []

    class Config:
        from_attributes = True


# ========== Обёртки для списковых ответов с пагинацией ==========

class PaginatedResponse(BaseModel):
    """Базовая схема для пагинированных ответов"""
    page: int = Field(..., description="Номер текущей страницы (начиная с 1)")
    size: int = Field(..., description="Количество элементов на странице")
    total: int = Field(..., description="Общее количество элементов")


class BookListResponse(PaginatedResponse):
    """Ответ со списком книг"""
    items: List[Book] = Field(default_factory=list, description="Список книг")


class AuthorListResponse(PaginatedResponse):
    """Ответ со списком авторов"""
    items: List[Author] = Field(default_factory=list, description="Список авторов")


class GenreListResponse(PaginatedResponse):
    """Ответ со списком жанров"""
    items: List[Genre] = Field(default_factory=list, description="Список жанров")
