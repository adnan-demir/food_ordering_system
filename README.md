# Food Ordering System

## Project Overview

This project is a full-stack food ordering system developed using FastAPI (backend) and React (frontend).
Users can browse restaurants, view menus, add items to a cart, and place orders with a simulated payment system.

---

## Features

* View restaurants and menus
* Add items to cart
* Place orders
* Payment simulation
* Multi-restaurant ordering
* RESTful API with FastAPI
* Frontend built with React and Vite

---

## Technologies Used

### Backend

* FastAPI
* SQLAlchemy
* Pydantic

### Frontend

* React (Vite)

### Database

* MySQL (migrated from SQLite)

---

## Database Design

The system includes more than 10 entities:

* User
* Restaurant
* MenuItem
* Category
* MenuItemCategory (Many-to-Many)
* Order
* OrderItem
* Cart
* CartItem
* Payment
* Address

---

## Relationships

### One-to-Many

* User → Orders
* Restaurant → MenuItems

### Many-to-Many

* MenuItem ↔ Category

---

## Installation and Setup

### 1. Clone the repository

git clone https://github.com/adnan-demir/food-ordering-system.git
cd food_ordering_system

---

### 2. Backend Setup

cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

Backend runs on:
http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

---

### 3. Frontend Setup

cd frontend
npm install
npm run dev

Frontend runs on:
http://localhost:5173

---

### 4. Database Setup (MySQL)

Create database:
CREATE DATABASE food_ordering_mysql;

Update connection string in database.py:
mysql+pymysql://root:your_password@localhost:3306/food_ordering_mysql

---

## System Diagrams

* Use Case Diagram
* Class Diagram
* Activity Diagram

---

## Authors

* Adnan Demir – 220911784
* Emre Becerir – 220911807

---

## Notes

This project was developed as part of a course assignment and demonstrates full-stack development and relational database design.
