# tests/test_calculation_factory.py - Factory Pattern Unit Tests

import pytest
from decimal import Decimal
from app.calculation_factory import (
    CalculationFactory,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    perform_calculation
)


class TestCalculationFactory:
    """Unit tests for the Calculation Factory Pattern"""
    
    def test_create_add_operation(self):
        """Test factory creates AddOperation"""
        operation = CalculationFactory.create_operation("ADD")
        assert isinstance(operation, AddOperation)
    
    def test_create_subtract_operation(self):
        """Test factory creates SubtractOperation"""
        operation = CalculationFactory.create_operation("SUBTRACT")
        assert isinstance(operation, SubtractOperation)
    
    def test_create_multiply_operation(self):
        """Test factory creates MultiplyOperation"""
        operation = CalculationFactory.create_operation("MULTIPLY")
        assert isinstance(operation, MultiplyOperation)
    
    def test_create_divide_operation(self):
        """Test factory creates DivideOperation"""
        operation = CalculationFactory.create_operation("DIVIDE")
        assert isinstance(operation, DivideOperation)
    
    def test_invalid_operation_type(self):
        """Test factory raises error for invalid operation"""
        with pytest.raises(ValueError, match="Unsupported operation"):
            CalculationFactory.create_operation("INVALID")


class TestCalculationOperations:
    """Unit tests for calculation operations"""
    
    def test_addition(self):
        """Test addition operation"""
        result = perform_calculation(Decimal("10"), Decimal("5"), "ADD")
        assert result == Decimal("15")
    
    def test_addition_negative(self):
        """Test addition with negative numbers"""
        result = perform_calculation(Decimal("-10"), Decimal("5"), "ADD")
        assert result == Decimal("-5")
    
    def test_subtraction(self):
        """Test subtraction operation"""
        result = perform_calculation(Decimal("10"), Decimal("5"), "SUBTRACT")
        assert result == Decimal("5")
    
    def test_multiplication(self):
        """Test multiplication operation"""
        result = perform_calculation(Decimal("10"), Decimal("5"), "MULTIPLY")
        assert result == Decimal("50")
    
    def test_multiplication_zero(self):
        """Test multiplication by zero"""
        result = perform_calculation(Decimal("10"), Decimal("0"), "MULTIPLY")
        assert result == Decimal("0")
    
    def test_division(self):
        """Test division operation"""
        result = perform_calculation(Decimal("10"), Decimal("5"), "DIVIDE")
        assert result == Decimal("2")
    
    def test_division_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            perform_calculation(Decimal("10"), Decimal("0"), "DIVIDE")
    
    def test_decimal_precision(self):
        """Test decimal precision is maintained"""
        result = perform_calculation(Decimal("10.5"), Decimal("2.3"), "ADD")
        assert result == Decimal("12.8")


# tests/test_calculation_schemas.py - Pydantic Schema Tests

import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.schemas import CalculationCreate
from app.models import OperationType


class TestCalculationSchemas:
    """Unit tests for Pydantic validation"""
    
    def test_valid_calculation_add(self):
        """Test valid ADD calculation"""
        calc = CalculationCreate(
            a=Decimal("10"),
            b=Decimal("5"),
            type=OperationType.ADD
        )
        assert calc.a == Decimal("10")
        assert calc.b == Decimal("5")
        assert calc.type == OperationType.ADD
    
    def test_valid_calculation_subtract(self):
        """Test valid SUBTRACT calculation"""
        calc = CalculationCreate(
            a=Decimal("20"),
            b=Decimal("8"),
            type=OperationType.SUBTRACT
        )
        assert calc.type == OperationType.SUBTRACT
    
    def test_valid_calculation_multiply(self):
        """Test valid MULTIPLY calculation"""
        calc = CalculationCreate(
            a=Decimal("7"),
            b=Decimal("6"),
            type=OperationType.MULTIPLY
        )
        assert calc.type == OperationType.MULTIPLY
    
    def test_valid_calculation_divide(self):
        """Test valid DIVIDE calculation"""
        calc = CalculationCreate(
            a=Decimal("100"),
            b=Decimal("4"),
            type=OperationType.DIVIDE
        )
        assert calc.type == OperationType.DIVIDE
    
    def test_division_by_zero_validation(self):
        """Test division by zero is rejected"""
        with pytest.raises(ValidationError, match="Cannot divide by zero"):
            CalculationCreate(
                a=Decimal("10"),
                b=Decimal("0"),
                type=OperationType.DIVIDE
            )
    
    def test_negative_numbers_allowed(self):
        """Test negative numbers are allowed"""
        calc = CalculationCreate(
            a=Decimal("-10"),
            b=Decimal("-5"),
            type=OperationType.ADD
        )
        assert calc.a == Decimal("-10")
    
    def test_zero_allowed_for_non_division(self):
        """Test zero is allowed for operations other than division"""
        calc = CalculationCreate(
            a=Decimal("10"),
            b=Decimal("0"),
            type=OperationType.ADD
        )
        assert calc.b == Decimal("0")
    
    def test_optional_user_id(self):
        """Test user_id is optional"""
        calc = CalculationCreate(
            a=Decimal("10"),
            b=Decimal("5"),
            type=OperationType.ADD
        )
        assert calc.user_id is None
    
    def test_with_user_id(self):
        """Test calculation with user_id"""
        calc = CalculationCreate(
            a=Decimal("10"),
            b=Decimal("5"),
            type=OperationType.ADD,
            user_id=1
        )
        assert calc.user_id == 1


# tests/test_calculation_routes.py - Route Tests (Mocked Database)

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from decimal import Decimal
from main import app
from app.models import Calculation, OperationType


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestCalculationRoutes:
    """Test calculation routes with mocked database"""
    
    @patch('app.routes_calculations.get_db')
    def test_create_calculation_success(self, mock_get_db, client):
        """Test successful calculation creation"""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Mock the calculation that would be saved
        mock_calc = Calculation(
            id=1,
            a=Decimal("10"),
            b=Decimal("5"),
            type=OperationType.ADD,
            result=Decimal("15")
        )
        mock_db.refresh = MagicMock(side_effect=lambda x: setattr(x, 'id', 1))
        
        response = client.post(
            "/calculations/",
            json={
                "a": 10,
                "b": 5,
                "type": "ADD"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "result" in data
        assert data["type"] == "ADD"
    
    def test_division_by_zero_rejected(self, client):
        """Test division by zero is rejected at schema level"""
        response = client.post(
            "/calculations/",
            json={
                "a": 10,
                "b": 0,
                "type": "DIVIDE"
            }
        )
        
        # Should fail validation
        assert response.status_code == 422
    
    def test_invalid_operation_type(self, client):
        """Test invalid operation type is rejected"""
        response = client.post(
            "/calculations/",
            json={
                "a": 10,
                "b": 5,
                "type": "INVALID"
            }
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client):
        """Test missing required fields"""
        response = client.post(
            "/calculations/",
            json={
                "a": 10
                # Missing b and type
            }
        )
        
        assert response.status_code == 422
    
    def test_invalid_number_format(self, client):
        """Test invalid number format"""
        response = client.post(
            "/calculations/",
            json={
                "a": "not_a_number",
                "b": 5,
                "type": "ADD"
            }
        )
        
        assert response.status_code == 422