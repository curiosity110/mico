from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Count, Case, When, Value, BooleanField, Prefetch
from rest_framework import serializers
from rest_framework.generics import ListAPIView, DestroyAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from orders.models import Order, Customer
from orders.serializer import OrderSerializer
from .models import User
from .serializers import UserSerializer, GroupSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]


class GetMeView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


class UsersListView(ListAPIView):
    queryset = User.objects.filter(is_active=True).prefetch_related("groups", "groups__description").order_by("pk")
    serializer_class = UserSerializer


class UsersDeleteView(DestroyAPIView):
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CreateUserView(CreateAPIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(
            help_text="Username for the user.",
            required=True,
            allow_blank=False,
            max_length=150,
            min_length=3,
        )
        email = serializers.EmailField(
            help_text="Email address of the user.",
            required=True,
            allow_blank=False,
        )
        first_name = serializers.CharField(
            help_text="First name of the user.",
            required=True,
            allow_blank=False,
        )
        last_name = serializers.CharField(
            help_text="Last name of the user.",
            required=True,
            allow_blank=False,
        )
        password = serializers.CharField(
            help_text="Password for the user.",
            required=True,
            write_only=True,
            min_length=8,
        )
        confirm_password = serializers.CharField(
            help_text="Confirm password for the user.",
            required=True,
            write_only=True,
            min_length=8,
        )
        groups = serializers.ListField(
            child=serializers.IntegerField(),
            write_only=True,
            min_length=1,
            help_text="List of group IDs to assign to the user.",
        )

    serializer_class = InputSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["password"] != serializer.validated_data["confirm_password"]:
            return Response(
                {"error": "Passwords do not match."},
                status=400
            )

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            password=serializer.validated_data["password"]
        )

        user_groups = Group.objects.filter(id__in=serializer.validated_data["groups"])
        user.groups.set(user_groups)
        user.save()

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=HTTP_201_CREATED)


class UpdateUserGroupsView(APIView):
    class InputSerializer(serializers.Serializer):
        groups = serializers.ListField(
            child=serializers.IntegerField(),
            write_only=True,
            min_length=1,
            help_text="List of group IDs to assign to the user.",
        )

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_groups = Group.objects.filter(id__in=serializer.validated_data["groups"])

        if user_groups.count() != len(serializer.validated_data["groups"]):
            return Response(
                {"error": "One or more group IDs are invalid."},
                status=400
            )

        user = get_object_or_404(User, id=kwargs.get("pk"))
        user.groups.set(user_groups)
        user.save()

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=HTTP_200_OK)


class GetMeOrdersView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (
            Order.objects.filter(
                agent=self.request.user,
                status__in=[Order.Status.TAKE, Order.Status.CALL_AGAIN, Order.Status.PENDING],
            )
            .select_related("agent", "order_item__product")
            .prefetch_related(
                Prefetch("customer", queryset=self.get_customer_queryset())
            )
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


class GroupsListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


