from django.db import models
from django.forms import ValidationError


class Category(models.Model):
    """ The category model for the products app """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """ The products model for the products app"""

    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=False, blank=False)
    name = models.CharField(max_length=254)
    has_variants = models.BooleanField(default=False, null=False, blank=False)
    description = models.TextField()
    new = models.BooleanField(default=False, null=False, blank=False)
    on_sale = models.BooleanField(default=False, null=False, blank=False)
    ingredients = models.TextField()
    allergens = models.TextField()
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)
    size_unit = models.CharField(max_length=20, null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    portion_size = models.IntegerField(default=1, null=False, blank=False)
    portion_unit = models.CharField(
        default='g', max_length=20, null=False, blank=False)
    stock_count = models.IntegerField(null=True, blank=True)

    def clean(self):
        """
        Custom validation to ensure a sale price is set on the main product
        when there are no variants but item is marked as for sale. Also
        a price must be set where there is no product variant amd must not
        be set if there are variants.
        """

        if not self.has_variants and self.on_sale and self.sale_price <= 0:
            raise ValidationError("Sale price must be greater than 0 when the \
                                  product is on sale and has no variants."
                                  )

        if not self.has_variants and self.price <= 0:
            raise ValidationError("Price must be greater than 0 when the \
                                  product has no variants."
                                  )

        if self.has_variants and self.price > 0:
            raise ValidationError("Price must not be set when the product \
                                  has variants."
                                  )

    def save(self, *args, **kwargs):
        """
        Override the save method to run clean before saving.
        """

        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    The product variant model for the products app so each product
    size can be tracked for stock management
    """

    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE,
        related_name='variants'
        )
    sku = models.CharField(max_length=255, unique=True)
    size = models.IntegerField(default=0, null=False, blank=False)
    size_unit = models.CharField(
        default='g', max_length=20, null=False, blank=False)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, default=0)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, default=0)
    stock_count = models.IntegerField(default=0)

    def clean(self):
        """
        Custom validation to enforce business rules.
        """

        if self.product and self.product.on_sale and self.sale_price <= 0:
            raise ValidationError("Sale price must be greater than 0 when the \
                                  associated product is on sale."
                                  )

        if self.product and not self.product.on_sale and self.sale_price > 0:
            raise ValidationError("Sale price must be set to 0 when the \
                                  associated product is not on sale."
                                  )

        if self.product and self.price <= 0:
            raise ValidationError("Price must be greater than 0.")

    def save(self, *args, **kwargs):
        """
        Override the save method to run full_clean() before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class NutritionalInfo(models.Model):
    """ The nutritional info model for the products app """

    class Meta:
        verbose_name_plural = 'Nutritional Info'

    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.CASCADE,
        related_name='nutritional_infos')
    energy_kcal = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    energy_kj = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    fat = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    saturated_fat = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    carbs = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    sugar = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    protein = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    fibre = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    salt = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.product.name
