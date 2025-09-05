from rest_framework import serializers
from ..models import *

class OfferSerializer(serializers.ModelSerializer):
    
    offer_slider_image=serializers.ImageField(source="image")
    slider_number = serializers.IntegerField(source="banner_number")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
 
    class Meta:
        model = OfferSliderModel
        fields =(
            'id',
            'offer_slider_image',
            'slider_number',
            'created_at',
            'updated_at',
            'deleted_at',
        )
    
    # def get_offer_slider_image(self, obj):
    #     return obj.image.name if obj.image else None
