from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from storage.db.database import SessionLocal
from storage.db.models import User
from core.jwt_auth import decode_access_token

security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(401, "Invalid token")
    
    username = payload.get("sub")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if not user:
        raise HTTPException(401, "invalid user")
    
    return user