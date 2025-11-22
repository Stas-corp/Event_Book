from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def register_user():
    return 'Ok'
