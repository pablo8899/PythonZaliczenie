"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('products/', views.ProductListView.as_view(), name='products'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('card/<int:product_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('card/<int:product_id>/add/', views.add_to_cart, name='add_to_cart'),
    path('card/<int:product_id>/<int:quantity>/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/place_order/', views.place_order, name='place_order'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('export_orders/', views.export_orders_to_xml, name='export_orders_to_xml'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)