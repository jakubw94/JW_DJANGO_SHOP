from shop.cart import Cart

### Adding cart count ###
def cart_count(request):
    return {
        "cart_count": Cart.count_items(request.session.get("cart"))
    }