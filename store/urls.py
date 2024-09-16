from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='store.home'),
    path('cart',views.cart,name='store.cart'),  
    path('cart/add/<int:cid>', views.cart_update, name='store.cart_update'),
    path('cart/remove/<int:cid>',views.remove_cart,name='store.remove_cart'),
    path('category/<int:pk>',views.category,name='store.category'),
    path('category/',views.category,name='store.category'),
    path('product/<int:pk>',views.product,name='store.product'),
    path('checkout',views.checkout,name='store.checkout'),
    path('checkout-complete',views.checkout_complete,name='store.checkout_complete'),
    path('contact',views.contact,name='store.contact'),
]
