        
from rest_framework import serializers
from ..models import InquiryModel, ProductModel
from user_app.models import UserModel

class InquirySerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    users_id=serializers.IntegerField(source="user.id",read_only=True)
    products_id = serializers.IntegerField(source="product_name.id", read_only=True)


    qty = serializers.IntegerField(source="quantity")
    product_name = serializers.CharField(source=" product_name.name", read_only=True)

    class Meta:
        model = InquiryModel
        fields = (
            "id",
            "user_id",
            "users_id",
            "product_id",
            "products_id",
            "qty",
            "product_name",
            "description",
            "status",
            "created_at",
            "updated_at",
            "deleted_at",
        
        )
        read_only_fields = ["users_id", "products_id"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        product_id = validated_data.pop("product_id")
            
        user = UserModel.objects.get(id=user_id)
        product = ProductModel.objects.get(id=product_id)
        
        inquiry = InquiryModel.objects.create(
       
            name = user,
            user = user,
            product_name=product,
          
            **validated_data
        )
        return inquiry

    