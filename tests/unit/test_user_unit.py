# tests/unit/test_user_unit.py

import pytest
from app.models.user import User, pwd_context
from app.schemas.base import UserCreate


def test_hash_password_valid():
    """Ensure hashing works and password is not stored in plain text."""
    password = "MySecret123"
    hashed = User.hash_password(password)

    assert hashed != password
    assert pwd_context.verify(password[:72], hashed)


def test_verify_password_correct():
    """verify_password should return True for correct password."""
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        username="testuser",
        password_hash=User.hash_password("Password123")
    )

    assert user.verify_password("Password123") is True


def test_verify_password_wrong():
    """verify_password should return False for wrong password."""
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        username="testuser",
        password_hash=User.hash_password("Password123")
    )

    assert user.verify_password("WrongPass") is False


def test_user_create_schema_valid():
    """Pydantic schema validation should succeed for correct input."""
    data = {
        "first_name": "Amitha",
        "last_name": "Reddy",
        "email": "amitha@example.com",
        "username": "amitha7",
        "password": "StrongPass123"
    }

    obj = UserCreate(**data)

    assert obj.email == "amitha@example.com"
    assert obj.username == "amitha7"


def test_user_create_schema_invalid_email():
    """Schema should reject invalid email addresses."""
    data = {
        "first_name": "Amitha",
        "last_name": "Reddy",
        "email": "bademail",
        "username": "arb",
        "password": "StrongPass123"
    }

    with pytest.raises(ValueError):
        UserCreate(**data)


def test_jwt_token_round_trip():
    """JWT token created should decode back to the original user ID."""
    token = User.create_access_token({"sub": "12345678-1234-1234-1234-123456789000"})

    decoded = User.verify_token(token)

    assert str(decoded) == "12345678-1234-1234-1234-123456789000"