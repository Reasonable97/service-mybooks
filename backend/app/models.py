from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship

from .database import Base


class Author(Base):
    """Модель автора книги"""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Связь "многие ко многим" с Book через BookAuthor
    books = relationship("BookAuthor", back_populates="author")


class Genre(Base):
    """Модель жанра"""
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Связь "многие ко многим" с Book через BookGenre
    books = relationship("BookGenre", back_populates="genre")


class Book(Base):
    """Модель книги"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Связи "многие ко многим" к Author и Genre через промежуточные таблицы
    authors = relationship("BookAuthor", back_populates="book", cascade="all, delete-orphan")
    genres = relationship("BookGenre", back_populates="book", cascade="all, delete-orphan")


class BookAuthor(Base):
    """Промежуточная таблица связи Book и Author (many-to-many)"""
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True)
    author_role = Column(String(50), nullable=True)  # роль автора: Lead, Co-author и т.д.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Связи к Book и Author
    book = relationship("Book", back_populates="authors")
    author = relationship("Author", back_populates="books")


class BookGenre(Base):
    """Промежуточная таблица связи Book и Genre (many-to-many)"""
    __tablename__ = "book_genres"

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Связи к Book и Genre
    book = relationship("Book", back_populates="genres")
    genre = relationship("Genre", back_populates="books")
