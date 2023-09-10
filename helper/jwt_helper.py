import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)

public_key = private_key.public_key()

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def generate_jwt_token(algorithm="RS256", **kwargs) -> str:
    try:
        payload = {"exp": datetime.now() + timedelta(minutes=15)}
        payload.update(kwargs)
        token = jwt.encode(payload, private_key, algorithm=algorithm)
    except Exception as e:
        token = None 
    return token

def decode_jwt_token(token, algorithm="RS256") -> dict:
    try:
        decoded = jwt.decode(token, public_key, algorithms=algorithm)
    except jwt.InvalidSignatureError as e:
        decoded = jwt.decode(token, algorithms=algorithm, options={"verify_signature": False})
    except Exception as e:
        decoded = None
    return decoded

def validate_jwt_token(token, algorithm="RS256") -> (bool, Exception):
    jwt_valid = False
    jwt_error = None
    try:
        jwt.decode(token, public_key, algorithms=algorithm)
        jwt_valid = True
    except Exception as e:
        jwt_error = e
    return (jwt_valid, jwt_error)