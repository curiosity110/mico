from django.db.models import Count, Case, When, Value, BooleanField, Prefetch
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from core.pagination import InternalPagination
from orders.models import Customer, Order, CustomerComment
from orders.serializer import OrderSerializer


# Create your views here.
class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    page_size = 100
    max_page_size = 500
    pagination_class = InternalPagination

    def get_queryset(self):
        return (
            Order.objects.all()
            .select_related("agent", "order_item__product")
            .prefetch_related(
                Prefetch("customer", queryset=self.get_customer_queryset())
            )
            .order_by("-id")
        )

    def get_customer_queryset(self):
        return Customer.objects.annotate(
            orders_count=Count("orders"), comments_count=Count("comments")
        ).annotate(
            has_history=Case(
                When(orders_count__gte=2, then=Value(True)),
                When(comments_count__gte=1, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )


class RetrieveOrderView(RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Order.objects.select_related(
            "agent", "order_item__product"
        ).prefetch_related(Prefetch("customer", queryset=self.get_customer_queryset()))

    def get_customer_queryset(self):
        return Customer.objects.annotate(
            orders_count=Count("orders"), comments_count=Count("comments")
        ).annotate(
            has_history=Case(
                When(orders_count__gte=2, then=Value(True)),
                When(comments_count__gte=1, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )


class UpdateOrderStatusView(APIView):

    class InputSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=Order.Status)

    def patch(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data["status"]

        order = get_object_or_404(Order, id=kwargs["pk"])
        order.status = status

        order.save()

        return Response(OrderSerializer(order).data)


class UpdateOrderAgentView(APIView):

    class InputSerializer(serializers.Serializer):
        agent_id = serializers.IntegerField()

    def patch(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agent_id = serializer.validated_data["agent_id"]

        order = get_object_or_404(Order, id=kwargs["pk"])

        if agent_id is None:
            agent = None
        else:
            agent = get_object_or_404(User, id=agent_id)

        order.agent = agent
        order.save()

        return Response(OrderSerializer(order).data)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"])
        order.agent = None
        order.save()

        return Response(OrderSerializer(order).data)


class ConfirmOrderView(APIView):
    class InputSerializer(serializers.Serializer):
        address = serializers.CharField()
        quantity = serializers.IntegerField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data["address"]
        quantity = serializer.validated_data["quantity"]

        order = get_object_or_404(Order, id=kwargs["pk"])
        if order.agent is None or order.agent != request.user:
            return PermissionDenied(
                "You are not allowed to confirm this order because it is not assigned to you."
            )
        order.status = Order.Status.CONFIRMED
        order.address = address
        order.save()

        order_item = order.order_item

        if order_item.quantity != quantity:
            order_item.quantity = quantity
            order_item.save()

        return Response(OrderSerializer(order).data)


class AddCommentView(APIView):
    class InputSerializer(serializers.Serializer):
        comment = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data["comment"]

        order = get_object_or_404(Order, id=kwargs["pk"])

        CustomerComment.objects.create(
            customer=order.customer, order=order, comment=comment, agent=request.user
        )

        return Response(OrderSerializer(order).data)
