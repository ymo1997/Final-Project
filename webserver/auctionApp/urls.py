from django.urls import path
from .views import *

urlpatterns = [
    path('room/<int:slug>', room, name="room"),
    path('signup/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('shop/', shop, name="shop"),
    path('cart/', cart, name="cart"),
    path('', home, name="home"),
    path('add/',createProduct, name="addProduct"),
    path('product/<int:slug>',detail, name="detail"),
    path('profile',profile, name="profile"),
    path('myproducts/', my_selling_items, name="myProducts"),
    path('deleteuser/', user_delete, name="deleteuser"),
    path('suspenduser/', user_suspend, name="suspenduser"),
    path("editprofile/", edit_profile, name="edit_profile"),
    path("stopauction/", stopauction, name="stopauction"),
]
