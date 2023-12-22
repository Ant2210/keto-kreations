from django.contrib import admin
from .models import Order, OrderDiscount, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Allows us to add and edit line items in the admin right from inside
    the order model.
    """

    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    This class allows us to customize the admin interface for orders.
    """

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid',)

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)


class OrderDiscountAdmin(admin.ModelAdmin):
    """
    This class allows us to customize the admin interface for order discounts.
    """

    fields = ('code', 'discount', 'percent', 'min_spend', 'active',)

    list_display = (
        'code',
        'discount',
        'percent',
        'min_spend',
        'active',
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDiscount, OrderDiscountAdmin)
