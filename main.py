from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.calculator import Calculator
from app.operations import AddOperation, SubtractOperation, OperationFactory
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("Calculator imported:", Calculator)
print("AddOperation imported:", AddOperation)


app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="frontend")


# Optional: allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create calculator instance
calc = Calculator()

@app.get("/calculate/{op_name}")
def api_add(op_name: str, a: float, b: float):
    try:
        operation = OperationFactory.create_operation(op_name)
        calc.set_operation(operation)
        result = calc.perform_operation(a, b)
        return {"result": float(result)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# CLI REPL (optional)
if __name__ == "__main__":
    from app.calculator_repl import calculator_repl
    calculator_repl()
