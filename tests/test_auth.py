import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService

def test_registeruser_success():
    user_repo_mock = MagicMock()
    user_repo_mock.get_by_email.return_value = None
    user_repo_mock.create.return_value = MagicMock(id="user123")
    
    with patch('app.services.auth_service.hash_password', return_value='hashed_pwd'), \
        patch('app.services.auth_service.create_jwt_token', return_value='jwt_token'):
        
        service = AuthService(user_repo=user_repo_mock, jwt_secret="secret", jwt_expire_minutes=30)
        token = service.register_user(email="test@example.com", password="password", name="Test User")
        
        
        user_repo_mock.create.assert_called_once_with("test@example.com", "hashed_pwd", "Test User")
        
        assert token == 'jwt_token'

def test_registeruser_email_already_exists():
    user_repo_mock = MagicMock()
    user_repo_mock.get_by_email.return_value = MagicMock()
    
    service = AuthService(user_repo=user_repo_mock, jwt_secret="secret", jwt_expire_minutes=30)
    
    with pytest.raises(RuntimeError, match="Email already in use"):
        service.register_user(email="test@example.com", password="password", name="Test User")