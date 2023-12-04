from django.shortcuts import render, redirect, get_object_or_404
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
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        current_stock = variant.stock_count
    else:
        """ If no product size is selected, add the product y it's ID """

        item_id = item_id
        product = get_object_or_404(Product, pk=item_id)
        current_stock = product.stock_count

    if item_id in list(bag.keys()):
        new_quantity = bag[item_id] + quantity
    else:
        new_quantity = quantity

    # Check if the new quantity exceeds the current stock
    if new_quantity > current_stock:
        messages.warning(
            f"Sorry, there is not enough stock for {new_quantity} items. The \
                maximum quantity for this item is {current_stock} which \
                includes items that may already be in your bag.")
        return redirect(redirect_url)

    bag[item_id] = new_quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
