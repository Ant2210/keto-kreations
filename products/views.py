from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, Value, DecimalField, Min
from django.db.models.functions import Lower, Coalesce
from .models import Product, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if sortkey == 'price':
                sortkey = 'lowest_price'

                """
                Found info on using Coalesce to handle null values here:
                https://docs.djangoproject.com/en/4.2/ref/models/database-functions/
                I compared the model field to a large number to ensure it
                is not returned as the lowest price if that field has no
                price, Value and DecimalField I figured out from the errors
                in the browser.
                """

                products = products.annotate(
                    lowest_price=Min(
                        Coalesce('price', Value(99999),
                                 output_field=DecimalField()),
                        Coalesce('productvariant__price', Value(
                            99999), output_field=DecimalField()),
                        Coalesce('sale_price', Value(99999),
                                 output_field=DecimalField()),
                        Coalesce('productvariant__sale_price',
                                 Value(99999), output_field=DecimalField())
                    )
                )

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Found info on removing duplicates from queryset here:
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet.distinct
        if 'sale' in request.GET:
            products = products.filter(Q(sale_price__gt=0) | Q(
                productvariant__sale_price__gt=0)).distinct()

        if 'new' in request.GET:
            products = products.filter(new=True)

        if 'all_specials' in request.GET:
            products = products.filter(Q(sale_price__gt=0) | Q(
                productvariant__sale_price__gt=0) | Q(
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

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    # Check if product stock count is less not null and less than 1
    product_out_of_stock = product.stock_count and product.stock_count < 1
    variants_out_of_stock = product.productvariant_set.filter(
        stock_count__gt=0).count() == 0

    context = {
        'product': product,
        'product_out_of_stock': product_out_of_stock,
        'variants_out_of_stock': variants_out_of_stock,
    }

    return render(request, 'products/product_detail.html', context)
