from sqlalchemy import Table, Column, Integer, String, Float
from database import metadata

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), index=True),
    Column("description", String(1000)),
    Column("price", Float),
)
