from fastapi import APIRouter, Response, Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    OAuth2,
)
from pydantic import BaseModel


from api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from api_v1.demo_auth.http_bearer import http_bearer
from api_v1.demo_auth.validation import (
    get_current_auth_user,
    validate_auth_user,
    get_current_auth_user_for_refresh,
)
from users.schemas import UserSchema


router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    response: Response, user: UserSchema = Depends(validate_auth_user)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response.set_cookie("Bearer", access_token)  # По приколу, неверно
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/users/me")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_auth_user),
):
    return {"username": user.username, "email": user.email}
