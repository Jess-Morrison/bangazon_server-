"""bangazon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from bangazonapi.views import register_user, check_user, UserView, ProductView, PaymentTypeView, OrderView, OrderProductsView, ProductJointView, OrderJointView, OrderCustomerJointView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'products', ProductView, 'product')
router.register(r'paymenttypes', PaymentTypeView, 'paymenttype')
router.register(r'orders', OrderView, 'order')
router.register(r'orderproducts', OrderProductsView, 'orderproduct')

urlpatterns = [
    path('register', register_user),
    path('checkuser', check_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # path('order/<int:order>/', OrderJointView.as_view(), name='order'),
    # Tried 'orders next to the get and got this:
    # AttributeError: 'OrderProductsView' object has no attribute 'orders'
    # path('orderproduct/<int:order_id>/', OrderJointView.as_view(), name='order'),
    path('order/<int:order_id>/', OrderJointView.as_view(), name='product'),
    path('orderByCustomer/<int:customer_id>/', OrderCustomerJointView.as_view(), name='customer'),
    path('product/<int:order_id>/', ProductJointView.as_view(), name='order'),
    # path('product/<int:order_id>/', ProductView.as_view(), name='order')
]
