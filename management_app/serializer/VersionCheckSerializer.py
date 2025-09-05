        
from rest_framework import serializers
from ..models import VersionModel

class VesioncheckSerializer(serializers.ModelSerializer):
    
    android = serializers.CharField(source="android_version")
    ios = serializers.CharField(source="ios_version")
    
    class Meta:
        model = VersionModel
        fields = (
            'android_id',
            'ios_id',
            'android',
            'ios',
            'android_description',
            'ios_description',
            'android_status',
            'ios_status',
            "created_at",
            "updated_at",
            "deleted_at",
        )
    
    # android_id=serializers.IntegerField(source='android_id')
    # android_version=serializers.CharField(source='android_version')
    # android_description= serializers.CharField(source='android_description')
    # android_status=serializers.CharField(source='android_status')
    
    # ios_id=serializers.IntegerField(source='ios_id')
    # ios_version=serializers.CharField(source='ios_version')
    # ios_description= serializers.CharField(source='ios_description')
    # ios_status=serializers.CharField(source='ios_status')
    
  