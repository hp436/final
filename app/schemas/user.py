from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# -----------------------------
# Schema for creating a user
# -----------------------------
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "john@example.com",
                "password": "StrongPass123"
            }
        }
    )


# -----------------------------
# Schema for reading user data (no password)
# -----------------------------
class UserRead(BaseModel):
    """Return user information without password fields"""
    id: UUID
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# Full user response schema
# -----------------------------
class UserResponse(BaseModel):
    """Schema for full user response object"""
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# Token schema
# -----------------------------
class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "jwt.token.here",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "email": "john@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_verified": False,
                    "created_at": "2025-01-01T00:00:00",
                    "updated_at": "2025-01-08T12:00:00",
                },
            }
        }
    )


# -----------------------------
# Token payload schema
# -----------------------------
class TokenData(BaseModel):
    """Schema for JWT token payload"""
    user_id: Optional[UUID] = None


# -----------------------------
# Login schema
# -----------------------------
class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe123",
                "password": "SecurePass123",
            }
        }
    )