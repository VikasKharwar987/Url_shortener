from fastapi import FastAPI
from app.routes.url_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "backend is working"}