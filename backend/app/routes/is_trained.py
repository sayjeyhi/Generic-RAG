from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.model import qa_chain

router = APIRouter()


@router.get("/")
async def ask():
    print("Checking if model is trained")
    if not qa_chain:
        print("Model was not trained")
        return JSONResponse(status_code=400,
                            content={"message": "Model is not trained yet. Please train the model first by calling /train."})

    print("Model was trained")
    return {"status": "trained"}
