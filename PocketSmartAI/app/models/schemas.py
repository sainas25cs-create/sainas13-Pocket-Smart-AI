from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class InteriorPlanRequest(BaseModel):
    room_type: str = Field(min_length=2, max_length=100)
    budget: float = Field(gt=0)
    style: str = Field(min_length=2, max_length=100)
    room_size: str = Field(min_length=2, max_length=100)
    requirements: str = Field(default="", max_length=1000)


class PartyPlanRequest(BaseModel):
    occasion: str = Field(min_length=2, max_length=100)
    guests: int = Field(gt=0, le=10000)
    budget: float = Field(gt=0)
    location: str = Field(min_length=2, max_length=200)
    food_preference: str = Field(default="", max_length=200)
    requirements: str = Field(default="", max_length=1000)


class JewelryPlanRequest(BaseModel):
    occasion: str = Field(min_length=2, max_length=100)
    budget: float = Field(gt=0)
    jewelry_type: str = Field(min_length=2, max_length=100)
    outfit_color: str = Field(min_length=2, max_length=100)
    outfit_style: str = Field(default="", max_length=100)
    requirements: str = Field(default="", max_length=1000)