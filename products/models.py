from django.db import models


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
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    ingredients = models.TextField()
    allergens = models.TextField()
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, default=0)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)
    size_unit = models.CharField(max_length=20, null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    new = models.BooleanField(default=False, null=True, blank=True)
    portion_size = models.IntegerField(default=1, null=False, blank=False)
    portion_unit = models.CharField(
        default='g', max_length=20, null=False, blank=False)
    stock_count = models.IntegerField(null=True, blank=True)
    nutritional_info = models.ForeignKey(
        'NutritionalInfo', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='nutritional_infos')

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    The product variant model for the products app so each product
    size can be tracked for stock management
    """

    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, unique=True)
    size = models.IntegerField(default=1, null=False, blank=False)
    size_unit = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, default=0) # NOQA
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, default=0)
    stock_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class NutritionalInfo(models.Model):
    """ The nutritional info model for the products app """

    class Meta:
        verbose_name_plural = 'Nutritional Info'

    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.CASCADE,
        related_name='nutritional_infos')
    energy_kcal = models.IntegerField(null=True, blank=True)
    energy_kj = models.IntegerField(null=True, blank=True)
    fat = models.IntegerField(null=True, blank=True)
    saturated_fat = models.IntegerField(null=True, blank=True)
    carbs = models.IntegerField(null=True, blank=True)
    sugar = models.IntegerField(null=True, blank=True)
    protein = models.IntegerField(null=True, blank=True)
    fibre = models.IntegerField(null=True, blank=True)
    salt = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product.name
