from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from config.variables import JWT_CONFIG
# from config.database import db
# from main import oauth2_scheme
import jwt


from datetime import timezone
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="github/login")


credentials_exception = HTTPException(
    status_code=401,
    detail="Invalid Token Sent",
    headers={"WWW-Authenticate": "Bearer"},
)


def generate_access_token(
        access_token: str,
        username: str,
        expires_in: int = JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"]):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_in)
    to_encode = {
        "access_token": access_token,
        "exp": expire, "iat": now,
        "username": username
    }
    return jwt.encode(
        to_encode,
        JWT_CONFIG["SECRET_KEY"],
        algorithm=JWT_CONFIG["ALGORITHM"])


async def decode_access_token(token: str):
    return jwt.decode(
        token,
        JWT_CONFIG["SECRET_KEY"],
        algorithms=JWT_CONFIG["ALGORITHM"])


async def get_current_token(token: str = Depends(oauth2_scheme)):
    try:
        token_info = await decode_access_token(token)
        access_token = token_info.get('access_token')
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(status_code=403, detail="Token Expired") from e
    except Exception as e:
        raise credentials_exception from e
    return access_token


async def get_current_username(token: str = Depends(oauth2_scheme)):
    try:
        token_info = await decode_access_token(token)
        username = token_info.get('username')
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(status_code=403, detail="Token Expired") from e
    except Exception as e:
        raise credentials_exception from e
    return username
