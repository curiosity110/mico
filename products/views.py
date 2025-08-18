from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        sale_price = serializers.FloatField()
        stock_price = serializers.FloatField()
        stock = serializers.IntegerField()

    def create(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = Product.objects.create(**input_serializer.validated_data)
        output_serializer = ProductSerializer(product)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ProductRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        sale_price = serializers.FloatField(required=False)
        stock_price = serializers.FloatField(required=False)
        stock = serializers.IntegerField(required=False)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for attr, value in serializer.validated_data.items():
            setattr(product, attr, value)
        product.save()

        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
