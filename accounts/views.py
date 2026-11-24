from django.shortcuts import render, redirect
from .forms import RegisterForm, ChangeDeliveryDataForm
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from shop.captcha import Captcha
from shop.models import Order
from django.utils.timezone import localtime
from .models import UserInfo


# GET - LOGIN PAGE #
@require_GET
def login_get(request):
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


# POST - LOGIN #
@require_POST
def login_post(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        if user.is_superuser:
            return redirect("/admin/")
        messages.success(request, "Successfully logged in")
        return redirect("shop")
    messages.error(request, "Invalid data")
    return redirect("login")


# GET - REGISTER PAGE #
@require_GET
def register_get(request):
    form = RegisterForm()
    captcha, answer = Captcha.generate_captcha()
    context = {"form": form, "captcha": captcha, "answer": answer}
    return render(request, "accounts/register.html", context)


# POST - REGISTER #
@require_POST
def register_post(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        if request.POST["captcha_input"] == request.POST["captcha_correct"]:
            form.save()
            messages.success(request, "Account created")
            return redirect("login")
        else:
            messages.error(request, "Wrong Captcha answer")
    else:
        messages.error(request, "Registration failed. Correct your data")
    captcha, answer = Captcha.generate_captcha()
    context = {"form": form, "captcha": captcha, "answer": answer}
    return render(request, "accounts/register.html", context)


# GET - LOGOUT #
@require_GET
@login_required
def logout_get(request):
    cart = request.session.get("cart", {})
    logout(request)
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "Successfully logged out")
    return redirect("home")


# GET - ACCOUNT PAGE #
@require_GET
@login_required
def account_get(request):
    if request.user.is_superuser:
        messages.error(request, "You can't access this endpoint with admin account")
        return redirect("home")
    auto_fill_data = {
        "address_1": request.user.userinfo.address_1,
        "address_2": request.user.userinfo.address_2,
        "zip_code": request.user.userinfo.zip_code,
        "city": request.user.userinfo.city,
        "phone": request.user.userinfo.phone}
    form = ChangeDeliveryDataForm(initial=auto_fill_data)
    orders = Order.objects.filter(user=request.user).order_by("-date")
    for order in orders:
        order.date = localtime(order.date)
    context = {"form": form, "email": request.user.username, "orders": orders,
               "name": request.user.first_name + ' ' + request.user.last_name}
    return render(request, "accounts/account.html", context)


# POST - UPDATE ACCOUNT #
@require_POST
@login_required
def account_post(request):
    form = ChangeDeliveryDataForm(request.POST)
    if form.is_valid():
        user_info = UserInfo.objects.get(user=request.user)
        user_info.address_1 = request.POST["address_1"]
        user_info.address_2 = request.POST["address_2"]
        user_info.zip_code = request.POST["zip_code"]
        user_info.city = request.POST["city"]
        user_info.phone = request.POST["phone"]
        user_info.save()
        messages.success(request, "Account updated")
    else:
        messages.error(request, "Wrong data")
    return redirect("account")