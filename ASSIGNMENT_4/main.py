from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

products=[
{"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics","in_stock":True},
{"id":2,"name":"Notebook","price":99,"category":"Stationery","in_stock":True},
{"id":3,"name":"USB Hub","price":799,"category":"Electronics","in_stock":False},
{"id":4,"name":"Pen Set","price":49,"category":"Stationery","in_stock":True}
]

cart=[]
orders=[]
order_id_counter=1

class CheckoutRequest(BaseModel):
 customer_name:str
 delivery_address:str


@app.post("/cart/add")
def add_to_cart(product_id:int,quantity:int=1):
 product=next((p for p in products if p["id"]==product_id),None)

 if not product:
  raise HTTPException(status_code=404,detail="Product not found")

 if not product["in_stock"]:
  raise HTTPException(status_code=400,detail=f"{product['name']} is out of stock")

 existing=next((c for c in cart if c["product_id"]==product_id),None)

 if existing:
  existing["quantity"]+=quantity
  existing["subtotal"]=existing["quantity"]*existing["unit_price"]
  return{"message":"Cart updated","cart_item":existing}

 item={
 "product_id":product["id"],
 "product_name":product["name"],
 "quantity":quantity,
 "unit_price":product["price"],
 "subtotal":product["price"]*quantity
 }

 cart.append(item)

 return{"message":"Added to cart","cart_item":item}


@app.get("/cart")
def view_cart():

 if not cart:
  return{"message":"Cart is empty"}

 grand_total=sum(item["subtotal"] for item in cart)

 return{
 "items":cart,
 "item_count":len(cart),
 "grand_total":grand_total
 }


@app.delete("/cart/{product_id}")
def remove_item(product_id:int):

 for i,item in enumerate(cart):
  if item["product_id"]==product_id:
   removed=cart.pop(i)
   return{"message":f"{removed['product_name']} removed from cart"}

 raise HTTPException(status_code=404,detail="Item not found in cart")


@app.post("/cart/checkout")
def checkout(data:CheckoutRequest):

 global order_id_counter

 if not cart:
  raise HTTPException(status_code=400,detail="CART_EMPTY")

 placed=[]
 grand_total=0

 for item in cart:

  order={
  "order_id":order_id_counter,
  "customer_name":data.customer_name,
  "product":item["product_name"],
  "quantity":item["quantity"],
  "total_price":item["subtotal"],
  "delivery_address":data.delivery_address
  }

  orders.append(order)
  placed.append(order)

  grand_total+=item["subtotal"]
  order_id_counter+=1

 cart.clear()

 return{
 "message":"Checkout successful",
 "orders_placed":placed,
 "grand_total":grand_total
 }


@app.get("/orders")
def get_orders():

 return{
 "orders":orders,
 "total_orders":len(orders)
 }