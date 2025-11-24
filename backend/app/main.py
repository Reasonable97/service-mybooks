from fastapi import FastAPI

# Создаём экземпляр приложения FastAPI
app = FastAPI(title="MyBooks API")

# Простой health-check эндпоинт
@app.get("/health")
def health_check():
    return {"status": "ok"}
