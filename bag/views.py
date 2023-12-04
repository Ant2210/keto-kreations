from django.shortcuts import render, redirect


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
    else:
        """ If no product size is selected, add the product y it's ID """

        item_id = item_id

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
