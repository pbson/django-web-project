from django.urls import path 
from django.conf.urls import url

from .views import (HomePageListView,
                    ProductDetailView,
                    add_to_cart,
                    remove_from_cart,
                    OrderSummaryView, 
                    remove_single_product_from_cart,
                    CheckoutView,
                    OrderInfo,
                    BestSellerListView,
                    CategoryDetailView)
app_name="homepage"

urlpatterns = [
    path('',HomePageListView.as_view(),name='home'), 
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('product/<slug>',ProductDetailView.as_view(),name='product'), 
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('remove-product-from-cart/<slug>/', remove_single_product_from_cart,name='remove-single-product-from-cart'),
    path('order-info/', OrderInfo.as_view(), name='order-info'),
    path('sale/', BestSellerListView.as_view(), name='sale'),
    path('category/<slug>',CategoryDetailView.as_view(),name='category'), 
    
]
