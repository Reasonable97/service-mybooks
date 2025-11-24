from fastapi import FastAPI

from .database import engine, Base
from . import models  # импортируем модели, чтобы SQLAlchemy их знал

# Создаём таблицы в БД при старте приложения (если их ещё нет)
Base.metadata.create_all(bind=engine)

# Создаём экземпляр приложения FastAPI
app = FastAPI(title="MyBooks API")


# Простой health-check эндпоинт
@app.get("/health")
def health_check():
    return {"status": "ok"}
