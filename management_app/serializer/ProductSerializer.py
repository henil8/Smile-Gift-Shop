from rest_framework import serializers
from ..models import *
import slugify,json


class PropertyImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImageModel
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()

    
    def get_category(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()]) if obj.category.exists() else ""

    def get_sub_category(self, obj):
        return ", ".join([sub.name for sub in obj.sub_category.all()]) if obj.sub_category.exists() else ""
    
    
    class Meta:
        model = ProductModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # images = PropertyImageSerializer(many=True,read_only=True)
    # remove_image_ids = serializers.CharField(write_only=True, required=False)
    brand_name = serializers.CharField(source='brand.name',read_only=True)
    category = serializers.CharField(write_only=True)
    sub_category = serializers.CharField(write_only=True)


    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        # images = validated_data.pop('images',None)

        categories = validated_data.pop('category', [])
        print(categories)
        subcategories = validated_data.pop('sub_category', [])
        
        if isinstance(categories, str):
            categories = json.loads(categories)   # e.g. "[20,22]" → [20,22]
        if isinstance(subcategories, str):
            subcategories = json.loads(subcategories)

        instance = super().create(validated_data)

        instance.category.set(categories)
        instance.sub_category.set(subcategories)
        

        if images:
            for image in images:
              ProductImageModel.objects.create(product=instance,image=image)

        return instance
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        remove_image_ids =request.data.get('remove_image_ids', '[]')
        # images = validated_data.pop('images',None)
        # remove_image_ids = validated_data.pop('remove_image_ids', '[]')

        categories = validated_data.pop('category', None)
        subcategories = validated_data.pop('sub_category', None)

        instance = super().update(instance,validated_data)

        if categories is not None:
            instance.category.set(categories)
        
        if subcategories is not None:
            instance.sub_category.set(subcategories)


        if images:
            for image in images:
                ProductImageModel.objects.create(product=instance, image=image)
        
        if remove_image_ids:
            if isinstance(remove_image_ids,str):
                remove_image_ids = json.loads(remove_image_ids)

            for img_id in remove_image_ids:
               ProductImageModel.objects.filter(id=img_id, product=instance).delete()


        return instance

        

    class Meta:
        model = ProductModel
        fields = '__all__'

class CartProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'name')
    gst_percentage = serializers.IntegerField(source='gst')
    end_use_sales_discount = serializers.IntegerField(source='sales_discount')
    limited_stock_status = serializers.CharField(source='limited_stock')
    out_of_stock_status = serializers.CharField(source='out_of_stock')
    super_distributor_rate =serializers.DecimalField(source='super_distributer_price',max_digits=10,   decimal_places=2)

    class Meta:
        model = ProductModel
        fields = ['id','category_id','product_name','distributer_price','retailer_price','product_price','description','brand_id','item_code','group','color','company_code','unit','hsn_code','upc_barcode','lan_barcode','super_distributor_rate','gst_percentage','end_use_sales_discount','warranty','feature','weight','document','web_link','video_link','short_name','limited_stock_status','out_of_stock_status','created_at','updated_at']