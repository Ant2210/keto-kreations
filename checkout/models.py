from decimal import Decimal
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product, ProductVariant


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID.
        """

        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """

        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or Decimal('0.00')
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY_COST
        else:
            self.delivery_cost = Decimal('0.00')
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems'
                              )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariant, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False
                                         )

    def clean(self):
        """
        Ensures that either a product or a product variant is specified,
        but not both. Found this solution here:
        https://docs.djangoproject.com/en/4.2/ref/forms/validation/#
        """
        if not self.product and not self.product_variant:
            raise ValidationError(
                "Either a Product or a ProductVariant is required."
            )

        if self.product and self.product_variant:
            raise ValidationError(
                "You cannot specify both a Product and a ProductVariant."
            )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total
        """

        self.clean()
        if self.product_variant:
            if self.product_variant.sale_price:
                price = self.product_variant.sale_price
            else:
                price = self.product_variant.price
        else:
            if self.product.sale_price:
                price = self.product.sale_price
            else:
                price = self.product.price

        self.lineitem_total = price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        if self.product_variant:
            return f'SKU {self.product_variant.sku} \
                on order {self.order.order_number}'
        elif self.product:
            return f'SKU {self.product.sku} on order {self.order.order_number}'
        else:
            return 'Invalid OrderLineItem \
                (no product or product variant specified)'
