from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from . import models, schemas


# ========== CRUD для книг ==========

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Получить список книг с пагинацией и общим количеством"""
    query = db.query(models.Book).options(
        joinedload(models.Book.authors).joinedload(models.BookAuthor.author),
        joinedload(models.Book.genres).joinedload(models.BookGenre.genre),
    )
    
    total = query.count()  # общее количество книг
    items = query.offset(skip).limit(limit).all()  # книги для текущей страницы
    
    return {"items": items, "total": total}



def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Получить книгу по ID с авторами и жанрами"""
    return (
        db.query(models.Book)
        .options(
            joinedload(models.Book.authors).joinedload(models.BookAuthor.author),
            joinedload(models.Book.genres).joinedload(models.BookGenre.genre),
        )
        .filter(models.Book.id == book_id)
        .first()
    )


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """Создать новую книгу с привязкой к авторам и жанрам"""
    # Создаём объект книги
    db_book = models.Book(
        title=book.title,
        year=book.year,
    )
    db.add(db_book)
    db.flush()  # чтобы получить ID книги до commit

    # Привязываем авторов
    for author_id in book.author_ids:
        book_author = models.BookAuthor(book_id=db_book.id, author_id=author_id)
        db.add(book_author)

    # Привязываем жанры
    for genre_id in book.genre_ids:
        book_genre = models.BookGenre(book_id=db_book.id, genre_id=genre_id)
        db.add(book_genre)

    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.Book]:
    """Частично обновить книгу (PATCH)"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None

    # Обновляем основные поля, если они переданы
    if book_update.title is not None:
        db_book.title = book_update.title
    if book_update.year is not None:
        db_book.year = book_update.year

    # Обновляем авторов, если передан список
    if book_update.author_ids is not None:
        # Удаляем старые связи
        db.query(models.BookAuthor).filter(models.BookAuthor.book_id == book_id).delete()
        # Создаём новые
        for author_id in book_update.author_ids:
            db.add(models.BookAuthor(book_id=book_id, author_id=author_id))

    # Обновляем жанры, если передан список
    if book_update.genre_ids is not None:
        db.query(models.BookGenre).filter(models.BookGenre.book_id == book_id).delete()
        for genre_id in book_update.genre_ids:
            db.add(models.BookGenre(book_id=book_id, genre_id=genre_id))

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """Удалить книгу по ID"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return False

    db.delete(db_book)
    db.commit()
    return True


# ========== Вспомогательные CRUD для авторов и жанров ==========

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    """Получить всех авторов с пагинацией"""
    query = db.query(models.Author)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"items": items, "total": total}


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    """Получить автора по ID"""
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Создать автора"""
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_genres(db: Session, skip: int = 0, limit: int = 100):
    """Получить все жанры с пагинацией"""
    query = db.query(models.Genre)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"items": items, "total": total}


def get_genre(db: Session, genre_id: int) -> Optional[models.Genre]:
    """Получить жанр по ID"""
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def create_genre(db: Session, genre: schemas.GenreCreate) -> models.Genre:
    """Создать жанр"""
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre
