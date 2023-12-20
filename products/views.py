from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q, DecimalField, Min, Case, When, Count
from django.db.models.functions import Lower
from .models import Product, Category, NutritionalInfo, ProductVariant
from checkout.models import OrderDiscount
from .forms import ProductForm, ProductVariantForm, ReviewForm

from django.utils.html import format_html


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Annotate products with the number of variants
    products = Product.objects.annotate(num_variants=Count('variants'))

    # Exclude products where has_variants is true but the variant count is
    # less than 1
    products = products.exclude(has_variants=True, num_variants__lt=1)

    # Exclude products where on_sale is true and at least one variant has a
    # sale price less than or equal to 0
    products = products.exclude(
        Q(on_sale=True) & Q(variants__sale_price__lte=0)
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
                                variants__sale_price__gt=0,
                                then='variants__sale_price'
                            ),
                            When(
                                variants__price__gt=0,
                                then='variants__price'
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
                variants__sale_price__gt=0)).distinct()

        if 'new' in request.GET:
            products = products.filter(new=True)

        if 'all_specials' in request.GET:
            products = products.filter(Q(sale_price__gt=0) | Q(
                variants__sale_price__gt=0) | Q(
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
    variants_out_of_stock = product.variants.filter(
        stock_count__gt=0).count() == 0

    form = ReviewForm(user=request.user, product=product)

    context = {
        'product': product,
        'product_out_of_stock': product_out_of_stock,
        'variants_out_of_stock': variants_out_of_stock,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def product_management(request):
    """ A view to show product management page """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    products = Product.objects.all()
    variants = ProductVariant.objects.all()
    discounts = OrderDiscount.objects.all()

    context = {
        'products': products,
        'variants': variants,
        'discounts': discounts,
        'on_product_management_page': True,
    }

    return render(request, 'products/product_management.html', context)


@login_required
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


@login_required
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


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

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


@login_required
def edit_variant(request, variant_id):
    """ Edit a variant in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

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


@login_required
@require_POST
def delete_product(request, product_id):
    """ Delete a product from the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, f'{ product.name } deleted!')
        return redirect('product_management')


@login_required
@require_POST
def delete_variant(request, variant_id):
    """ Delete a variant from the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        variant.delete()
        messages.success(request, f'{ variant } deleted!')
        return redirect('product_management')


@login_required
def stock_management(request):
    """ A view to show stock management page """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('variant_stock_count_'):
                variant_id = key.split('_')[-1]
                variant = get_object_or_404(ProductVariant, pk=variant_id)
                variant.stock_count = value
                variant.save()
            elif key.startswith('product_stock_count_'):
                product_id = key.split('_')[-1]
                product = get_object_or_404(Product, pk=product_id)
                product.stock_count = value
                product.save()

        messages.success(request, 'Stock count updated!')
        return redirect('product_management')

    products = Product.objects.all()
    variants = ProductVariant.objects.all()

    context = {
        'products': products,
        'variants': variants,
    }

    return render(request, 'products/stock_management.html', context)


@login_required
def add_discount(request):
    """ Add a discount to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('amount')
        percent = request.POST.get('percent') == "true"
        min_spend = request.POST.get('min_spend')
        active = request.POST.get('active') == "true"

        OrderDiscount.objects.create(
            code=code,
            discount=discount,
            percent=percent,
            min_spend=min_spend,
            active=active,
        )

        messages.success(request, f'Discount { code } successfully created!')
        return redirect('product_management')

    return redirect('product_management')


@login_required
@require_POST
def edit_discount(request, discount_id):
    """ Edit a discount in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    discount = get_object_or_404(OrderDiscount, pk=discount_id)

    if request.method == 'POST':
        discount.code = request.POST.get('code')
        discount.discount = request.POST.get('amount')
        discount.percent = request.POST.get('percent') == "true"
        discount.min_spend = request.POST.get('min_spend')
        discount.active = request.POST.get('active') == "true"
        discount.save()

    messages.success(request, f'{ discount } successfully updated!')
    return redirect('product_management')


@login_required
@require_POST
def delete_discount(request, discount_id):
    """ Delete a discount from the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        discount = get_object_or_404(OrderDiscount, pk=discount_id)
        discount.delete()
        messages.success(request, f'{ discount } successfully deleted!')
        return redirect('product_management')


@login_required
@require_POST
def add_review(request, product_id):
    """ Add a review to a product """

    if not request.user.is_authenticated:
        messages.error(
            request,
            'Sorry, only registered users can do that. Please login or \
                register to leave a review.'
        )
        return redirect('product_detail', product_id)

    product = get_object_or_404(Product, pk=product_id)

    form = ReviewForm(user=request.user, product=product, data=request.POST)
    print(f"Form data: {form.data}")
    print(f"Form errors: {form.errors}")
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        messages.success(request, 'Review successfully added!')
        return redirect('product_detail', product_id)
    else:
        print("Form is not valid")
        print(form.errors)
        messages.error(
            request,
            'Failed to add review. Please try again or contact us for help.'
        )
        return redirect('product_detail', product_id)
