import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# -----------------------------
# Import app modules
# -----------------------------
from app import models, crud
from app.database import engine, get_db
from app.schemas import UserCreate, UserRead, LoginRequest
from app.calculator import Calculator
from app.operations import OperationFactory
from app.routes_calculations import router as calculation_router
from app import schemas

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(title="FastAPI Calculator + Users")

# Mount frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="frontend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Create database tables
# -----------------------------
models.Base.metadata.create_all(bind=engine)

# -----------------------------
# Include routers
# -----------------------------
from app.auth import router as auth_router
app.include_router(auth_router)
app.include_router(calculation_router)

# -----------------------------
# Calculator Setup
# -----------------------------
calc = Calculator()

@app.get("/calculate/{op_name}")
def api_calculate(op_name: str, a: float, b: float):
    try:
        operation = OperationFactory.create_operation(op_name)
        calc.set_operation(operation)
        result = calc.perform_operation(a, b)
        return {"result": float(result)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------------
# Auth routes (login/register)
# -----------------------------
from fastapi import Body

from app.auth import create_access_token

@app.post("/register", response_model=schemas.Token)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # optional: default username to email if not sent
    if not user_in.username:
        user_in.username = user_in.email

    existing_user = db.query(models.User).filter(
        (models.User.username == user_in.username) |
        (models.User.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    user = crud.create_user(db, user_in)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}



# -----------------------------
# CLI REPL (optional)
# -----------------------------
def init_db():
    from app import models
    from app.database import engine
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    from app.calculator_repl import calculator_repl
    calculator_repl()
