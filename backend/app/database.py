from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite: файл базы данных будет лежать рядом с backend (./mybooks.db)
DATABASE_URL = "sqlite:///./mybooks.db"

# Создаём движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # нужно для SQLite
)

# Фабрика сессий: через неё получаем объекты Session для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()
