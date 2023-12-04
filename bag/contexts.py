from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        if item_id.startswith('variant_'):
            # For product variants
            variant_id = int(item_id.split('_')[1])
            variant = get_object_or_404(ProductVariant, pk=variant_id)
            total += quantity * (variant.sale_price if variant.sale_price else variant.price) # NOQA
            product_count += quantity
            bag_items.append({
                'item_id': variant_id,
                'quantity': quantity,
                'variant': variant,
                'type': 'variant',
            })
        else:
            # For main products
            product = get_object_or_404(Product, pk=item_id)
            total += quantity * (product.sale_price if product.sale_price else product.price) # NOQA
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

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
