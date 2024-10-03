from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from ..services.data_loader import process_file
from ..services.model import train_model

router = APIRouter()

@router.post("/")
async def train(file: UploadFile = File(None), youtube_link: str = Form(None)):
    if file:
        contents = await file.read()
        split_docs = process_file(contents, file.filename)
    else:
        return JSONResponse(status_code=400, content={"message": "No file or YouTube link provided"})

    train_model(split_docs)
    return {"message": "Training completed successfully"}
