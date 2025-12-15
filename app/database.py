import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Environment-aware database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging, optional

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#---------------------------------------------------
# TEST DATABASE
#---------------------------------------------------

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# Base = declarative_base()

# # Production DB
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Test DB (in-memory)
# TestingEngine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestingEngine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
