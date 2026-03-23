from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Ordering System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_data():
    db = SessionLocal()

    if db.query(models.Restaurant).count() == 0:
        restaurant1 = models.Restaurant(name="Pizza Palace", cuisine="Italian")
        restaurant2 = models.Restaurant(name="Burger House", cuisine="American")

        db.add_all([restaurant1, restaurant2])
        db.commit()

        db.refresh(restaurant1)
        db.refresh(restaurant2)

        menu_items = [
            models.MenuItem(name="Margherita Pizza", price=12.5, restaurant_id=restaurant1.id),
            models.MenuItem(name="Pepperoni Pizza", price=14.0, restaurant_id=restaurant1.id),
            models.MenuItem(name="Cheeseburger", price=10.0, restaurant_id=restaurant2.id),
            models.MenuItem(name="Fries", price=4.5, restaurant_id=restaurant2.id),
        ]
        db.add_all(menu_items)

    if db.query(models.User).count() == 0:
        user = models.User(name="Test User", email="test@example.com")
        db.add(user)

    db.commit()
    db.close()


@app.get("/")
def root():
    return {"message": "Food Ordering System API is running"}


@app.get("/restaurants", response_model=list[schemas.RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()


@app.get("/restaurants/{restaurant_id}/menu", response_model=list[schemas.MenuItemResponse])
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()


@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_price = 0

    for item in order.items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
        total_price += menu_item.price * item.quantity

    new_order = models.Order(
        user_id=order.user_id,
        total_price=total_price,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        order_item = models.OrderItem(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return new_order