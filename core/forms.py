from django import forms

from core.form_fields import PhoneNumberField
from orders.models import Customer, Order, OrderItem
from products.models import Product


class OrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label="Име/Презиме")
    phone = PhoneNumberField(max_length=255, label="Телефонски број")

    def save(self):
        product_id = self.cleaned_data["product_id"]
        name = self.cleaned_data["name"]
        phone = self.cleaned_data["phone"]

        customer, created = Customer.objects.get_or_create(
            phone=phone, defaults={"name": name}
        )

        order = Order.objects.create(customer=customer, status=Order.Status.PENDING, type=Order.Type.NORMAL)

        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order, product=product, quantity=1, price=product.sale_price
        )

        return order
