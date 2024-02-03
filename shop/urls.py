from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutpage, name='logout'),
    path('cart', views.cartpage, name='cart'),
    path('fav', views.fav, name='fav'),
    path('favviewpage', views.favviewpage, name='favviewpage'),
    path('remove_cart/<str:cid>', views.remove_cart, name='remove_cart'),
    path('remove_favourite/<str:fid>',
         views.remove_favourite, name='remove_favourite'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>', views.collectionsview, name='collections'),
    path('collections/<str:cname>/<str:pname>',
         views.product_detials, name='product_detials'),
    path('addtocart', views.addtocart, name='addtocart')
]
