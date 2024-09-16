from .models import Category,Cart,Product


def website_store(request):

    categories = Category.objects.order_by('order')
    cart = Cart.objects.filter(session=request.session.session_key).last()
    cart_total = 0
    cart_products = []
    if cart:
        cart_products = Product.objects.filter(pk__in=cart.cart_items)
        for item in cart_products:
            cart_total +=item.price
    return {"categories":categories,'cart_products':cart_products,'total':cart_total}