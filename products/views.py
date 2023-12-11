from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, DecimalField, Min, Case, When, Count
from django.db.models.functions import Lower
from .models import Product, Category, NutritionalInfo
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Annotate products with the number of variants
    products = Product.objects.annotate(num_variants=Count('productvariant'))

    # Exclude products where has_variants is true but the variant count is
    # less than 1
    products = products.exclude(has_variants=True, num_variants__lt=1)

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

                products = products.annotate(
                    lowest_price=Min(
                        Case(
                            When(
                                productvariant__sale_price__gt=0,
                                then='productvariant__sale_price'
                            ),
                            When(
                                productvariant__price__gt=0,
                                then='productvariant__price'
                            ),
                            When(
                                sale_price__gt=0,
                                then='sale_price'
                            ),
                            default='price',
                            output_field=DecimalField()
                        )
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


def product_management(request):
    """ A view to show product management page """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    context = {}

    return render(request, 'products/product_management.html', context)


def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            product.save()

            # Create NutritionalInfo
            nutritional_info = NutritionalInfo.objects.create(
                energy_kcal=int(request.POST.get('energy_kcal')),
                energy_kj=int(request.POST.get('energy_kj')),
                fat=int(request.POST.get('fat')),
                saturated_fat=int(request.POST.get('saturated_fat')),
                carbs=int(request.POST.get('carbs')),
                sugar=int(request.POST.get('sugar')),
                protein=int(request.POST.get('protein')),
                fibre=int(request.POST.get('fibre')),
                salt=int(request.POST.get('salt')),
                product=product,
            )

            product.nutritional_info = nutritional_info
            product.save()

            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
