# import pytest
# from pydantic import ValidationError
# from app.schemas import UserCreate, UserRead

# def test_user_create_valid():
#     data = {"username": "tester", "email": "tester@example.com", "password": "TestPass123"}
#     user = UserCreate(**data)
#     assert user.username == "tester"
#     assert user.email == "tester@example.com"
#     assert user.password == "TestPass123"

# def test_user_create_invalid_email():
#     data = {"username": "tester", "email": "not-an-email", "password": "TestPass123"}
#     with pytest.raises(ValidationError):
#         UserCreate(**data)

# def test_user_read_schema():
#     data = {"id": 1, "username": "tester", "email": "tester@example.com", "created_at": "2025-11-11T00:00:00"}
#     user = UserRead(**data)
#     assert user.username == "tester"
#     assert user.email == "tester@example.com"
