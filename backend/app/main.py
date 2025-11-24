from fastapi import FastAPI

from .database import engine, Base
from . import models
from .routers import books  # импортируем роутер

# Создаём таблицы в БД при старте
Base.metadata.create_all(bind=engine)

# Создаём экземпляр приложения FastAPI
app = FastAPI(title="MyBooks API", version="1.0.0")

# Подключаем роутер книг
app.include_router(books.router)


# Health-check эндпоинт
@app.get("/health")
def health_check():
    return {"status": "ok"}
