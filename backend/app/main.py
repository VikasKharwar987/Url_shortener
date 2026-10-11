from fastapi import FastAPI
from app.routes.url_routes import router
from app.routes import auth_routes

app = FastAPI()

app.include_router(router)
app.include_router(auth_routes.router)

@app.get("/")
def home():
    return {"message": "backend is working"}