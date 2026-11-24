from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_get, name="login"),
    path("login_user/", views.login_post, name="login_user"),
    path("register/", views.register_get, name="register"),
    path("register_user/", views.register_post, name="register_user"),
    path("logout/", views.logout_get, name="logout"),
    path("user/", views.account_get, name="account"),
    path("user/update_account/", views.account_post, name="update_account")
]