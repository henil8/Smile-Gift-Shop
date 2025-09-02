from rest_framework import serializers
from ..models import *
from management_app.serializer.ProductSerializer import CartProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id", "user_id", "product_id", "brand_id",
            "qty", "price", "status",
            "total_price", "created_at", "updated_at","product"
        ]
        read_only_fields = ["price", "created_at", "updated_at", "total_price"]