from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------
@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    # Check password confirmation
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        new_user = User.register(db, user_data.model_dump())
        db.commit()
        db.refresh(new_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Generate JWT token
    access_token = User.create_access_token({"sub": str(new_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(new_user)
    }


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):

    # Authenticate user by username or email
    user = User.authenticate(
        db=db,
        username=credentials.username,
        password=credentials.password
    )

    # Failed authentication → 401
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT
    token = User.create_access_token({"sub": str(user.id)})

    # Return full Token schema (required)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }
