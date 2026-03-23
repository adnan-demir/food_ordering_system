from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    orders = relationship("Order", back_populates="user")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cuisine = Column(String(100), nullable=False)

    menu_items = relationship("MenuItem", back_populates="restaurant")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    restaurant = relationship("Restaurant", back_populates="menu_items")
    menu_item_categories = relationship("MenuItemCategory", back_populates="menu_item")

    


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="pending")

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    menu_item_categories = relationship("MenuItemCategory", back_populates="category")

    


class MenuItemCategory(Base):
    __tablename__ = "menu_item_categories"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    menu_item = relationship("MenuItem", back_populates="menu_item_categories")
    category = relationship("Category", back_populates="menu_item_categories")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer)

    cart = relationship("Cart", back_populates="cart_items")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_line = Column(String(200))

    user = relationship("User")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    status = Column(String(50))

    order = relationship("Order")