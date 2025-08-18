from django.contrib import admin
from products.models import Product, ProductPage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "stock", "sale_price", "stock_price"]


@admin.register(ProductPage)
class ProductPageAdmin(admin.ModelAdmin):  # <- fix typo ProdutPageAdmin -> ProductPageAdmin
    autocomplete_fields = ["product"]
    list_display = ["product_name", "slug"]  # <- show product name via a method
    list_filter = ["product"]
    list_select_related = ["product"]

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = "Product"
