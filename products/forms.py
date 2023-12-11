from django import forms
from .models import Product, ProductVariant, Category


class ProductForm(forms.ModelForm):
    """
    Product form to add a new product to the store
    and add nutritional info to the product
    """

    # Nutritional info fields
    energy_kcal = forms.IntegerField(label='Energy (kcal)', min_value=0)
    energy_kj = forms.IntegerField(label='Energy (kj)', min_value=0)
    fat = forms.IntegerField(label='Fat', min_value=0)
    saturated_fat = forms.IntegerField(label='Saturated Fat', min_value=0)
    carbs = forms.IntegerField(label='Carbs', min_value=0)
    sugar = forms.IntegerField(label='Sugar', min_value=0)
    protein = forms.IntegerField(label='Protein', min_value=0)
    fibre = forms.IntegerField(label='Fibre', min_value=0)
    salt = forms.IntegerField(label='Salt', min_value=0)

    class Meta:
        model = Product
        fields = [
            'has_variants',
            'category',
            'sku',
            'name',
            'description',
            'ingredients',
            'allergens',
            'price',
            'sale_price',
            'new',
            'image_url',
            'image',
            'size',
            'size_unit',
            'portion_size',
            'portion_unit',
            'stock_count',
        ]
        labels = {
            'has_variants': '**IMPORTANT** Is this product a single item or\
                will it have multiple variants?',
            'new': 'Is this a new product?',
        }

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

        # Check if a product with the same SKU already exists
        if Product.objects.filter(sku=sku).exists(
        ) or ProductVariant.objects.filter(sku=sku).exists():
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

        # Check if the SKU already exists for products or variants
        if Product.objects.filter(sku=sku).exists(
        ) or ProductVariant.objects.filter(sku=sku).exists():
            raise forms.ValidationError(
                "This SKU is already in use. Please provide a unique SKU for \
                    products and variants."
            )

        return sku
