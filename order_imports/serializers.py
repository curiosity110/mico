import logging

import magic
from rest_framework import serializers

from accounts.serializers import UserSerializer
from order_imports.mime_types import MimeTypes
from order_imports.models import OrderImport
from orders.serializer import OrderSerializer

logger = logging.getLogger(__file__)


class XlsxOrderImportSerializer(serializers.Serializer):
    file = serializers.FileField(
        help_text="Upload an XLSX file containing order data."
    )

    def validate_file(self, value):
        if not value.name.lower().endswith('.xlsx'):
            raise serializers.ValidationError("File must have a .xlsx extension.")

        mime_type = magic.from_buffer(value.read(1024), mime=True)
        value.seek(0)

        if mime_type not in [MimeTypes.XLSX.value, MimeTypes.OCTET_STREAM.value]:
            logger.error(
                f"Invalid file type: {mime_type}. Expected: {MimeTypes.XLSX.value}"
            )
            raise serializers.ValidationError("Uploaded file must be a valid XLSX file.")

        return value


class OrderImportListSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    orders_count = serializers.SerializerMethodField()
    agent = UserSerializer(read_only=True)

    class Meta:
        model = OrderImport
        fields = '__all__'

    def get_file_name(self, obj):
        return obj.file.name if obj.file else None

    def get_orders_count(self, obj):
        return obj.orders.count()


class OrderImportDetailSerializer(OrderImportListSerializer):
    orders = OrderSerializer(many=True, read_only=True)