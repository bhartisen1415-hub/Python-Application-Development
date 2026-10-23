from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    price: float = Field(ge=0)


class ItemUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    price: float = Field(ge=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
