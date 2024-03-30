"""
URL configuration for PetStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from petApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin1/',views.Admin,name='admin1'),
    path('adminbase/',views.adminBase,name='adminbase'),
    path('adminform/',views.AdminForm,name='adminfrom'),
    path('allanimals/',views.AllAnimals,name='allanimals'),
    path('userbase/',views.UserBase,name='userbase'),
    path('orderplace/<int:id>',views.OrderPlace,name='orderplace'),
    path('cart/',views.Add_To_Cart, name='cart'),
    path('search/',views.Search, name='search'),
    path('details/<int:id>/<str:breed>',views.Detail, name='details'),
    path('usersignup/',views.SignUp1,name='usersignup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.LogOut, name='logout'),
    path('removecart/<int:id>',views.RemoveCart,name='removecart'),
    path('finalorder/<int:aid>/<int:pid>',views.Final_order,name='finalorder'),
    path('addressdel/<int:id>',views.Address_del,name='addressdel'),
    path('preorder/<int:aid>/<int:pid>',views.Pre_Order,name='preorder'),
    path('orderconfirm/<int:aid>/<int:pid>',views.Order_Confirm,name='orderconfirm'),
    path('orders/',views.Orders,name='orders'),
    path('cartaddress/',views.Cart_Address,name='cartaddress'),
    path('cartpreorder/<int:aid>',views.Cart_Preorder,name='cartpreorder'),
    path('cartorderconfirm/<int:aid>',views.Cart_OrderConfirm,name='cartorderconfirm'),
    path('adminsignup/',views.AdminSignUp,name='adminsignup'),
    path('adminlogin/',views.AdminLogin,name='adminlogin'),
    path('welcome/<int:aid>/<int:pid>',views.Real_Order,name='welcome'),
    path('cartconfirm/<int:aid>',views.CartReal_Order,name='cartconfirm'),
    path('pay/',views.final,name='pay'),
    path('deliveryboy/',views.Delivery_Boy,name='deliveryboy'),
    path('orderhisory/<int:pid>/<int:aid>',views.Order_Histories,name='orderhistory'),
    path('orderhistoryshow/',views.Order_Histories_Show,name='orderhistoryshow'),
    path('adminprofile/',views.Admin_Profile,name='adminprofile'),
    path('',views.IndexPage,name='index'),
    # path('passchange/',views.PassowrdChange,name='passchange'),
    path('otpgenerate/',views.OTP_Generate,name='otpgenerate'),
    path('addcomment/<int:id>/<str:breed>',views.Comment,name='addcomment')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
