from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.data_loader import process_youtube_link
from ..services.model import train_model
from ..schemas.main import Train_YoutubeRequest

router = APIRouter()

@router.post("/")
async def train(request: Train_YoutubeRequest):
    if request.youtube_link:
        print(request.youtube_link)
        split_docs = process_youtube_link(request.youtube_link)
    else:
        return JSONResponse(status_code=400, content={"message": "No YouTube link provided"})

    train_model(split_docs)
    return {"message": "Training completed successfully"}
