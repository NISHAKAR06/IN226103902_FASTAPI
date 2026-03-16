from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

products=[
{"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics","in_stock":True},
{"id":2,"name":"Notebook","price":99,"category":"Stationery","in_stock":True},
{"id":3,"name":"USB Hub","price":799,"category":"Electronics","in_stock":False},
{"id":4,"name":"Pen Set","price":49,"category":"Stationery","in_stock":True}
]

class Product(BaseModel):
 name:str
 price:int
 category:str
 in_stock:bool

@app.post("/products",status_code=201)
def add_product(data:Product):
 for p in products:
  if p["name"].lower()==data.name.lower():
   raise HTTPException(status_code=400,detail="Product with this name already exists")
 new_id=max(p["id"] for p in products)+1
 product={"id":new_id,**data.dict()}
 products.append(product)
 return{"message":"Product added","product":product}

@app.get("/products")
def get_products():
 return{"products":products,"total":len(products)}

@app.get("/products/audit")
def products_audit():
 in_stock=[p for p in products if p["in_stock"]]
 out_stock=[p["name"] for p in products if not p["in_stock"]]
 most_exp=max(products,key=lambda p:p["price"])
 total_value=sum(p["price"]*10 for p in in_stock)
 return{
 "total_products":len(products),
 "in_stock_count":len(in_stock),
 "out_of_stock_names":out_stock,
 "total_stock_value":total_value,
 "most_expensive":{"name":most_exp["name"],"price":most_exp["price"]}
 }

@app.put("/products/discount")
def discount_products(category:str,discount_percent:int=Query(...,ge=1,le=99)):
 updated=[]
 for p in products:
  if p["category"].lower()==category.lower():
   p["price"]=int(p["price"]*(1-discount_percent/100))
   updated.append({"name":p["name"],"new_price":p["price"]})
 if not updated:
  return{"message":"No products found in this category"}
 return{"updated_count":len(updated),"products":updated}

@app.get("/products/{product_id}")
def get_product(product_id:int):
 for p in products:
  if p["id"]==product_id:
   return p
 raise HTTPException(status_code=404,detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id:int,price:Optional[int]=None,in_stock:Optional[bool]=None):
 for p in products:
  if p["id"]==product_id:
   if price is not None:
    p["price"]=price
   if in_stock is not None:
    p["in_stock"]=in_stock
   return{"message":"Product updated","product":p}
 raise HTTPException(status_code=404,detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id:int):
 for i,p in enumerate(products):
  if p["id"]==product_id:
   name=p["name"]
   products.pop(i)
   return{"message":f"Product '{name}' deleted"}
 raise HTTPException(status_code=404,detail="Product not found")