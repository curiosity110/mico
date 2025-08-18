from django.contrib import admin

from products.models import Product, ProductPage


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "stock", "sale_price", "stock_price"]


@admin.register(ProductPage)
class ProdutPageAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]
    list_display = ["product__name", "slug"]
    list_filter = ["product"]
