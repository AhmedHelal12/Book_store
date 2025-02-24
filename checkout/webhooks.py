
from django.views.decorators.csrf import csrf_exempt
import stripe
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.http import HttpResponse
from checkout import models
from store.models import Order, Product
from django.core.mail import send_mail
from django.template.loader import render_to_string
from book_store import settings
import json

@csrf_exempt
def stripe_webhook(request):
    print('Stripe Webhook Received')

    payload = request.body.decode('utf-8')
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        print('Invalid payload')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        print('Invalid signature')
        return HttpResponse(status=400)

    # Print full event data for debugging
    event_data = json.loads(payload)
    print(json.dumps(event_data, indent=2))  # Log the entire event

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print("Payment Intent Object:", payment_intent)

        transaction_id = payment_intent.get('metadata', {}).get('transaction')
        if not transaction_id:
            print("ERROR: transaction_id is missing in metadata")
            return HttpResponse(status=400)

        print(f"Processing transaction: {transaction_id}")
        make_order(transaction_id)

    return HttpResponse(status=200)

@csrf_exempt
def paypal_webhook(sender, **kwargs):
    if sender.payment_status == ST_PP_COMPLETED:
        if sender.receiver_email != settings.PAYPAL_EMAIL:
            return
        print('PaymentIntent was successful')
        make_order(sender.invoice)


valid_ipn_received.connect(paypal_webhook)


def make_order(transaction_id):
    try:
        transaction = models.Transaction.objects.get(pk=transaction_id)
    except models.Transaction.DoesNotExist:
        print(f"❌ Transaction {transaction_id} not found")
        return HttpResponse(f"Transaction {transaction_id} not found", status=400)

    print("✅ Transaction found:", transaction)

    transaction.status = models.TransactionStatus.Completed
    transaction.save()

    order = Order.objects.create(transaction=transaction)

    print("Transaction items:", transaction.items)

    if not isinstance(transaction.items, list):
        return HttpResponse("Invalid items", status=400)

    products = Product.objects.filter(pk__in=transaction.items)
    for product in products:
        order.orderproduct_set.create(product_id=product.id, price=product.price)

    msg_html = render_to_string('emails/order.html', {'order': order, 'products': products})

    if not transaction.customer_email:
        return HttpResponse("Missing email", status=400)

    send_mail(
        subject='New Order',
        html_message=msg_html,
        message=msg_html,
        from_email='noreply@example.com',
        recipient_list=[transaction.customer_email]
    )

    print("✅ Order and email sent successfully!")
    return HttpResponse("Order processed", status=200)