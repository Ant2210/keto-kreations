from django.shortcuts import (
    render, redirect, get_object_or_404, reverse, HttpResponse)
from django.contrib import messages
from products.models import Product, ProductVariant


def view_bag(request):
    """ A view to return the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if 'product-size' in request.POST:
        """
        If a product size is selected, add the corresponding product
        variant by it's ID and prefix the item_id with 'variant_' so
        it can be identified in the context processor
        """

        variant_id = request.POST['selected_variant_id']
        item_id = f"variant_{variant_id}"
        product = get_object_or_404(ProductVariant, pk=variant_id)
        current_stock = product.stock_count
    else:
        """ If no product size is selected, add the product y it's ID """

        item_id = item_id
        product = get_object_or_404(Product, pk=item_id)
        current_stock = product.stock_count

    product_name_display = product.product.name if 'product-size' in \
        request.POST else product.name

    if item_id in list(bag.keys()):
        new_quantity = bag[item_id] + quantity
    else:
        new_quantity = quantity

    if new_quantity > current_stock:
        if bag.get(item_id):
            messages.error(request,
                           f"Sorry, there is not enough stock for \
                            {quantity} items. The maximum quantity for \
                            {product_name_display} - {product.size}\
                            ({product.size_unit}) is {current_stock} and \
                            you already have {new_quantity - quantity} \
                            in your bag."
                           )
        else:
            messages.error(request,
                           f"Sorry, there is not enough stock for \
                            {quantity} items. The maximum quantity for \
                            {product_name_display} - {product.size}\
                            ({product.size_unit}) is {current_stock}."
                           )
        return redirect(redirect_url)

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product_name_display} - \
                            {product.size} ({product.size_unit}) quantity to \
                            {bag[item_id]}'
                         )
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product_name_display} - \
                            {product.size} ({product.size_unit}) to your bag'
                         )

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    quantity = int(request.POST.get('quantity'))

    if 'variant' in request.POST:
        variant_id = int(item_id.split('_')[1])
        product = get_object_or_404(ProductVariant, pk=variant_id)
        current_stock = product.stock_count
    else:
        product = get_object_or_404(Product, pk=item_id)
        current_stock = product.stock_count

    bag = request.session.get('bag', {})

    product_name_display = product.product.name if item_id.startswith(
        'variant') else product.name

    if quantity > current_stock:
        messages.error(request,
                       f"Sorry, there is not enough stock for \
                        {quantity} items. The maximum quantity for \
                        {product_name_display} - {product.size}\
                        ({product.size_unit}) is {current_stock}."
                       )
        return redirect(reverse('view_bag'))

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request,
                         f'Updated {product_name_display} - {product.size}\
                        ({product.size_unit}) quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request,
                         f'Removed {product_name_display} - {product.size}\
                        ({product.size_unit}) from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    try:
        bag = request.session.get('bag', {})

        if item_id.startswith('variant'):
            variant_id = int(item_id.split('_')[1])
            product = get_object_or_404(ProductVariant, pk=variant_id)
        else:
            product = get_object_or_404(Product, pk=item_id)

        product_name_display = product.product.name if item_id.startswith(
            'variant') else product.name

        bag.pop(item_id)
        messages.success(request,
                         f'Removed {product_name_display} - {product.size}\
                        ({product.size_unit}) from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
