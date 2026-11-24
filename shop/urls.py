from django.urls import path
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.shop, name="shop"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact/", views.contact, name="contact"),
    path("contact/send_message/", views.send_contact_message, name="send_contact_message"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", views.remove_product, name="remove_from_cart"),
    path("change_cart_quantity/", views.change_cart_quantity, name="update_cart_quantity"),
    path("make_order/", views.make_order, name="make_order"),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions")
]

