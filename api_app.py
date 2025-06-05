from fastapi import FastAPI
from app.webapp.model_route import models_router
from app.telegrambot.endpoint import telegram_bot_router
# from fastapi import Depends
# from utils.security import check

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(models_router)
app.include_router(telegram_bot_router)
