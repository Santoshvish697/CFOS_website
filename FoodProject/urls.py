"""FoodProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from foodapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---- HOME ----
    path('', views.foodapp),
    path('home', views.foodapp),

    # ---- FOOD ----
    path('addfoods', views.addfood),
    path('deletefood/<int:FoodId>', views.deletefood),
    path('getfood/<int:FoodId>', views.getfood),
    path('editfood/<int:FoodId>', views.updatefood),
    path('allfood', views.showfood),

    # ---- CUSTOMER ----
    path('addcustomer', views.addcust),
    path('deletecustomer/<int:CustId>', views.deletecust),
    path('getcustomer', views.getcust),
    path('editcustomer/<int:CustId>', views.updatecust),
    path('allcustomer', views.showcust),
    path('foodcatalogue/', views.foodcatalogue),

    # ---- CUSTOMER ----
    path('updatepasswd', views.updatepasswd),
    path('updatepassword', views.changepass),

    # ---- LOGIN ----
    path('login', views.login),
    path('dologin', views.doLogin),
    path('logout', views.doLogout),

    # ---- CART ----
    path('addtocart/<int:FoodId>', views.addcart),
    path('allcart', views.showcart),
    path('deletecart/<int:CartId>', views.delcart),
    path('updateqnty/<str:s>', views.updateQNT),

    # ---- ORDER ----
    path('placeorder', views.placeorder),
    path('orders', views.getorder),
        path('wallet/',views.wallet,name = "wallet"),
    path('add_funds/',views.add_funds,name = "add_funds"),
    path('subtract_funds/',views.subtract_funds,name = "subtract_funds"),
    path('admin_wallet/',views.admin_acc,name= "admin_wallet")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)