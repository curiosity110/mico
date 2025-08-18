from django.db import models
from django.utils.text import slugify

from core.models import BaseInternalModel


# Create your models here.
class Product(BaseInternalModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sale_price = models.PositiveIntegerField(default=0)
    stock_price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.sale_price}"


class ProductPage(BaseInternalModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    template_path = models.FilePathField(
        path="templates/product-pages/", recursive=True
    )

    def get_template_name(self):
        # return template path without templates/ prefix
        return self.template_path.split("templates/")[1]

    def __str__(self):
        return f"{self.product.name} - {self.slug}"
