from fastapi import FastAPI
from .routes.train import router as train_router
from .routes.ask import router as ask_router

app = FastAPI()

app.include_router(train_router, prefix="/train", tags=["train"])
app.include_router(ask_router, prefix="/ask", tags=["ask"])
