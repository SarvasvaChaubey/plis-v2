from fastapi import APIRouter
from app.services.gemma_service import test_gemma

router = APIRouter()

@router.get("/test-gemma")
def test():
    return {"response": test_gemma()}