from pydantic import BaseModel, EmailStr

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
