from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from ..services.data_loader import process_file, process_youtube_link
from ..services.model import train_model

router = APIRouter()

@router.post("/")
async def train(file: UploadFile = File(None), youtube_link: str = Form(None)):
    print(file)
    if file:
        contents = await file.read()
        split_docs = process_file(contents, file.filename)
    elif youtube_link:
        print("\n\n\n========\n========\n========\nyoutube_link")
        print(youtube_link)
        split_docs = process_youtube_link(youtube_link)
    else:
        return JSONResponse(status_code=400, content={"message": "No file or YouTube link provided"})

    train_model(split_docs)
    return {"message": "Training completed successfully"}
