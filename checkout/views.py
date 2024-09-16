from django.shortcuts import render,redirect
from .forms import UserInfo
from store.models import Cart,Product,Order,OrderProduct
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.
def make_order(request):

    if request.method != "POST":
        return redirect('store.checkout')
    
    form = UserInfo(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.cart_items)

        total = 0

        for item in products:
            total += item.price
        
        if total <=0:
            return redirect('store.cart')

        order = Order.objects.create(customer=form.cleaned_data,total=total)

        for product in products:
            ##order.orderproduct_set.create(product_id=product.id,price=product.price)
            OrderProduct.objects.create(order_id=order.id,product_id=product.id,price=product.price)
        
        send_order_email(order,products)
        cart.delete()

        return redirect('store.checkout_complete')
    else:
        return redirect('store.checkout')


def send_order_email(order,products):
    html_msg = render_to_string('email/order.html',{'order':order,'products':products})

    send_mail(
       subject="New Order",
       from_email="ahmed@gmail.com",
       recipient_list=[order.customer['first_name']],
       message=html_msg,
       html_message=html_msg)