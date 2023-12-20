from django import forms
from django.forms import ValidationError
from .widgets import CustomClearableFileInput
from .models import Product, ProductVariant, Category, Review


class ProductForm(forms.ModelForm):
    """
    Product form to add a new product to the store
    and add nutritional info to the product
    """

    # Nutritional info fields
    energy_kcal = forms.DecimalField(
        label='Energy (kcal)', min_value=0, decimal_places=2)
    energy_kj = forms.DecimalField(
        label='Energy (kj)', min_value=0, decimal_places=2)
    fat = forms.DecimalField(label='Fat', min_value=0, decimal_places=2)
    saturated_fat = forms.DecimalField(
        label='Saturated Fat', min_value=0, decimal_places=2)
    carbs = forms.DecimalField(label='Carbs', min_value=0, decimal_places=2)
    sugar = forms.DecimalField(label='Sugar', min_value=0, decimal_places=2)
    protein = forms.DecimalField(
        label='Protein', min_value=0, decimal_places=2)
    fibre = forms.DecimalField(label='Fibre', min_value=0, decimal_places=2)
    salt = forms.DecimalField(label='Salt', min_value=0, decimal_places=2)

    class Meta:
        model = Product
        fields = [
            'has_variants',
            'new',
            'on_sale',
            'category',
            'sku',
            'name',
            'description',
            'ingredients',
            'allergens',
            'price',
            'sale_price',
            'image_url',
            'image',
            'size',
            'size_unit',
            'portion_size',
            'portion_unit',
            'stock_count',
        ]
        labels = {
            'has_variants': 'Is this product a single item or\
                will it have multiple variants?',
            'new': 'Is this a new product?',
            'on_sale': 'Is this product on sale?',
        }

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        # Set min_value=0 for existing fields
        self.fields['price'].min_value = 0
        self.fields['sale_price'].min_value = 0
        self.fields['portion_size'].min_value = 0
        self.fields['stock_count'].min_value = 0

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'
        self.fields['category'].widget.attrs['class'] += ' form-select'

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        instance = getattr(self, 'instance', None)

        # Check if a product with the same SKU already exists
        # (excluding the current instance)
        if Product.objects.filter(
            sku=sku).exclude(pk=instance.pk).exists() or \
           ProductVariant.objects.filter(sku=sku).exists():
            raise forms.ValidationError(
                "This SKU is already in use. Please provide a unique SKU for \
                    products and variants."
            )

        return sku


class ProductVariantForm(forms.ModelForm):
    """
    Product variant form to add a new product variant to the store
    """

    class Meta:
        model = ProductVariant
        fields = [
            'product',
            'sku',
            'size',
            'size_unit',
            'price',
            'sale_price',
            'stock_count',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mb-3'
        self.fields['product'].widget.attrs['class'] += ' form-select'
        self.fields['product'].choices = Product.objects.filter(
            has_variants=True).values_list('id', 'name')

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        instance = getattr(self, 'instance', None)

        # Check if a product variant with the same SKU already exists
        # (excluding the current instance)
        if Product.objects.filter(sku=sku).exists() or \
                ProductVariant.objects.filter(
                sku=sku).exclude(pk=instance.pk).exists():
            raise ValidationError(
                "This SKU is already in use. Please provide a unique SKU \
                    for products and variants."
            )

        return sku


class ReviewForm(forms.ModelForm):
    """
    Form for the product review page.
    """

    class Meta:
        model = Review
        fields = ('rating', 'comment')
        labels = {
            'comment': 'Please provide a brief comment about your experience',
        }

    # Define choices for the rating field
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        label='Please select a rating between 1 and 5'
    )

    def __init__(self, user, product, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'mb-3'
            if field == 'rating':
                self.fields[field].widget.attrs['class'] += ' form-select'
