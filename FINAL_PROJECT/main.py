from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ---------------- DATA ----------------
menu = [
    {"id": 1, "name": "Pizza", "price": 299, "category": "Food", "available": True},
    {"id": 2, "name": "Burger", "price": 199, "category": "Food", "available": True},
    {"id": 3, "name": "Pasta", "price": 249, "category": "Food", "available": False},
    {"id": 4, "name": "Fries", "price": 99, "category": "Snacks", "available": True}
]

cart = []
orders = []
order_counter = 1


# ---------------- DAY 1 ----------------
@app.get("/")
def home():
    return {"message": "Food Delivery API Running"}

@app.get("/menu")
def get_menu():
    return {"menu": menu, "total": len(menu)}

@app.get("/menu/summary")
def menu_summary():
    available = len([i for i in menu if i["available"]])
    return {
        "total_items": len(menu),
        "available_items": available
    }


# ---------------- HELPERS (DAY 3) ----------------
def find_item(item_id: int):
    return next((i for i in menu if i["id"] == item_id), None)

def calculate_total(price: int, quantity: int):
    return price * quantity

def filter_logic(keyword: Optional[str] = None):
    result = menu
    if keyword is not None:
        result = [i for i in result if keyword.lower() in i["name"].lower()]
    return result


# ---------------- DAY 2 (PYDANTIC) ----------------
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=10)


# ---------------- DAY 4 (CRUD) ----------------
@app.post("/menu", status_code=201)
def add_item(name: str, price: int, category: str):
    if any(i["name"].lower() == name.lower() for i in menu):
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_item = {
        "id": len(menu) + 1,
        "name": name,
        "price": price,
        "category": category,
        "available": True
    }
    menu.append(new_item)
    return new_item


@app.put("/menu/{item_id}")
def update_item(item_id: int, name: Optional[str] = None, price: Optional[int] = None):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if name is not None:
        item["name"] = name
    if price is not None:
        item["price"] = price

    return item


@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item["available"]:
        raise HTTPException(status_code=400, detail="Cannot delete available item")

    menu.remove(item)
    return {"message": "Item deleted"}


# ---------------- DAY 5 (WORKFLOW) ---------
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not item["available"]:
        raise HTTPException(status_code=400, detail="Item not available")

    existing = next((c for c in cart if c["item_id"] == item_id), None)

    if existing:
        existing["quantity"] += quantity
        existing["total"] = calculate_total(item["price"], existing["quantity"])
        return {"message": "Cart updated", "cart_item": existing}

    new_cart = {
        "item_id": item_id,
        "name": item["name"],
        "quantity": quantity,
        "total": calculate_total(item["price"], quantity)
    }
    cart.append(new_cart)
    return {"message": "Added to cart", "cart_item": new_cart}


@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}
    total = sum(i["total"] for i in cart)
    return {"items": cart, "grand_total": total}


@app.post("/cart/checkout")
def checkout(customer_name: str):
    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    placed_orders = []

    for item in cart:
        order = {
            "order_id": order_counter,
            "customer_name": customer_name,
            "item": item["name"],
            "quantity": item["quantity"],
            "total": item["total"]
        }
        orders.append(order)
        placed_orders.append(order)
        order_counter += 1

    cart.clear()

    return {
        "message": "Order placed",
        "orders": placed_orders
    }


@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# ---------------- DAY 6 ----------------
@app.get("/menu/search")
def search_products(keyword: str):
    result = filter_logic(keyword)
    if not result:
        return {"message": f"No items found for {keyword}"}
    return {"results": result}


@app.get("/menu/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be price or name"}

    reverse = True if order == "desc" else False
    sorted_data = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

    return {"products": sorted_data}


@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit

    total = len(menu)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "items": menu[start:end]
    }


@app.get("/menu/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):
    result = filter_logic(keyword)

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    total = len(result)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": total,
        "total_pages": total_pages,
        "items": result[start:end]
    }


# ---------------- KEEP LAST ----------------
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item