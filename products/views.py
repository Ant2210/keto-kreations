from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Found info on removing duplicates from queryset here:
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet.distinct
        if 'sale' in request.GET:
            products = products.filter(Q(sale_price__isnull=False) | Q(
                productvariant__sale_price__isnull=False)).distinct()

        if 'new' in request.GET:
            products = products.filter(new=True)

        if 'all_specials' in request.GET:
            products = products.filter(Q(sale_price__isnull=False) | Q(
                productvariant__sale_price__isnull=False) | Q(
                    new=True)).distinct()

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
