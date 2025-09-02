from rest_framework import serializers
from ..models import *



class ProductSerializer(serializers.ModelSerializer):

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