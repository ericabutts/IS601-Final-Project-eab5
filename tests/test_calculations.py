# import pytest
# from decimal import Decimal
# from unittest.mock import MagicMock
# from app.models import Calculation
# from main import app  # adjust to your FastAPI instance
# from fastapi.testclient import TestClient
# from app.routes_calculations import get_db  # adjust the path to where get_db is defined


# client = TestClient(app)

# OPERATION_MAP = {
#     "add": "ADD",
#     "subtract": "SUBTRACT",
#     "multiply": "MULTIPLY",
#     "divide": "DIVIDE",
# }

# @pytest.fixture
# def db(monkeypatch):
#     mock_db = MagicMock()
#     monkeypatch.setattr("app.routes_calculations.get_db", lambda: mock_db)
#     return mock_db

# @pytest.mark.parametrize(
#     "a,b,op,expected",
#     [
#         (5, 3, "add", Decimal(8)),
#         (10, 4, "subtract", Decimal(6)),
#         (2, 7, "multiply", Decimal(14)),
#         (20, 4, "divide", Decimal(5)),
#     ]
# )
# def test_create_calculation(db, a, b, op, expected):
#     payload = {
#         "a": str(a),
#         "b": str(b),
#         "type": OPERATION_MAP[op],
#         "user_id": 1
#     }

#     db_calc = MagicMock(spec=Calculation)
#     db_calc.id = 1
#     db_calc.a = Decimal(a)
#     db_calc.b = Decimal(b)
#     db_calc.type = OPERATION_MAP[op]
#     db_calc.result = expected
#     db_calc.user_id = 1

#     db.add.return_value = None
#     db.commit.return_value = None
#     db.refresh.side_effect = lambda x: setattr(x, "id", 1) or x

#     response = client.post("/calculations/", json=payload)

#     assert response.status_code == 201
#     data = response.json()

#     # Compare numeric values as float
#     assert float(data["a"]) == float(a)
#     assert float(data["b"]) == float(b)
#     assert data["type"] == OPERATION_MAP[op]
#     assert float(data["result"]) == float(expected)
#     assert data["user_id"] == 1


# import pytest
# from unittest.mock import MagicMock
# from decimal import Decimal
# from app.models import Calculation

# @pytest.fixture
# def mock_db():
#     db = MagicMock()
#     db_calc = MagicMock(spec=Calculation)
#     db_calc.id = 1
#     db_calc.a = Decimal(5)
#     db_calc.b = Decimal(3)
#     db_calc.type = "ADD"
#     db_calc.result = Decimal(8)
#     db_calc.user_id = 1

#     db.query.return_value.filter.return_value.first.return_value = db_calc
#     return db

# def test_get_calculation(mock_db):
#     # Override FastAPI dependency
#     app.dependency_overrides[get_db] = lambda: mock_db

#     response = client.get("/calculations/1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == 1
#     assert data["type"] == "ADD"
#     assert float(data["a"]) == 5.0
#     assert float(data["b"]) == 3.0
#     assert float(data["result"]) == 8.0

#     app.dependency_overrides.clear()

