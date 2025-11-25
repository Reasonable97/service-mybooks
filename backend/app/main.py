from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from . import models
from .routers import books, authors, genres  # импортируем роутеры

# Создаём таблицы в БД при старте
Base.metadata.create_all(bind=engine)

# Создаём экземпляр приложения FastAPI
app = FastAPI(title="MyBooks API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутер книг
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)


# Health-check эндпоинт
@app.get("/health")
def health_check():
    return {"status": "ok"}
