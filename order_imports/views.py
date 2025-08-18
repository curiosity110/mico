import logging

import pandas as pd
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from accounts.models import User
from core.utils import normalize_phone_number_if_possible
from order_imports.serializers import XlsxOrderImportSerializer, OrderImportListSerializer, OrderImportDetailSerializer
from orders.models import *
from products.models import Product
from .models import OrderImport
logger = logging.getLogger(__name__)



# Create your views here.
class CreateXlsxOrderImportView(GenericAPIView):
    def __init__(self):
        super().__init__()
        self.pd = None
        self.required_headers = [
            "IME",
            "ADRESA",
            "GRAD",
            "TELEFON",
            "PRODUKTI"
        ]

    serializer_class = XlsxOrderImportSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_import = OrderImport.objects.create(
            file=serializer.validated_data['file'],
            agent=None
        )

        try:
            self.pd = pd.read_excel(
                serializer.validated_data['file'],
                engine='openpyxl',
                dtype=str,
            )
        except Exception as e:
            raise ValidationError(
                detail=f"Error reading Excel file: {str(e)}"
            )

        self._validate_headers()

        for index, row in self.pd.iterrows():
            if row[self.required_headers].isnull().all() or not row[self.required_headers].astype(
                    str).str.strip().any():
                continue

            values = {header: row.get(header, '') for header in self.required_headers}

            customer_name = values.get("IME", "").strip()
            customer_phone = values.get("TELEFON", "").strip()

            if not customer_name or not customer_phone:
                logger.warning(
                    f"Skipping row {index + 1} due to missing customer name or phone."
                )
                continue

            customer, _ = Customer.objects.get_or_create(
                phone=normalize_phone_number_if_possible(customer_phone),
                defaults = {
                    'name': customer_name,
                }
            )

            order = self._create_order(
                order_import=order_import,
                customer=customer,
                address=values.get("ADRESA", "").strip(),
                city=values.get("GRAD", "").strip()
            )

            logger.info(f"Created order {order.id} for customer {customer.name}.")
            products = values.get("PRODUKTI", "").strip()

            self._create_order_items(order, products)


        order_import.refresh_from_db()
        serializer = OrderImportDetailSerializer(order_import)

        return Response(serializer.data, status=201)


    def _create_order(self, order_import: OrderImport, customer: Customer, address: str, city: str) -> Order:
        return Order.objects.create(
            status=Order.Status.PENDING,
            type=Order.Type.IMPORTED,
            agent=None,
            customer=customer,
            address=address,
            city=city,
            order_import=order_import
        )


    def _create_order_items(self, order: Order, products: str):
        product_names = [name.strip() for name in products.split(",") if name.strip()]
        index = 0
        for product_name in product_names:
            if index == 1:
                break
            name, quantity = product_name.split(" x ") if " x " in product_name else (product_name, 1)
            index += 1

            product, created = Product.objects.get_or_create(
                name=name,
                defaults= {
                    'sale_price': 0,  # Default sale price, can be adjusted later
                    'stock_price': 0,  # Default stock price, can be adjusted later
                    'stock': 0,  # Default stock, can be adjusted later
                }
            )

            logger.info(f"Processing product: {product_name} (Created: {created})")


            order_item = OrderItem.objects.create(order=order, product=product, quantity=int(quantity), price=product.sale_price)
            logger.info(f"Created order item {order_item.id} for product {product.name}.")



    def _validate_headers(self):
        required_headers = [
            "IME",
            "ADRESA",
            "GRAD",
            "TELEFON",
            "PRODUKTI"
        ]

        actual_headers = self.pd.columns.tolist()
        missing_headers = [
            header.upper() for header in required_headers if header not in actual_headers
        ]

        if missing_headers:
            raise ValidationError(
                detail=f"Missing required headers: {', '.join(missing_headers)}"
            )

class ListOrderImportsView(ListAPIView):
    serializer_class = OrderImportListSerializer
    queryset = OrderImport.objects.all().order_by('-created_at')
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrieveOrderImportView(RetrieveAPIView):
    queryset = OrderImport.objects.all().prefetch_related('orders', 'orders__order_item', 'orders__customer')
    serializer_class = OrderImportDetailSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AssignOrderImportToAgentView(GenericAPIView):
    serializer_class = OrderImportListSerializer
    permission_classes = []

    @transaction.atomic
    def post(self, request, pk, agent_id, *args, **kwargs):
        order_import = get_object_or_404(OrderImport, pk=pk)
        agent = get_object_or_404(User, pk=agent_id)

        order_import.agent = agent
        order_import.save()

        Order.objects.filter(order_import=order_import).update(agent=agent)

        order_import.refresh_from_db()
        serializer = OrderImportListSerializer(order_import)
        return Response(serializer.data, status=200)
