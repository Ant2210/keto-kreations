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
        product = get_object_or_404(ProductVariant, pk=variant_id)
        current_stock = product.stock_count
    else:
        """ If no product size is selected, add the product y it's ID """

        item_id = item_id
        product = get_object_or_404(Product, pk=item_id)
        current_stock = product.stock_count

    if item_id in list(bag.keys()):
        new_quantity = bag[item_id] + quantity
    else:
        new_quantity = quantity

    product_name_display = product.product.name if 'product-size' in \
        request.POST else product.name

    if new_quantity > current_stock:
        if bag.get(item_id):
            messages.warning(request,
                             f"Sorry, there is not enough stock for \
                            {quantity} items. The maximum quantity for \
                            {product_name_display} - {product.size}\
                            ({product.size_unit}) is {current_stock} and \
                            you already have {new_quantity - quantity} \
                            in your bag."
                             )
        else:
            messages.warning(request,
                             f"Sorry, there is not enough stock for \
                            {quantity} items. The maximum quantity for \
                            {product_name_display} - {product.size}\
                            ({product.size_unit}) is {current_stock}."
                             )
        return redirect(redirect_url)

    bag[item_id] = new_quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
