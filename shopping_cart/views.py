from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from datetime import date
import datetime
import random
import string

import braintree
import stripe

from profiles.models import Profile
from products.models import Product
from shopping_cart.models import OrderItem, Order, Transaction


# Manage Views
stripe.api_key = settings.STRIPE_SECRET_KEY


def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # order_item: create order item of selected product
    # status: check if the user already owns this product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(
        owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "Item added to cart.")
    return redirect(reverse('products:product_list'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return redirect(reverse('shopping_cart:update_records',
                                        kwargs={
                                            'token': token
                                        })
                                )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            if existing_order:
                result = transact({
                    'amount': existing_order.get_cart_total(),
                    'payment_method_nonce': request.POST['payment_method_nonce'],
                    'options': {
                        "submit_for_settlement": True
                    }
                })
            else:
                result = transact({
                    'amount': 0,
                    'payment_method_nonce': request.POST['payment_method_nonce'],
                    'options': {
                        "submit_for_settlement": True
                    }
                })


            if result.is_success or result.transaction:
                return redirect(reverse('shopping_cart:update_records',
                                        kwargs={
                                            'token': result.transaction.id
                                        })
                                )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('shopping_cart:checkout'))

    context = {
        'order': existing_order,
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'shopping_cart/checkout.html', context)


@login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.owned_item.add(*order_products)
    user_profile.save()

    # create and save a transaction
    transaction = Transaction(profile=request.user.profile,
                              token=token,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)
    transaction.save()

    # send an email to the customer: look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('profiles:my_profile'))


def success(request, **kwargs):
    # Indicate transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})


# View Functions

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=settings.BT_ENVIRONMENT,
        merchant_id=settings.BT_MERCHANT_ID,
        public_key=settings.BT_PUBLIC_KEY,
        private_key=settings.BT_PRIVATE_KEY
    )
)


def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[
        2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str


def generate_client_token():
    return gateway.client_token.generate()


def transact(options):
    return gateway.transaction.sale(options)


def find_transaction(id):
    return gateway.transaction.find(id)
