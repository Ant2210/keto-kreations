from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import Order, OrderForm
from .models import OrderLineItem, OrderDiscount
from products.models import Product, ProductVariant
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """ Cache checkout data for stripe """

    try:
        json_data = json.loads(request.body.decode('utf-8'))
        pid = json_data.get('client_secret').split('_secret')[0]
        save_info = json_data.get('save_info', False)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': save_info,
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handles the checkout process by creating an order and order line items.
    It also checks the stock for each item in the bag and displays an error
    message if there's not enough stock. It also checks if the user is
    authenticated and pre-fills the order form with the user's default
    information then renders the checkout page with the order form.
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        # Perform a stock check before creating the order
        for item_id, quantity in bag.items():
            try:
                if item_id.startswith('variant_'):
                    variant_id = int(item_id.split('_')[1])
                    variant = get_object_or_404(ProductVariant, pk=variant_id)
                    if variant.stock_count < quantity:
                        messages.error(
                            request, f"Sorry, there is not enough stock for \
                            {variant.product.title}. Please update the \
                            quantity in your bag."
                        )
                        return redirect(reverse('view_bag'))
                else:
                    product = get_object_or_404(Product, pk=item_id)
                    if product.stock_count < quantity:
                        messages.error(
                            request, f"Sorry, there is not enough stock for \
                            {product.title}. Please update the quantity in \
                            your bag."
                        )
                        return redirect(reverse('view_bag'))
            except (Product.DoesNotExist, ProductVariant.DoesNotExist):
                messages.error(
                    request, "One of the products in your bag wasn't found in \
                    our database. Please call us for assistance!"
                )
                return redirect(reverse('view_bag'))

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            discount_code_str = request.session.get('discount_code')
            if discount_code_str:
                discount_code = get_object_or_404(
                    OrderDiscount, code__iexact=discount_code_str
                )
                order.discount_code = discount_code
            order.save()
            for item_id, quantity in bag.items():
                try:
                    if item_id.startswith('variant_'):
                        variant_id = int(item_id.split('_')[1])
                        variant = get_object_or_404(
                            ProductVariant, pk=variant_id
                        )
                        order_line_item = OrderLineItem(
                            order=order,
                            product_variant=variant,
                            quantity=quantity,
                        )
                        order_line_item.save()
                    else:
                        product = get_object_or_404(Product, pk=item_id)
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                        order_line_item.save()
                except (Product.DoesNotExist, ProductVariant.DoesNotExist):
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our "
                        "database. Please call us for assistance!"
                    )
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                           Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment"
            )
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.full_name,
                    'email': (
                        profile.email if profile.email else profile.user.email
                    ),
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key missing. Did you forget \
                         to set it in your environment?'
                         )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    discount_amount = 0

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'full_name': order.full_name,
                'email': order.email,
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

        discount_amount = 0
        if order.discount_code:
            if order.discount_code.percent:
                discount_amount = (
                    order.order_total + order.delivery_cost) * (
                        order.discount_code.discount / 100)
            else:
                discount_amount = order.discount_code.discount

    messages.success(request, f'Order successfully processed! Your order \
                    number is {order_number}. A confirmation email will be \
                    sent to {order.email}.'
                     )

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'discount_amount': discount_amount,
    }

    return render(request, template, context)
