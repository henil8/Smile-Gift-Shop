from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from phonenumber_field.phonenumber import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from phonenumber_field.phonenumber import to_python

class ProfileSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(source="mobile_no")
    class Meta:
        model = ProfileModel
        fields = [
            "id", "contact","profile_pic", "addresses", "otp", "otp_requested_at","os_type",
        ]

class AddressSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(source='mobile')
    
    class Meta:
        model = AddressModel
        fields = ["id","full_name","street","city","state","pincode","contact","address"]

    def update(self, instance, validated_data):
        mobile = validated_data.pop('mobile', '')
        if mobile:
            instance.mobile = mobile
            instance.save()       
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source="date_joined", read_only=True)
    contact = serializers.CharField(source="mobile_no")
    firebase_token = serializers.CharField(source="token")

    profile_image = serializers.ImageField(source="profilemodel.profile_pic",required=False, allow_null=True)
    otp = serializers.CharField(source="profilemodel.otp", read_only=True)
    os_type = serializers.CharField(source="profilemodel.os_type", read_only=True)

    address = serializers.CharField(source="address.first.address", read_only=True)
    pincode = serializers.CharField(source="address.first.pincode", read_only=True)

    # addresses = AddressSerializer(many=True)
    class Meta:
        model = UserModel
        fields = ["id","first_name", "last_name","email", "contact","address","pincode","profile_image","otp","os_type", "is_active","created_at","firebase_token"]

    def create(self, validated_data):
        validated_data["is_active"] = True  # force is_active=True
        return super().create(validated_data)
    
    def update(self, instance, validated_data):

        profile_data = validated_data.pop("profilemodel", {})

        instance = super().update(instance, validated_data)

        profile = getattr(instance, "profilemodel", None)
        if profile and "profile_pic" in profile_data:
            profile.profile_pic = profile_data["profile_pic"]
            profile.save()

        return instance
    
class CountriesSerializer(serializers.ModelSerializer):

    all_state = serializers.SerializerMethodField(read_only=True)

    def get_all_state(self, obj):
        get_all_country = StatesModel.objects.filter(country=obj).values()
        return get_all_country

    class Meta:
        model = CountryModel
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField(read_only=True)
    all_cities = serializers.SerializerMethodField(read_only=True)

    def get_all_cities(self, obj):
        get_all_cities = CitiesModel.objects.filter(state=obj).values()
        return get_all_cities

    def get_country_name(self, obj):
        return obj.country.country_name

    class Meta:
        model = StatesModel
        fields = '__all__'


class CitiesSerializer(serializers.ModelSerializer):
    state_name = serializers.SerializerMethodField(read_only=True)
    country_name = serializers.SerializerMethodField(read_only=True)

    def get_state_name(self, obj):
        return obj.state.name

    def get_country_name(self, obj):
        return obj.country.country_name


    class Meta:
        model = CitiesModel
        fields = '__all__'
