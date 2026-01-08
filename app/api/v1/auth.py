"""
Authentication API Endpoints
Login, registration, token refresh, role/permission management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.core.database import get_db
from app.core.auth import (
    verify_password, get_password_hash, create_access_token, create_refresh_token,
    verify_token, get_current_active_user, get_user_roles, get_user_permissions,
    require_admin, require_permission
)
from app.models.user import User
from app.models.auth import Role, Permission, UserRole, RolePermission, RefreshToken, LoginAttempt
from app.schemas.auth import (
    Token, LoginRequest, RefreshTokenRequest, RegisterRequest, ChangePasswordRequest,
    UserResponse, RoleCreate, RoleResponse, PermissionResponse, AssignRoleRequest, UpdateUserRequest
)
from app.core.config import settings

router = APIRouter(tags=["Authentication"])


@router.post("/auth/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    # Track login attempt
    attempt = LoginAttempt(
        email=login_data.email,
        success=False,
    )
    
    # Find user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        attempt.failure_reason = "invalid_credentials"
        db.add(attempt)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        attempt.failure_reason = "account_inactive"
        db.add(attempt)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Create tokens - JWT 'sub' (subject) must be a string
    token_data = {"sub": str(user.id), "email": user.email}
    expires_delta = timedelta(days=30) if login_data.remember_me else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(token_data, expires_delta)
    refresh_token_str = create_refresh_token(token_data)
    
    # Store refresh token
    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.utcnow() + timedelta(days=30),
    )
    db.add(refresh_token)
    
    # Mark attempt as successful
    attempt.success = True
    db.add(attempt)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        "expires_in": int(expires_delta.total_seconds()),
    }


@router.post("/auth/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    payload = verify_token(refresh_data.refresh_token, "refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if token exists and is not revoked
    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_data.refresh_token,
        RefreshToken.revoked == False
    ).first()
    
    if not token_record or token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or revoked"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token - JWT 'sub' (subject) must be a string
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_data.refresh_token,  # Keep same refresh token
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/auth/register", response_model=UserResponse)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if email exists
    if db.query(User).filter(User.email == register_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if db.query(User).filter(User.username == register_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Truncate password to 70 bytes BEFORE hashing (bcrypt limit is 72, use 70 for safety)
    password = register_data.password
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 70:
        # Truncate to 70 bytes
        truncated = password_bytes[:70]
        # Remove incomplete UTF-8 sequences
        while truncated and (truncated[-1] & 0xC0) == 0x80:
            truncated = truncated[:-1]
        try:
            password = truncated.decode('utf-8')
        except UnicodeDecodeError:
            # If decode fails, use ASCII fallback
            password = truncated.decode('ascii', errors='ignore') or password[:50]
    
    # Create user
    user = User(
        email=register_data.email,
        username=register_data.username,
        hashed_password=get_password_hash(password),
        full_name=register_data.full_name,
        is_active=True,  # Auto-activate for now, can be changed to require email verification
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Assign default "editor" role
    default_role = db.query(Role).filter(Role.role_name == "editor").first()
    if default_role:
        user_role = UserRole(user_id=user.id, role_id=default_role.id)
        db.add(user_role)
        db.commit()
    
    roles = get_user_roles(db, user.id)
    permissions = get_user_permissions(db, user.id)
    
    return UserResponse(
        **{col.name: getattr(user, col.name) for col in user.__table__.columns},
        roles=roles,
        permissions=permissions,
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    roles = get_user_roles(db, current_user.id)
    permissions = get_user_permissions(db, current_user.id)
    
    return UserResponse(
        **{col.name: getattr(current_user, col.name) for col in current_user.__table__.columns},
        roles=roles,
        permissions=permissions,
    )


@router.post("/auth/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Truncate password to 70 bytes BEFORE hashing (bcrypt limit is 72, use 70 for safety)
    new_password = password_data.new_password
    new_password_bytes = new_password.encode('utf-8')
    if len(new_password_bytes) > 70:
        truncated = new_password_bytes[:70]
        while truncated and (truncated[-1] & 0xC0) == 0x80:
            truncated = truncated[:-1]
        try:
            new_password = truncated.decode('utf-8')
        except UnicodeDecodeError:
            new_password = truncated.decode('ascii', errors='ignore') or new_password[:50]
    
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


# Role and Permission Management (Admin only)
@router.post("/auth/roles", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Create a new role"""
    if db.query(Role).filter(Role.role_name == role_data.role_name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )
    
    role = Role(
        role_name=role_data.role_name,
        display_name=role_data.display_name,
        description=role_data.description,
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    
    # Assign permissions
    for perm_name in role_data.permission_names:
        permission = db.query(Permission).filter(Permission.permission_name == perm_name).first()
        if permission:
            role_perm = RolePermission(role_id=role.id, permission_id=permission.id)
            db.add(role_perm)
    
    db.commit()
    
    permissions = [rp.permission.permission_name for rp in role.permissions if rp.permission]
    return RoleResponse(
        **{col.name: getattr(role, col.name) for col in role.__table__.columns},
        permissions=permissions,
    )


@router.get("/auth/roles", response_model=List[RoleResponse])
async def list_roles(
    db: Session = Depends(get_db)
):
    """List all roles"""
    roles = db.query(Role).all()
    result = []
    for role in roles:
        permissions = [rp.permission.permission_name for rp in role.permissions if rp.permission]
        result.append(RoleResponse(
            **{col.name: getattr(role, col.name) for col in role.__table__.columns},
            permissions=permissions,
        ))
    return result


@router.post("/auth/assign-role")
async def assign_role(
    assign_data: AssignRoleRequest,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Assign roles to a user"""
    user = db.query(User).filter(User.id == assign_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove existing roles
    db.query(UserRole).filter(UserRole.user_id == assign_data.user_id).delete()
    
    # Assign new roles
    for role_name in assign_data.role_names:
        role = db.query(Role).filter(Role.role_name == role_name).first()
        if role:
            user_role = UserRole(user_id=user.id, role_id=role.id, assigned_by=current_user.id)
            db.add(user_role)
    
    db.commit()
    return {"message": "Roles assigned successfully"}

