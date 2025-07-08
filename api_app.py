from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from app.webapp.model_route import models_router
from app.telegrambot.endpoint import telegram_bot_router

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(models_router)
app.include_router(telegram_bot_router)


def run_app():
    uvicorn.run(app)
