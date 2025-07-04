from fastapi import FastAPI, HTTPException
from database import database, engine, metadata
from models import products, users
from schemas import Product, UserCreate, UserOut, CartItemCreate, CartItemOut
from sqlalchemy import select
from passlib.context import CryptContext
from models import cart

app = FastAPI()
metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.post("/products/")
async def create_product(product: Product):
    query = products.insert().values(
        name=product.name, description=product.description, price=product.price
    )
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}

@app.get("/products/{product_id}")
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    # Check if user already exists
    query = users.select().where(users.c.email == user.email)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    query = users.insert().values(email=user.email, hashed_password=hashed_password)
    user_id = await database.execute(query)
    return {"id": user_id, "email": user.email}






@app.post("/cart/", response_model=CartItemOut)
async def add_to_cart(item: CartItemCreate):
    # Check if product exists
    product_query = products.select().where(products.c.id == item.product_id)
    product = await database.fetch_one(product_query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Insert into cart
    query = cart.insert().values(product_id=item.product_id, quantity=item.quantity)
    cart_id = await database.execute(query)
    return {**item.dict(), "id": cart_id}

@app.get("/cart/", response_model=list[CartItemOut])
async def view_cart():
    query = cart.select()
    return await database.fetch_all(query)


