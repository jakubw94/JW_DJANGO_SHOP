from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from .models import Product, ProductImage, OrderItem
from .cart import Cart
from .forms import ContactForm, MakeOrderForm
from .email_class import Email
from django.contrib import messages
from django.db import transaction
from .captcha import Captcha
from django_shop.settings import EMAIL_SETTING
from utils import preview_email_message


# GET - Home page #
@require_GET
def home(request):
    return render(request, "shop/home.html")


# GET - Products list page #
@require_GET
def shop(request):
    products = Product.objects.filter(available=True).order_by("id")
    context = {"products": products}
    return render(request, "shop/shop.html", context)


# GET - Product detail page #
@require_GET
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, "shop/product.html", context)


# GET - Cart page #
@require_GET
def cart(request):
    cart, total, modified = Cart.create_cart_structure(request)
    if modified:
        messages.error(request, "Some items were removed or adjusted due to availability")
    context = {"cart": cart, "total": total}
    return render(request, "shop/cart.html", context)


# POST - Add to cart #
@require_POST
def add_to_cart(request):
    session_cart = request.session.get("cart", {})
    product_id = request.POST["product_id"]
    category = request.POST["category"]
    new_cart = Cart.add_item(session_cart, product_id, category)
    if new_cart:
        messages.success(request, "Item added to cart")
        request.session["cart"] = new_cart
        request.session.modified = True
    elif new_cart is None:
        messages.error(request, "Not enough items in stock")
    return redirect("shop")


# POST - Remove from cart #
@require_POST
def remove_product(request):
    cart = request.session.get("cart", {})
    product_id = request.POST["product_id"]
    new_cart = Cart.remove_item(cart, product_id)
    request.session["cart"] = new_cart
    request.session.modified = True
    messages.success(request, "Item removed from cart")
    return redirect("cart")


# POST - Change cart quantity #
@require_POST
def change_cart_quantity(request):
    cart = request.session.get("cart", {})
    product_id = request.POST["product_id"][:-1]
    operation = request.POST["product_id"][-1]
    new_cart = Cart.change_quantity(cart, product_id, operation)
    if new_cart is not None:
        messages.success(request, "Changed cart quantity")
        request.session["cart"] = new_cart
        request.session.modified = True
    elif new_cart is None:
        messages.error(request, "Not enough items in stock")
    return redirect("cart")


# GET - Checkout page #
@require_GET
def checkout(request):
    if request.user.is_superuser:
        messages.error(request, "You can't proceed orders with admin account")
        return redirect("home")
    elif request.user.is_authenticated:
        auto_fill_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address_1': request.user.userinfo.address_1,
            'address_2': request.user.userinfo.address_2,
            'zip_code': request.user.userinfo.zip_code,
            'city': request.user.userinfo.city,
            'phone': request.user.userinfo.phone}
    else:
        auto_fill_data = {}
    form = MakeOrderForm(initial=auto_fill_data)
    cart, total, modified = Cart.create_cart_structure(request)
    if not total:
        return redirect("cart")
    if modified:
        messages.error(request, "Some items were removed or adjusted due to availability")
    captcha, answer = Captcha.generate_captcha()
    context = {"form": form, "cart": cart, "total": total, "captcha": captcha, "answer": answer}
    return render(request, "shop/checkout.html", context)


# POST - Make order #
@require_POST
def make_order(request):
    session_cart = request.session.get('cart', {})
    cart, total, modified = Cart.create_cart_structure(request)
    form_data = request.POST.copy()
    if request.user.is_authenticated:
        form_data["email"] = request.user.username
    form = MakeOrderForm(form_data)
    if modified:
        messages.error(request, "Some items were removed or adjusted due to availability")
    else:
        if form.is_valid():
            if request.POST["captcha_input"] == request.POST["captcha_answer"]:
                try:
                    with transaction.atomic():
                        order = form.save(commit=False)
                        order.user = request.user if request.user.is_authenticated else None
                        order.total_amount = total
                        order.save()
                        combined_cart = cart['products'] + cart['services'] + cart['time_services']
                        for item in combined_cart:
                            OrderItem.objects.create(order=order, product_id=item.id, quantity=item.quantity,
                                                     name=item.name, price_at_order_time=item.price)
                            if item.id and item.category == 'products':
                                item_db = Product.objects.get(id=item.id)
                                if item_db.stock - item.quantity < 0:
                                    raise ValueError(f'Not enough stock for product {item.name}')
                                else:
                                    item_db.stock -= item.quantity
                                    item_db.save()
                        ### EMAILS ##########################################################
                        if EMAIL_SETTING:
                            Email.send_order_summary_email_to_shop(combined_cart, total, order)
                            Email.send_order_summary_email_to_client(combined_cart, total, order)
                        else:
                            preview_email_message(request, combined_cart, total, order, "order")
                        #####################################################################
                        request.session.pop('cart')
                        request.session.modified = True
                        messages.success(request, 'Your order has been placed')
                        return redirect('home')
                except ValueError:
                    messages.error(request, f'Not enough items for {item.name} - ({item_db.stock} in stock)')
                except Exception:
                    messages.error(request, 'Error with processing order - try again later')
            else:
                messages.error(request, 'Wrong Captcha answer')
        else:
            messages.error(request, 'Wrong data')
    captcha, answer = Captcha.generate_captcha()
    context = {"form": form, "cart": cart, "total": total, "captcha": captcha, "answer": answer}
    print(form.errors.as_data())
    return render(request, 'shop/checkout.html', context)


# GET - Contact page #
@require_GET
def contact(request):
    form_data =  {"email": request.user.email} if request.user.is_authenticated else {}
    form = ContactForm(initial=form_data)
    captcha, answer = Captcha.generate_captcha()
    context = {"form": form, "captcha": captcha, "answer": answer}
    return render(request, "shop/contact.html", context)


# POST - Send contact message to shop #
@require_POST
def send_contact_message(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        if request.POST["captcha_input"] == request.POST["captcha_answer"]:
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            try:
                ### EMAIL #####################################################
                if EMAIL_SETTING:
                    Email.send_contact_email(email, subject, message)
                    messages.success(request, "Message send successfully")
                else:
                    preview_email_message(request, email, subject, message, "message_to_shop")
                ###############################################################
                return redirect("shop")
            except Exception:
                messages.error(request, "Error with sending message")
        else:
            messages.error(request, "Wrong Captcha answer")
    else:
        messages.error(request, "Invalid data")
    captcha, answer = Captcha.generate_captcha()
    context = {"form": form, "captcha": captcha, "answer": answer}
    return render(request, "shop/contact.html", context)


# GET - Terms and conditions page #
@require_GET
def terms_conditions(request):
    return render(request, "shop/terms_conditions.html")
