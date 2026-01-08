"""
Authentication and Authorization Utilities
JWT token generation, password hashing, role/permission checking
"""
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.auth import Role, Permission, UserRole, RolePermission, RefreshToken

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt directly"""
    try:
        # Ensure password is <= 72 bytes
        pwd_bytes = plain_password.encode('utf-8')
        if len(pwd_bytes) > 72:
            pwd_bytes = pwd_bytes[:72]
            while pwd_bytes and (pwd_bytes[-1] & 0xC0) == 0x80:
                pwd_bytes = pwd_bytes[:-1]
            plain_password = pwd_bytes.decode('utf-8', errors='ignore')
        
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt directly - truncate to 72 bytes if needed"""
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Convert to bytes
    pwd_bytes = password.encode('utf-8')
    
    # Truncate to 72 bytes if longer (bcrypt's limit)
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        # Remove incomplete UTF-8 sequences
        while pwd_bytes and (pwd_bytes[-1] & 0xC0) == 0x80:
            pwd_bytes = pwd_bytes[:-1]
    
    # Hash using bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # JWT exp must be Unix timestamp (seconds since epoch)
    # Calculate UTC timestamp manually since utcnow() returns naive datetime
    if expire.tzinfo is None:
        # Naive datetime - assume UTC and convert to timestamp
        expire_ts = (expire - datetime(1970, 1, 1)).total_seconds()
    else:
        expire_ts = expire.timestamp()
    
    to_encode.update({"exp": int(expire_ts), "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=30)  # Refresh tokens last 30 days
    
    # JWT exp must be Unix timestamp (seconds since epoch)
    # Calculate UTC timestamp manually since utcnow() returns naive datetime
    if expire.tzinfo is None:
        # Naive datetime - assume UTC and convert to timestamp
        expire_ts = (expire - datetime(1970, 1, 1)).total_seconds()
    else:
        expire_ts = expire.timestamp()
    
    to_encode.update({"exp": int(expire_ts), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            print(f"[Auth] Token type mismatch: expected '{token_type}', got '{payload.get('type')}'")
            return None
        return payload
    except JWTError as e:
        print(f"[Auth] JWT decode error: {str(e)}")
        return None
    except Exception as e:
        print(f"[Auth] Unexpected error verifying token: {str(e)}")
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f"[Auth] Verifying token: {token[:50]}...")
    payload = verify_token(token)
    if payload is None:
        print("[Auth] Token verification failed - payload is None")
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        print(f"[Auth] No user_id in payload: {payload}")
        raise credentials_exception
    
    # Convert string back to int for database query
    try:
        user_id: int = int(user_id_str)
    except (ValueError, TypeError):
        print(f"[Auth] Invalid user_id format in token: {user_id_str}")
        raise credentials_exception
    
    print(f"[Auth] Looking up user with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print(f"[Auth] User not found with ID: {user_id}")
        raise credentials_exception
    
    if not user.is_active:
        print(f"[Auth] User {user_id} is inactive")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    
    print(f"[Auth] User authenticated: {user.email} (ID: {user.id})")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    return current_user


def get_user_roles(db: Session, user_id: int) -> List[str]:
    """Get all role names for a user"""
    # Check if user is superuser
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.is_superuser:
        return ["superuser"]
    
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    return [ur.role.role_name for ur in user_roles if ur.role]


def get_user_permissions(db: Session, user_id: int) -> List[str]:
    """Get all permission names for a user"""
    # Get all roles for user
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    role_ids = [ur.role_id for ur in user_roles]
    
    if not role_ids:
        return []
    
    # Get all permissions for those roles
    role_permissions = db.query(RolePermission).filter(
        RolePermission.role_id.in_(role_ids)
    ).all()
    
    return [rp.permission.permission_name for rp in role_permissions if rp.permission]


def check_permission(db: Session, user_id: int, permission_name: str) -> bool:
    """Check if user has a specific permission"""
    permissions = get_user_permissions(db, user_id)
    return permission_name in permissions


def check_role(db: Session, user_id: int, role_name: str) -> bool:
    """Check if user has a specific role"""
    roles = get_user_roles(db, user_id)
    return role_name in roles or role_name == "superuser"  # Superuser has all roles


def require_permission(permission_name: str):
    """Dependency to require a specific permission"""
    async def permission_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        if current_user.is_superuser:
            return current_user
        
        if not check_permission(db, current_user.id, permission_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission_name}"
            )
        return current_user
    
    return permission_checker


def require_role(role_name: str):
    """Dependency to require a specific role"""
    async def role_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        if current_user.is_superuser:
            return current_user
        
        if not check_role(db, current_user.id, role_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {role_name}"
            )
        return current_user
    
    return role_checker


def require_admin():
    """Dependency to require admin role"""
    return require_role("admin")

