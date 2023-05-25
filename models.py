from database import Base
from sqlalchemy import String,Integer,Float, Column


class Inventory(Base):
    __tablename__='inventory'
    id=Column(Integer,primary_key=True)
    product_name=Column(String(80))
    variant=Column(String(80), nullable=True)
    sku=Column(String(80))
    price=Column(Float)
    qty=Column(Integer)
    description=Column(String(200))

    def __init__(self,id,product_name,variant,sku,price,qty,description):
        self.id=id
        self.product_name=product_name
        self.variant=variant
        self.sku=sku
        self.price=price
        self.qty=qty
        self.description=description



    def __repr__(self):
        return f"<name={self.product_name} price={self.price}>"
