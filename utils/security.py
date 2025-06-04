import requests
from jose import jwt
from functools import lru_cache
from datetime import datetime
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader


token_key = APIKeyHeader(name='token') 
secret = APIKeyHeader(name='key')

@lru_cache(maxsize=1)
def get_firebase_public_keys():
    """Fetch Google's public keys for token verification"""
    response = requests.get(
        'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'
    )
    return response.json()

async def verify_token(token: str = Depends(token_key)) -> dict:
    """
    Verify Firebase JWT token using public keys
    """
    try:
        # Get the kid from the headers prior to verification
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        
        # Get the public keys
        public_keys = get_firebase_public_keys()
        
        # Get the right key
        public_key = public_keys[kid]
        
        # Verify the token
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience='gita-app-cvcjjm'  # Your Firebase project ID
        )
        
        # Verify time-based claims
        now = datetime.utcnow().timestamp()
        if decoded_token['exp'] < now:
            raise HTTPException(400,
                                "Token Expired")
        
        return decoded_token
        
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )


async def check(key = Depends(secret)):
    if key == "hello":
        return "Hi"
    
    raise HTTPException(400,"Unauthorised")
