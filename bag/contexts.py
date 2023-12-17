from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant
from checkout.models import OrderDiscount
from django.contrib import messages


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    discount_code = request.session.get('discount_code', {})

    for item_id, quantity in bag.items():
        if item_id.startswith('variant_'):
            """
            If the product being added is a product variant then get the
            variant ID and get the variant from the database using the ID
            and set the type to 'variant' so it can be identified when it
            is passed to the template
            """

            variant_id = int(item_id.split('_')[1])
            variant = get_object_or_404(ProductVariant, pk=variant_id)
            total += quantity * (variant.sale_price if variant.sale_price else variant.price)  # NOQA
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'variant': variant,
                'type': 'variant',
            })
        else:
            """
            If the product being added is not a variant
            then get the product from the database using the ID
            and set the type to 'product' so it can be identified when it
            is passed to the template
            """

            product = get_object_or_404(Product, pk=item_id)
            total += quantity * (product.sale_price if product.sale_price else product.price)  # NOQA
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'type': 'product',
            })

    if product_count > 0 and total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = Decimal(settings.STANDARD_DELIVERY_COST)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    if discount_code:
        discount_code = get_object_or_404(
            OrderDiscount, code__iexact=discount_code)
        if total >= discount_code.min_spend:
            if discount_code.percent:
                discount_total = (total * (discount_code.discount / 100))
            else:
                discount_total = discount_code.discount
        else:
            discount_total = 0

        # Check if discount_total is 0 and remove discount_code from session
        if discount_total == 0:
            # message only if not on checkout_success page
            if request.resolver_match.url_name != 'checkout_success':
                messages.warning(
                    request, f'The discount code {discount_code.code} \
                    has been removed because the minimum spend requirement \
                    was not met.'
                )
            del request.session['discount_code']
    else:
        discount_total = 0

    grand_total = delivery + total - discount_total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'discount_code': discount_code,
        'discount_total': discount_total,
        'grand_total': grand_total,
    }

    return context
