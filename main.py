# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from fastapi.exceptions import RequestValidationError

# Calculator operations
from app.operations import add, subtract, multiply, divide

# Routers
from app.routers import auth
from app.routers import user
from app.routers import calculations

# Database
from app.database import Base, engine, SessionLocal
from app.models.user import User

import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ---------------------------------------------------------
# CREATE DATABASE TABLES FIRST (MUST COME BEFORE SEED)
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# SEED DEFAULT PLAYWRIGHT TEST USER (RUNS AFTER TABLES EXIST)
# ---------------------------------------------------------
@app.on_event("startup")
def seed_test_user():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "test@test.com").first()
        if not existing:
            user = User(
                first_name="Test",
                last_name="User",
                email="test@test.com",
                username="test@test.com"
            )
            user.password = "password"
            db.add(user)
            db.commit()
            logger.info("Seeded default Playwright test user")
        else:
            logger.info("Default test user already exists")
    finally:
        db.close()

# ---------------------------------------------------------
# TEMPLATES (Front-end pages)
# ---------------------------------------------------------
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------
# FRONT-END ROUTES
# ---------------------------------------------------------
@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/calculations/page")
async def calculations_page(request: Request):
    return templates.TemplateResponse("calculations.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ---------------------------------------------------------
# REGISTER BACKEND ROUTERS
# ---------------------------------------------------------
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(calculations.router)

# ---------------------------------------------------------
# Calculator Schemas
# ---------------------------------------------------------
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value


class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

# ---------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )

# ---------------------------------------------------------
# BASIC ROUTES
# ---------------------------------------------------------
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e:
        logger.error(f"Divide Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Divide Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
