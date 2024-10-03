from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..schemas.ask_request import AskRequest
from ..services.model import qa_chain

router = APIRouter()

@router.post("/")
async def ask(request: AskRequest):
    if not qa_chain:
        return JSONResponse(status_code=400, content={"message": "Model is not trained yet. Please train the model first."})

    response = qa_chain(request.question)

    if not response:
        return JSONResponse(status_code=400, content={"message": "Model is not trained yet. Please train the model first."})

    return {"answer": response}