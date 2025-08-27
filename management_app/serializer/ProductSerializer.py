from rest_framework import serializers
from ..models import *



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = '__all__'