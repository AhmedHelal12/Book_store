from django.shortcuts import render
from .models import Product,Slider,Category,Cart
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.translation import gettext as _
def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    sliders = Slider.objects.order_by('order')

    return render(request,'index.html',{
        'products':products,
        'sliders':sliders
    })

def cart(request):
    cart = Cart.objects.filter(session=request.session.session_key)
    return render(request,'cart.html',{'cart':cart})

def cart_update(request, cid):
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    print(f"Session ID: {session_id}")
    
    cart = Cart.objects.filter(session_id=session_id).last()
    print(f"Cart: {cart}")
    
    if cart is None:
        cart = Cart.objects.create(session_id=session_id, cart_items=[cid])
        print(f"Created new cart: {cart}")
    elif cid not in cart.cart_items:
        cart.cart_items.append(cid)
        cart.save()
        print(f"Updated cart with new item: {cart.cart_items}")
    
    return JsonResponse({
        "message": _("The product has been added to your cart"),
        "items_count": len(cart.cart_items)
    })

def remove_cart(request,cid):
 
    
    session_id = request.session.session_key
    if not session_id:
        return JsonResponse({})
    cart = Cart.objects.filter(session_id=session_id).last()
    if cart is None:
        return JsonResponse({})
    elif cid  in cart.cart_items:
        cart.cart_items.remove(cid)
        cart.save()
    
    return JsonResponse({"message":_("The product has been removed from your cart"),"items_count":len(cart.cart_items)})

def category(request,pk=None):

    cat = None
    query = request.GET.get('query')
    pk = request.GET.get('category',pk)
    where = {}
    if pk:
        cat = Category.objects.get(pk=pk)
        where['category_id'] = pk
    
    if query:
        where['short_description__icontains']=query


    products = Product.objects.filter(**where)
    paginator = Paginator(products,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,'category.html',{
            'category':cat,
            'page_obj':page_obj
        })

def checkout(request):
    return render(request,'checkout.html')

def checkout_complete(request):
    return render(request,'checkout-complete.html')

def contact(request):
    return render(request,'contact.html')

def product(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,'product.html',{'product':product})