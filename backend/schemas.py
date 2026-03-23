from pydantic import BaseModel
from typing import List


class RestaurantBase(BaseModel):
    name: str
    cuisine: str


class RestaurantResponse(RestaurantBase):
    id: int

    class Config:
        from_attributes = True


class MenuItemBase(BaseModel):
    name: str
    price: float
    restaurant_id: int


class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str

    class Config:
        from_attributes = True