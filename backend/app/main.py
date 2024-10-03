from fastapi import FastAPI
from .routes.train import router as train_router
from .routes.ask import router as ask_router
from .routes.is_trained import router as is_trained_router

app = FastAPI()

app.include_router(train_router, prefix="/train", tags=["train"])
app.include_router(ask_router, prefix="/ask", tags=["ask"])
app.include_router(is_trained_router, prefix="/is_trained", tags=["is_trained"])
