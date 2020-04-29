from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="ShopHome"),
    path('about/',views.about,name="About Us"),
    path('signin/',views.signin,name="Welcome"),
    path('contact/',views.contact,name="contact Us"),
    path('tracker/',views.tracker,name="trackingStatus"),
    path('products/<int:myid>',views.prodview,name="productView"),
    path('search/',views.search,name="Search"),
    path('checkout/',views.checkout,name="Checkout"),
    path('login',views.handlelogin, name="handleLogin"),
    path('logout',views.handlelogout, name="handleLogout"),
    path('signup', views.handlesignup, name="signUp"),
]
