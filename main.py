# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User, Product
from authentication import authenticate_user, create_access_token, get_current_user, oauth2_scheme

app = FastAPI()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = next(get_db())
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    hashed_password = get_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.get("/products")
async def get_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": product.id, "name": product.name, "category": product.category, "sku": product.sku, "quantity_in_stock": product.quantity_in_stock, "price": product.price} for product in products]

@app.post("/products")
async def create_product(name: str, category: str, sku: str, quantity_in_stock: int, price: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.sku == sku).first()
    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists",
        )
    new_product = Product(name=name, category=category, sku=sku, quantity_in_stock=quantity_in_stock, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created successfully"}

@app.get("/summary")
async def get_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    low_stock_alerts = db.query(Product).filter(Product.quantity_in_stock < 10).count()
    total_inventory_value = db.query(Product).with_entities(db.func.sum(Product.price * Product.quantity_in_stock)).scalar()
    return {"total_products": total_products, "low_stock_alerts": low_stock_alerts, "total_inventory_value": total_inventory_value}