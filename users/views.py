from fastapi import APIRouter

from users import crud
from users.schemas import CreateUser


router = APIRouter(prefix="/users", tags=[])


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user_crud(user_in=user)
