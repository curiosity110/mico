from django.contrib import admin

from orders.models import Customer, Order, OrderItem, CustomerComment

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CustomerComment)
