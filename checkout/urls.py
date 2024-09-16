from django.urls import path
from .views import make_order
urlpatterns = [
    path('/order',make_order,name='checkout.order')
]
