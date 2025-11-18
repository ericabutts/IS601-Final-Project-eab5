# calculation_factory.py

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Type

class CalculationOperation(ABC):
    """Abstract base class for calculation operations"""
    
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Execute the calculation operation"""
        pass


class AddOperation(CalculationOperation):
    """Addition operation"""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b


class SubtractOperation(CalculationOperation):
    """Subtraction operation"""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b


class MultiplyOperation(CalculationOperation):
    """Multiplication operation"""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b


class DivideOperation(CalculationOperation):
    """Division operation"""
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class CalculationFactory:
    """Factory for creating calculation operations"""
    
    _operations: Dict[str, Type[CalculationOperation]] = {
    "ADD": AddOperation,
    "SUBTRACT": SubtractOperation,
    "MULTIPLY": MultiplyOperation,
    "DIVIDE": DivideOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_type: str) -> CalculationOperation:
        """
        Create and return the appropriate calculation operation.
        
        Args:
            operation_type: The type of operation to create
            
        Returns:
            An instance of the appropriate CalculationOperation subclass
            
        Raises:
            ValueError: If operation_type is not supported
        """
        
        if operation_type not in cls._operations:
            raise ValueError(
                f"Unsupported operation: {operation_type}. "
                f"Supported operations: {', '.join(cls._operations.keys())}"
            )
        
        return cls._operations[operation_type]()
    
    @classmethod
    def get_supported_operations(cls) -> list:
        """Return list of supported operations"""
        return list(cls._operations.keys())


# Helper function to perform calculation
def perform_calculation(a: Decimal, b: Decimal, operation_type: str) -> Decimal:
    """
    Perform a calculation using the factory pattern.
    
    Args:
        a: First operand
        b: Second operand
        operation_type: Type of operation to perform
        
    Returns:
        Result of the calculation
    """
    operation = CalculationFactory.create_operation(operation_type)
    return operation.execute(a, b)