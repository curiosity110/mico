from django.db import models
from core.models import BaseInternalModel
from django.conf import settings 

class Customer(BaseInternalModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        from core.utils import normalize_phone_number_if_possible
        self.phone = normalize_phone_number_if_possible(self.phone)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Order(BaseInternalModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        TAKE = "TAKE", "Take"
        CALL_AGAIN = "CALL_AGAIN", "Call Again"
        CONFIRMED = "CONFIRMED", "Confirmed"
        SHIPPED = "SHIPPED", "Shipped"
        RETURNED = "RETURNED", "Returned"
        PAID = "PAID", "Paid"
        TRASHED = "TRASHED", "Trashed"
        CANCELLED = "CANCELLED", "Cancelled"

    class Type(models.TextChoices):
        NORMAL = "NORMAL", "Normal"
        IMPORTED = "IMPORTED", "Imported"

    status = models.CharField(
        max_length=255,
        choices=Status.choices,           # <- fix
        default=Status.PENDING,
    )
    type = models.CharField(
        max_length=255,
        choices=Type.choices,             # <- fix
        default=Type.NORMAL,
    )

    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)

    # ----- OrderImport relation (fix or temporarily disable) -----
    # If you DO have an app & model named order_imports.OrderImport,
    # ensure 'order_imports' is in INSTALLED_APPS and the model is defined as OrderImport.
    # Otherwise, point to the correct app/model or comment out for now to unblock migrations.
    order_import = models.ForeignKey(
        "order_imports.OrderImport",      # <- change to "orders.OrderImport" if that's where it lives
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    # -------------------------------------------------------------

    def __str__(self):
        return f"{self.pk} - {self.status} - {self.customer}"


class OrderItem(BaseInternalModel):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="order_item"
    )
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product} - {self.quantity} - {self.price}"


class CustomerComment(BaseInternalModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="comments"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.customer} - {self.comment}"
