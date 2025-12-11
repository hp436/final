from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


# ------------------------------------------------------
# REGISTER USER
# ------------------------------------------------------
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):

    try:
        new_user = User.register(db, payload.model_dump())
        db.commit()
        db.refresh(new_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = User.create_access_token({"sub": str(new_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }


# ------------------------------------------------------
# LOGIN USER
# ------------------------------------------------------
@router.post("/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):

    auth_result = User.authenticate(db, payload.username, payload.password)

    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return auth_result