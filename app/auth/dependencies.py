# app/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

# Tests expect no leading slash
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserResponse:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token → get user_id
    user_id = User.verify_token(token)
    if not user_id:
        raise credentials_exception

    # Query the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    # Tests expect a UserResponse, not the ORM model
    return UserResponse.from_orm(user)


def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """Tests expect it to return a UserResponse."""
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return current_user
