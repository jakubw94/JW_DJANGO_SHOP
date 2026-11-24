from .models import Product, DeliveryCost
from types import SimpleNamespace
import os
from django.conf import settings
import copy

### Session cart structure: {"12": {"c": "p", "q": 2}, "2": ...} - product_id as key ###

class Cart:

    ### Adding product to cart --> return new cart ###
    @staticmethod
    def add_item(session_cart: dict, product_id: str | int, category: str) -> dict | None:
        if category == "products":
            stock = Product.objects.filter(id=product_id).values_list('stock', flat=True).first()
            if stock == 0 or (product_id in session_cart and stock <= session_cart[product_id]["q"]):
                return None
        if product_id in session_cart:
            session_cart[product_id]["q"] += 1
        else:
            session_cart[product_id] = {"c": category[0], "q": 1}
        return session_cart

    ### Counting items in cart --> return number of items ####
    @staticmethod
    def count_items(session_cart: dict | None) -> int:
        if session_cart:
            items = sum(v["q"] if v["c"] != "t" else 1 for v in session_cart.values())
        else:
            items = 0
        return items

    ### Removing item from cart --> return new cart ###
    @staticmethod
    def remove_item(session_cart: dict, product_id: str | int) -> dict:
        new_cart = {k: v for k, v in session_cart.items() if k != product_id}
        return new_cart

    ### Changing quantity of item in cart --> return new cart ###
    @staticmethod
    def change_quantity(session_cart: dict, product_id: str | int, operation: str) -> dict | None:
        if session_cart[product_id]["c"] == "p":
            stock = Product.objects.filter(id=product_id).values_list('stock', flat=True).first()
            if operation == "+" and stock <= session_cart[product_id]["q"]:
                return None
        session_cart[product_id]["q"] += 1 if operation == "+" else -1
        if session_cart[product_id]["q"] == 0:
            session_cart.pop(product_id)
        return session_cart

    ### Creating cart structure to pass to cart and checkout views --> return tuple ###
    @staticmethod
    def create_cart_structure(request) -> tuple:
        # Getting cart from session #
        session_cart = copy.deepcopy(request.session.get("cart", {}))
        # Returning None if no cart or empty cart #
        if not session_cart:
            return (None, 0, None)
        # Getting id's from cart #
        id_list = [id for id in session_cart]
        # Getting db products based on cart id's and removing inactive/deleted products #
        db_products = Product.objects.filter(id__in=id_list, available=True)
        db_products = [p for p in db_products if not (p.category == "products" and p.stock <= 0)]
        id_to_remove = [id for id in id_list if id not in [str(p.id) for p in db_products]]
        for id in id_to_remove:
            session_cart.pop(id)
        # Quantity check and adding quantity paremeter #
        for p in db_products:
            if p.category == "products":
                if session_cart[str(p.id)]["q"] > p.stock:
                    session_cart[str(p.id)]["q"] = p.stock
            p.quantity = session_cart[str(p.id)]["q"]
        # Saving modified session cart if deleted items #
        if request.session["cart"] != session_cart:
            request.session["cart"] = session_cart
            request.session.modified = True
            modified = True
        else:
            modified = False
        # Getting delivery cost #
        delivery_cost = DeliveryCost.objects.filter(id=1).values_list('total', flat=True).first()
        # Creating return structure #
        db_products.sort(key=lambda p: p.id)
        products = [p for p in db_products if p.category == "products"]
        services = [p for p in db_products if p.category == "services"]
        time_services = [p for p in db_products if p.category == "time_services"]
        # Adding delivery position to products
        if products:
            delivery_obj = SimpleNamespace(id=None, name='Delivery', price=delivery_cost, quantity=1)
            products.append(delivery_obj)
        # Calculating total money #
        for p in products + services + time_services:
            p.total = round(p.price * p.quantity, 2)
        total = round(sum(p.price * p.quantity for p in products + services + time_services), 2)
        # Returning new structure
        cart = {"products": products, "services": services, "time_services": time_services}
        # cart - cart structure, total - total amount of money, modified - True/False
        return (cart, total, modified)