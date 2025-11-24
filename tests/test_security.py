from app.core.security import hash_password, verify_password, create_jwt_token, decode_jwt_token, create_token_pair

def test_hash_and_verify_password():
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_jwt_token():
    user_id = 123
    secret = "mysecretkey"
    token = create_jwt_token(
        user_id, 
        secret, 
        expires_minutes=5,
        token_type='access'
    )
    assert isinstance(token, tuple)
    assert isinstance(token[0], str)
    assert isinstance(token[1], dict)
    
    payload = decode_jwt_token(token[0], secret)
    assert payload["user_id"] == user_id

def test_create_token_pair():
    user_id = 123
    secret = "mysecretkey"
    access_expires_minutes = 1
    refresh_expires_minutes = 100
    tokens = create_token_pair(
        user_id=user_id,
        secret=secret,
        access_expires_minutes=access_expires_minutes,
        refresh_expires_minutes=refresh_expires_minutes
    )
    assert isinstance(tokens, tuple)
    
    pair_tokens = tokens[0]
    access_token = pair_tokens.get("access_token")
    refresh_token = pair_tokens.get("refresh_token")
    assert decode_jwt_token(access_token, secret).get("type") == "access"
    assert decode_jwt_token(refresh_token, secret, "refresh").get("type") == "refresh"