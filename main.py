from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models


app=FastAPI()

#creating the columns of the database
class Inventory(BaseModel):
    id:int
    product_name:str
    variant:str
    sku:str
    price:float
    qty:int
    description:str

    class Config:
        orm_mode=True


db=SessionLocal()

# get everything from the database
@app.get('/inventory',response_model=List[Inventory],status_code=200)
def get_all_products():
    pens=db.query(models.Inventory).all()

    return pens


# get a single product from the database based on the given id
@app.get('/inventory/{product_id}',response_model=Inventory,status_code=status.HTTP_200_OK)
def get_a_product(product_id:int):
    product=db.query(models.Inventory).filter(models.Inventory.id==product_id).first()

    return product


# global search for a product based on the given keyword
@app.get('/inventory/search/{keyword}')
def search_products(keyword:str):
    result = []
    # allow there to be random string before and after the keyword
    tag = "%{}%".format(keyword)
    # search the keyword in all product names
    target=db.query(models.Inventory).filter(models.Inventory.product_name.like(tag)).all()
    result.append(target)
    # search the keyword in all variant
    target1=db.query(models.Inventory).filter(models.Inventory.variant.like(tag)).all()
    result.append(target1)
    # search the keyword in all sku
    target2 = db.query(models.Inventory).filter(models.Inventory.sku.like(tag)).all()
    result.append(target2)
    # search the keyword in all descriptions
    target3 = db.query(models.Inventory).filter(models.Inventory.description.like(tag)).all()
    result.append(target3)

    return result

# allow the user to buy a product
@app.get('/inventory/buy/{product_id}/{quantity}')
def buy_products(product_id:int,quantity:int):
    # get the product based on given id
    target = db.query(models.Inventory).filter(models.Inventory.id==product_id).first()

    # calculate the cost based on the price of the target product and the quantity
    total_cost=(target.price)*quantity

    if quantity > target.qty: # if the input quantity is larger than the supply
        return {"message":"Insufficient Supply!"}

    target.qty-=quantity

    return {"message":"Your total is: "+str(total_cost)}


# create a new product
@app.post('/inventory',response_model=Inventory,status_code=status.HTTP_201_CREATED)
def new_product(product:Inventory):
    new_product=models.Inventory(
        id=product.id,
        product_name=product.product_name,
        variant=product.variant,
        sku=product.sku,
        price=product.price,
        qty=product.qty,
        description=product.description
    )

    db.add(new_product)
    db.commit()

    return new_product


# decrement the quantity of a product
@app.post('/inventory/remove/{product_id}/{quantity}')
def remove_products(product_id:int,quantity:int):
    target = db.query(models.Inventory).filter(models.Inventory.id==product_id).first()

    # if the given quantity is larger than the supply, clear all the supplies
    if quantity > target.qty:
        target.qty=0
        return target

    target.qty-= quantity

    return target


# increment the quantity of a product
@app.post('/inventory/add/{product_id}/{quantity}')
def add_products(product_id:int,quantity:int):
    target = db.query(models.Inventory).filter(models.Inventory.id==product_id).first()

    target.qty += quantity

    return target


# update the info of a product
@app.put('/inventory/{product_id}',response_model=Inventory,status_code=status.HTTP_200_OK)
def update_product(product_id:int,product:Inventory):
    target=db.query(models.Inventory).filter(models.Inventory.id==product_id).first()
    target.product_name=product.product_name
    target.variant=product.variant
    target.sku=product.sku
    target.price=product.price
    target.qty=product.qty
    target.description=product.description

    db.commit()

    return target


# delete a product from the inventory
@app.delete('/inventory/{product_id}')
def delete_product(product_id:int):
    target=db.query(models.Inventory).filter(models.Inventory.id==product_id).first()

    # if the given id does not exist
    if target is None:
        return {"message":"PRODUCT NOT FOUND"}

    db.delete(target)
    db.commit()
    return target