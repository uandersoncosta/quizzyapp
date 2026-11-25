from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
  full_name: str = Field(min_length=2, max_length=150)
  email: EmailStr
  password: str = Field(min_length=8, max_length=128)
  confirmed_password: str = Field(min_length=8, max_length=128)

class SignInRequest(BaseModel):
  email: EmailStr
  password: str

class UserResponse(BaseModel):
  id: str
  email: EmailStr
  full_name: str
  
  class Config:
        from_attributes = True

class TokenResponse(BaseModel):
  access_token: str
  token_type:str = 'bearer'