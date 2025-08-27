from rest_framework import serializers
from ..models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel
        fields = ('id','name','image')

    def create(self, validated_data):
        return CategoryModel.add_root(**validated_data)
    


class SubCategorySerializer(serializers.ModelSerializer):
    main_category = serializers.SerializerMethodField()
    parent_id = serializers.IntegerField(write_only=True)

    def get_main_category(self,obj):
        if obj.get_parent():
            return obj.get_parent().name
        else:
            return ''
    
    def create(self, validated_data):
        parent_id = validated_data.pop('parent_id',None)
        if not parent_id:
            raise serializers.ValidationError({"parent_id": "This field is required."})
        try:
            parent = CategoryModel.objects.get(id=parent_id)
        except CategoryModel.DoesNotExist:
            raise serializers.ValidationError({"parent_id": "Parent category not found."})
        
        return parent.add_child(**validated_data)

    def update(self, instance, validated_data):
        parent_id = validated_data.pop('parent_id',None)
        if not parent_id:
            raise serializers.ValidationError({'parent_id':'This field is required'})   
        try:
            parent = CategoryModel.objects.get(id=parent_id)
        except CategoryModel.DoesNotExist:
            raise serializers.ValidationError({'parent_id': 'Parent category not found.'})
        

        for attr,val in validated_data.items():
            setattr(instance,attr,val)

        if instance.get_parent() != parent:
           instance.move(parent,'last-child')

        
        instance.save()
        
        return instance

    class Meta:
        model = CategoryModel
        fields = ('id','name','main_category','image','full_path','parent_id')