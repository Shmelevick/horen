from fastapi import APIRouter, Response, Depends, HTTPException, status, Form
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel
from jwt import InvalidTokenError

from icecream import ic

from users.schemas import UserSchema
from auth import utils as auth_utils


router = APIRouter(prefix="/jwt", tags=["JWT"])

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/jwt/login/")


john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("qwerty"),
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


users_db: dict[str, UserSchema] = {john.username: john, sam.username: sam}


def validate_auth_user(username: str = Form(), password: str = Form()):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not auth_utils.validate_password(password, user.password):
        raise unauthed_exc
    return user


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # ic(credentials)
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid  token error: {e}",
        ) from e
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    )


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    response: Response, user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(payload=jwt_payload)
    response.set_cookie("Bearer", token)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/users/me")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_auth_user),
):
    return {"username": user.username, "email": user.email}
