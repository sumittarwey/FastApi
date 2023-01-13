from typing import List, Optional

from pydantic import BaseModel,EmailStr


class ItemBase(BaseModel):
    name: str
    price : float
    description: Optional[str] = None
    store_id: int

    class Config:
        schema_extra = {
            "create_item": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class StoreBase(BaseModel):
    name: str

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    fullname: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    username: EmailStr 
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "joe@xyz.com",
                "password": "any"
            }
        }