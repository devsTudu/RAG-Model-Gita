from fastapi import FastAPI
from app.model_route import models_router
# from fastapi import Depends
# from utils.security import check

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(models_router)

