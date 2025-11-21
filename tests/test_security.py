from app.core.security import hash_password, verify_password, create_jwt_token, decode_jwt_token

def test_hash_and_verify_password():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_jwt_token():
    user_id = 123
    secret = "mysecretkey"
    token = create_jwt_token(user_id, secret, expires_minutes=5)
    assert isinstance(token, str)
    payload = decode_jwt_token(token, secret)
    assert payload["user_id"] == user_id