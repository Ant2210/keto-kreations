from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q, DecimalField, Min, Case, When, Count
from django.db.models.functions import Lower
from .models import Product, Category, NutritionalInfo, ProductVariant
from .forms import ProductForm, ProductVariantForm

from django.utils.html import format_html


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Annotate products with the number of variants
    products = Product.objects.annotate(num_variants=Count('productvariant'))

    # Exclude products where has_variants is true but the variant count is
    # less than 1
    products = products.exclude(has_variants=True, num_variants__lt=1)

    # Exclude products where on_sale is true and at least one variant has a
    # sale price less than or equal to 0
    products = products.exclude(
        Q(on_sale=True) & Q(productvariant__sale_price__lte=0)
    )

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

    products = Product.objects.all()
    variants = ProductVariant.objects.all()

    context = {
        'products': products,
        'variants': variants,
    }

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

            product_detail_url = reverse(
                "product_detail", args=[product.id])
            success_message = f'Successfully added product {product}!\
                <br>You can view the details \
                <a href="{product_detail_url}">here</a>'
            messages.success(request, format_html(success_message))

            return redirect('product_management')
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


def add_variant(request):
    """ Add a variant to a product """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.save()

            product_detail_url = reverse(
                "product_detail", args=[variant.product.id])
            success_message = f'Successfully added variant {variant}!\
                <br>You can view the details \
                <a href="{product_detail_url}">here</a>'
            messages.success(request, format_html(success_message))

            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to add variant. Please ensure the form is valid.'
            )
    else:
        form = ProductVariantForm()

    template = 'products/add_variant.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """

    product = get_object_or_404(Product, pk=product_id)

    # Fetch nutritional information associated with the product
    nutritional_info = product.nutritional_info

    # Create a dictionary to manually populate nutritional information fields
    nutritional_info_data = {
        'energy_kcal': nutritional_info.energy_kcal,
        'energy_kj': nutritional_info.energy_kj,
        'fat': nutritional_info.fat,
        'saturated_fat': nutritional_info.saturated_fat,
        'carbs': nutritional_info.carbs,
        'sugar': nutritional_info.sugar,
        'protein': nutritional_info.protein,
        'fibre': nutritional_info.fibre,
        'salt': nutritional_info.salt,
    }

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

            # Update nutritional information
            nutritional_info.energy_kcal = request.POST.get('energy_kcal')
            nutritional_info.energy_kj = request.POST.get('energy_kj')
            nutritional_info.fat = request.POST.get('fat')
            nutritional_info.saturated_fat = request.POST.get('saturated_fat')
            nutritional_info.carbs = request.POST.get('carbs')
            nutritional_info.sugar = request.POST.get('sugar')
            nutritional_info.protein = request.POST.get('protein')
            nutritional_info.fibre = request.POST.get('fibre')
            nutritional_info.salt = request.POST.get('salt')
            nutritional_info.save()

            product.save()

            # Delete variants if has_variants is set to False
            if not product.has_variants:
                ProductVariant.objects.filter(product=product).delete()

            # If on_sale is set to False, set sale_price to 0 for product
            # and variants
            if not product.on_sale:
                product.sale_price = 0
                product.save()
                ProductVariant.objects.filter(
                    product=product).update(sale_price=0)

            product_detail_url = reverse(
                "product_detail", args=[product.id])
            success_message = f'Successfully updated {product}!\
                <br>You can view the details \
                <a href="{product_detail_url}">here</a>'
            messages.success(request, format_html(success_message))

            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.'
            )
    else:
        # Create the ProductForm instance with the product and nutritional
        # information data
        form = ProductForm(instance=product, initial=nutritional_info_data)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def edit_variant(request, variant_id):
    """ Edit a variant in the store """

    variant = get_object_or_404(ProductVariant, pk=variant_id)

    if request.method == 'POST':
        form = ProductVariantForm(
            request.POST, request.FILES, instance=variant)
        if form.is_valid():
            form.save()

            product_detail_url = reverse(
                "product_detail", args=[variant.product.id])
            success_message = f'Successfully updated {variant}!\
                <br>You can view the details \
                <a href="{product_detail_url}">here</a>'
            messages.success(request, format_html(success_message))

            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to update variant. Please ensure the form is valid.'
            )
    else:
        form = ProductVariantForm(instance=variant)
        messages.info(request, f'You are editing {variant}')

    template = 'products/edit_variant.html'
    context = {
        'form': form,
        'variant': variant,
    }

    return render(request, template, context)


def delete_product(request, product_id):
    """ Delete a product from the store """

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'{ product.name } deleted!')
    return redirect('product_management')


def delete_variant(request, variant_id):
    """ Delete a variant from the store """

    variant = get_object_or_404(ProductVariant, pk=variant_id)
    variant.delete()
    messages.success(request, f'{ variant } deleted!')
    return redirect('product_management')
