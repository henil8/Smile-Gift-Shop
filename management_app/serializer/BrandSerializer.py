from rest_framework import serializers
from ..models import *


class BrandSerializer(serializers.ModelSerializer):
    brand_name=serializers.CharField(source="name")
    brand_image=serializers.SerializerMethodField()
    description=serializers.CharField()
    brand_display_number=serializers.IntegerField(source="number")

    class Meta:
        model = BrandModel
        fields = (
            'id',
            'brand_name',
            'brand_image',
            'description',
            'brand_display_number', 
        )

    def get_brand_image(self,obj):
        return obj.image.name if obj.image else None
    
   

    