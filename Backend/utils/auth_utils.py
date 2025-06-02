# app/routers/auth_utils.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Backend.config import SECRET_KEY, ALGORITHM
from Backend.database import SessionLocal
from Backend.services.user_service import get_user_by_name
from Backend.models.user import User as UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# 用于解析 token 后的数据结构
class TokenData(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    """
    1. 从 Authorization: Bearer <token> 中拿到 token
    2. jwt.decode 验证签名和 exp
    3. payload['sub'] 即当初我们 put 进去的 username
    4. 根据 username 去数据库查用户，查不到或过期就抛 401
    5. 返回 UserModel 实例，注入到路由里
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码并验证 token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str  = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # 根据 username 拿到 User 实例
    user = get_user_by_name(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
