"""
Authentication and Authorization Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Auth Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    roles: List[str] = []
    permissions: List[str] = []
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# Role Schemas
class RoleCreate(BaseModel):
    role_name: str
    display_name: str
    description: Optional[str] = None
    permission_names: List[str] = []


class RoleResponse(BaseModel):
    id: int
    role_name: str
    display_name: str
    description: Optional[str] = None
    is_system: bool
    permissions: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


# Permission Schemas
class PermissionResponse(BaseModel):
    id: int
    permission_name: str
    display_name: str
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# User Role Assignment
class AssignRoleRequest(BaseModel):
    user_id: int
    role_names: List[str]


class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None

