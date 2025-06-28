# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database, engine, metadata
from models import products

app = FastAPI()

# Create tables
metadata.create_all(engine)

# Pydantic model
class Product(BaseModel):
    name: str
    description: str | None = None
    price: float

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
