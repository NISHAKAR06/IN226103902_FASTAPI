from fastapi import FastAPI,Query,HTTPException
from typing import List

app=FastAPI()

products=[
{"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics"},
{"id":2,"name":"Notebook","price":99,"category":"Stationery"},
{"id":3,"name":"USB Hub","price":799,"category":"Electronics"},
{"id":4,"name":"Pen Set","price":49,"category":"Stationery"}
]

orders=[]
order_id_counter=1


@app.get("/products/search")
def search_products(keyword:str):
 result=[p for p in products if keyword.lower() in p["name"].lower()]
 if not result:
  return{"message":f"No products found for: {keyword}"}
 return{"keyword":keyword,"total_found":len(result),"products":result}


@app.get("/products/sort")
def sort_products(sort_by:str="price",order:str="asc"):

 if sort_by not in ["price","name"]:
  return{"error":"sort_by must be 'price' or 'name'"}

 reverse=True if order=="desc" else False

 sorted_products=sorted(products,key=lambda p:p[sort_by],reverse=reverse)

 return{
 "sort_by":sort_by,
 "order":order,
 "products":sorted_products
 }


@app.get("/products/page")
def paginate_products(page:int=1,limit:int=2):

 start=(page-1)*limit
 end=start+limit

 total=len(products)
 total_pages=(total+limit-1)//limit

 return{
 "page":page,
 "limit":limit,
 "total_pages":total_pages,
 "products":products[start:end]
 }


@app.post("/orders")
def create_order(customer_name:str,product_id:int):

 global order_id_counter

 product=next((p for p in products if p["id"]==product_id),None)

 if not product:
  raise HTTPException(status_code=404,detail="Product not found")

 order={
 "order_id":order_id_counter,
 "customer_name":customer_name,
 "product":product["name"],
 "price":product["price"]
 }

 orders.append(order)
 order_id_counter+=1

 return{"message":"Order placed","order":order}


@app.get("/orders/search")
def search_orders(customer_name:str):

 result=[o for o in orders if customer_name.lower() in o["customer_name"].lower()]

 if not result:
  return{"message":f"No orders found for: {customer_name}"}

 return{
 "customer_name":customer_name,
 "total_found":len(result),
 "orders":result
 }


@app.get("/products/sort-by-category")
def sort_by_category():

 sorted_products=sorted(products,key=lambda p:(p["category"],p["price"]))

 return{"products":sorted_products}


@app.get("/products/browse")
def browse_products(
 keyword:str=None,
 sort_by:str="price",
 order:str="asc",
 page:int=1,
 limit:int=4
):

 result=products

 if keyword:
  result=[p for p in result if keyword.lower() in p["name"].lower()]

 reverse=True if order=="desc" else False
 result=sorted(result,key=lambda p:p[sort_by],reverse=reverse)

 total=len(result)
 total_pages=(total+limit-1)//limit

 start=(page-1)*limit
 end=start+limit

 return{
 "keyword":keyword,
 "sort_by":sort_by,
 "order":order,
 "page":page,
 "limit":limit,
 "total_found":total,
 "total_pages":total_pages,
 "products":result[start:end]
 }


@app.get("/orders/page")
def paginate_orders(page:int=1,limit:int=3):

 start=(page-1)*limit
 end=start+limit

 total=len(orders)
 total_pages=(total+limit-1)//limit

 return{
 "page":page,
 "limit":limit,
 "total_pages":total_pages,
 "orders":orders[start:end]
 }


@app.get("/products/{product_id}")
def get_product(product_id:int):

 for p in products:
  if p["id"]==product_id:
   return p

 raise HTTPException(status_code=404,detail="Product not found")