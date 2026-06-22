from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
