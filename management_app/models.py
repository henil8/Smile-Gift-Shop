from django.db import models
from django.core.validators import (MaxLengthValidator, MinValueValidator, MaxValueValidator)
from django.db import models
from treebeard.mp_tree import MP_Node
from phonenumber_field.modelfields import PhoneNumberField
from tinymce_4.fields import TinyMCEModelField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import base64
from user_app.models import UserModel
# Create your models here.

class CategoryTagsModel(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    class Meta:
        indexes = [
            models.Index(fields=['name'], name='idx_categorytag_name'),
        ]


class CategoryModel(MP_Node):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="Categories", blank=True, null=True)
    sub_category_image = models.ImageField(upload_to='Sub Categories',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    sequence = models.IntegerField(unique=True , blank=True, null=True)
    full_pathtext = models.TextField(blank=True, null=True)
    category_tags = models.ForeignKey(CategoryTagsModel, on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def full_path(self):
        ancestors_names = [ancestor.name for ancestor in self.get_ancestors()]
        self.full_pathtext = " / ".join([*ancestors_names, self.name])
        # self.save(update_fields=['full_pathtext'])        
        return " / ".join([*ancestors_names, self.name])


    @property
    def ancestor_names(self):
        return [ancestor.name for ancestor in self.get_ancestors()]
    

    def __str__(self):
        return f"{self.name} | {self.id}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['name'], name='idx_category_name'),
            models.Index(fields=['image'], name='idx_category_image'),
            models.Index(fields=['sequence'], name='idx_category_sequence'),
            models.Index(fields=['is_active'], name='idx_category_is_active'),
            models.Index(fields=['full_pathtext'], name='idx_category_full_pathtext'),
        ]


 
class BrandModel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True)
    number = models.IntegerField(null=True,blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        indexes = [
            models.Index(fields=['name'], name='idx_Brand_name'),
        ]

class ProductTag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'], name='idx_producttag_name'),
        ]

class ProductModel(models.Model):
    PRODUCT_USE_TYPE_CHOICES = (('Consumable', 'Consumable'),
                                ('Service', 'Service'), ('Storable Product', 'Storable Product'), ('Voucher', 'Voucher'))
    PRODUCT_TYPE_CHOICES = (
        ('Single Product', 'Single Product'), ('Kit', 'Kit'))
 
    
    UNIT_CHOICES  = [
        ("pcs", "Piece"),
        ("set", "Set"),
        ("pair", "Pair"),
        ("box", "Box"),
        ("pack", "Pack"),
        ("dozen", "Dozen"),
        ("bundle", "Bundle"),
        ("roll", "Roll"),
        ("sheet", "Sheet"),
        ("book", "Book"),
        ("card", "Card"),
        ("bottle", "Bottle"),
        ("jar", "Jar"),
    ]
 
 
    category = models.ManyToManyField(CategoryModel, blank=True , related_name='product_single_category')
    sub_category = models.ManyToManyField(CategoryModel, blank=True , related_name='product_sub_category')
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=100,choices=UNIT_CHOICES)
    short_name = models.CharField(max_length=255)
    product_price = models.DecimalField(
        default=0, verbose_name="MRP Rate(Product Price)", decimal_places=2, max_digits=10)
    image1 = models.ImageField(upload_to="Products", default="Products/product.png")
    item_code = models.CharField(max_length=100)
    group = models.CharField(max_length=100,null=True,blank=True)
    model = models.CharField(max_length=100,null=True,blank=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    company_code = models.CharField(max_length=100,null=True,blank=True)
    upc_barcode = models.CharField(
        max_length=13, blank=True, null=True, validators=[MaxLengthValidator(13)])
    lan_barcode = models.CharField(
        max_length=13, blank=True, null=True, validators=[MaxLengthValidator(13)])
    retailer_price = models.DecimalField(
        default=0, verbose_name="Retailer Price", decimal_places=2, max_digits=10,null=True,blank=True)
    distributer_price = models.DecimalField(
        default=0, verbose_name="Distributer Price", decimal_places=2, max_digits=10,null=True,blank=True)
    super_distributer_price = models.DecimalField(
        default=0, verbose_name="Super Distributer Price", decimal_places=2, max_digits=10,null=True,blank=True)
    gst = models.FloatField(
        default=0, blank=True, null=True)
    sales_discount =models.FloatField(
        default=0, blank=True, null=True)
    warranty = models.CharField(max_length=10)
    weight = models.FloatField(
        default=0, verbose_name='net weight (in gms)')
    web_link = models.URLField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    feature = models.CharField(max_length=100, blank=True, null=True)
    description = TinyMCEModelField(null=True, blank=True)
    limited_stock = models.CharField(max_length=10,choices=[
        ("Yes", "Yes"),
        ("No", "No"),])
    out_of_stock = models.CharField(max_length=10,choices=[
        ("Yes", "Yes"),
        ("No", "No"),])
    document = models.FileField(upload_to='Documents',null=True,blank=True)
    cost = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    image2 = models.ImageField(upload_to="Products", null=True, blank=True)
    image3 = models.ImageField(upload_to="Products", null=True, blank=True)
    image4 = models.ImageField(upload_to="Products", null=True, blank=True)
    image5 = models.ImageField(upload_to="Products", null=True, blank=True)
    product_use_type = models.CharField(
        max_length=255, choices=PRODUCT_USE_TYPE_CHOICES, default='')
    product_type = models.CharField(
        max_length=255, choices=PRODUCT_TYPE_CHOICES, default='')
    brand = models.ForeignKey(
        BrandModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    notes = models.TextField(
        help_text='Notes for internal purposes', null=True, blank=True)
    barcode_image = models.ImageField(
        upload_to='Barcodes', blank=True, null=True)
    can_be_sold = models.BooleanField(default=True)
    can_be_purchased = models.BooleanField(default=True)
    hsn_code = models.CharField(max_length=255, null=True, blank=True)
    is_tracking  = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    product_tag = models.ManyToManyField(ProductTag, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(blank=True, null=True)

    @property
    def encrypted_id(self):
        if self.id is None:
            return None
        return base64.urlsafe_b64encode(str(self.id).encode()).decode()

    @property
    def decrypted_id(self):
        if self.encrypted_id is None:
            return None
        return int(base64.urlsafe_b64decode(self.encrypted_id.encode()).decode())
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        indexes = [
            models.Index(fields=['name'], name='idx_name'),
            models.Index(fields=['short_name'], name='idx_short_name'),
            models.Index(fields=['product_price'], name='idx_product_price'),
            models.Index(fields=['product_type'], name='idx_product_type'),
            models.Index(fields=['is_archived'], name='idx_is_archived'),
            models.Index(fields=['is_published'], name='idx_is_published'),
            models.Index(fields=['brand'], name='idx_brand'),
            models.Index(fields=['product_use_type'], name='idx_product_use_type'),
            models.Index(fields=['created_at'], name='idx_product_created_at'),
            models.Index(fields=['is_tracking'], name='idx_product_is_tracking'),
            models.Index(fields=['hsn_code'], name='idx_hsn_code'),
            models.Index(fields=['weight'], name='idx_weight'),
        ]

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to="Products")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['product__created_at']

    def __str__(self):
        return f"Image for {self.product.name}"
  
class NewsModel(models.Model):
   title = models.CharField(max_length=100)
   image = models.ImageField(null=True,blank=True)
   description = TinyMCEModelField(null=True, blank=True)
   role = models.ForeignKey('user_app.RoleModel',on_delete=models.CASCADE,null=True,blank=True)

   class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["role"]),
        ]


class BusinessCategoryModel(models.Model):
    name= models.CharField(max_length=100)

    class Meta:
        verbose_name = "Business Category"
        verbose_name_plural = "Business Categories"
        indexes = [
            models.Index(fields=["name"]),
        ]

class InquiryModel(models.Model):
    name = models.ForeignKey('user_app.UserModel',on_delete=models.CASCADE)
    product_name = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = TinyMCEModelField(null=True, blank=True)
    status = models.CharField(max_length=30,choices=[
        ("Pending", "Pending"),
        ("Complete", "Complete")])
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='user')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["name", "status"]),  # useful for filtering user inquiries by status
            models.Index(fields=["product_name"]),
        ]


class FeedbackModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    title = models.CharField(max_length=200)
    description = TinyMCEModelField(null=True, blank=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.email}"


class HelpAndSupportModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=200)
    description = TinyMCEModelField(null=True, blank=True)

    class Meta:
        verbose_name = "Help & Support"
        verbose_name_plural = "Help & Support"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.email}"
    

class FirmModel(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey('user_app.UserModel',on_delete=models.CASCADE)

class ThirdPartyModel(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey('user_app.UserModel',on_delete=models.CASCADE)



class OrderModel(models.Model):
    ORDER_STATUS = (('Pending', 'Pending'), ('Out for Delivery',
                    'Out for Delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'))
    PAYMENT_TYPE_CHOICES = (
        ('Cash on Delivery', 'Cash on Delivery'), ('Online Payment', 'Online Payment'))

    class SALES_STATUS_CHOICES(models.TextChoices):
        quotation = ('Quotation', 'Quotation')
        quotation_sent = ('Quotation Sent', 'Quotation Sent')
        sales_order = ('Sales Order', 'Sales Order')
        cancel_order = ('Cancelled', 'Cancelled')
    
    customer = models.ForeignKey('user_app.UserModel', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    firm_name = models.ForeignKey(FirmModel,on_delete=models.SET_NULL,blank=True,null=True)
    third_party_order = models.ForeignKey(ThirdPartyModel,on_delete=models.SET_NULL,blank=True,null=True)
    product_info = models.JSONField(blank=True, null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    order_status = models.CharField(choices=ORDER_STATUS, default='Pending', max_length=100)
    pay_type = models.CharField(max_length=200, choices=PAYMENT_TYPE_CHOICES, blank=True, null=True)
    sale_status = models.CharField(max_length=255, choices=SALES_STATUS_CHOICES.choices, default=SALES_STATUS_CHOICES.quotation)
    product_total = models.FloatField(default=0.00)       
    discount_amt = models.FloatField(default=0.00)
    tax_amt = models.FloatField(default=0.00)
    shipping_amt = models.PositiveIntegerField(default=0)
    final_total = models.FloatField(default=0.00)
    is_paid = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_gift = models.BooleanField(default=False, verbose_name="is a gift?")
    gift_message = models.TextField(blank=True, null=True, verbose_name="gift message")
    applied_voucher_code = models.CharField(max_length=25, blank=True, null=True)
    margin = models.IntegerField(default=0)
    is_ecommerce = models.BooleanField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    address = models.ForeignKey('user_app.AddressModel', on_delete= models.DO_NOTHING, blank=True,null=True)
    source_doc = models.CharField(max_length=255, blank=True, null=True)
    
    @property
    def total_order_qty(self):
        total_qt = 0
        for i in self.product_info:
            total_qt += i["quantity"]
        return total_qt


    def save(self, *args, **kwargs):
        if not self.order_id:
            if OrderModel.objects.count() >= 1:
                last_order_id = int(
                    OrderModel.objects.last().order_id.removeprefix('SO'))
            else:
                last_order_id = 0
            self.order_id = 'SGS' + str(last_order_id+1).zfill(8)

        super(OrderModel, self).save(*args, **kwargs)

    @property
    def untax_amount(self):
        l1 = []
        amount = 0
        for i in self.product_info:
            
            if "untax_amount" in i:
                amount = i["untax_amount"]
                amount = i["untax_amount"] * i["quantity"]
    
        l1.append(amount)
        return sum(l1)

    class Meta:
        indexes = [
            models.Index(fields=['order_id'], name='idx_order_reference'),
            models.Index(fields=['order_date'], name='idx_order_date'),
            models.Index(fields=['final_total'], name='idx_final_total'),
            models.Index(fields=['is_paid'], name='idx_is_paid'),
            models.Index(fields=['is_expired'], name='idx_is_expired'),
            models.Index(fields=['is_gift'], name='idx_is_gift'),
            models.Index(fields=['gift_message'], name='idx_gift_message'),
            models.Index(fields=['applied_voucher_code'], name='idx_applied_voucher_code'),
            models.Index(fields=['margin'], name='idx_margin'),
            models.Index(fields=['is_ecommerce'], name='idx_is_ecommerce'),
            models.Index(fields=['note'], name='idx_note'),
            models.Index(fields=['source_doc'], name='idx_source_doc'),
            models.Index(fields=['created_at'], name='idx_order_created_at'),
            models.Index(fields=['order_status'], name='idx_order_status'),
            models.Index(fields=['delivery_date'], name='idx_delivery_date'),
            models.Index(fields=['expiration_date'], name='idx_expiration_date'),
            models.Index(fields=['pay_type'], name='idx_pay_type'),  
        ]

    def __str__(self):
        return f"{self.order_id} - {self.customer}"
    

class OrderLinesModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.DO_NOTHING , blank=True , null=True , related_name='orderrelation')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING , blank=True , null=True)
    quantity = models.FloatField(default=0.00)
    selling_price = models.FloatField(default=0.00)

    tax_amount = models.FloatField(default=0.00)
    untax_amount = models.FloatField(default=0.00)
    product_total = models.FloatField(default=0.00)
    margin_amount = models.FloatField(default=0.00)
    after_margin_amount = models.FloatField(default=0.00)

class LocationModel(models.Model):
    class LocationTypeChoices(models.TextChoices):
        vendor_location = ('Vendor Location', 'Vendor Location')
        view = ('View', 'View')
        internal_location = ('Internal Location', 'Internal Location')
        customer_location = ('Customer Location', 'Customer Location')
        inventory_loss = ('Inventory Loss', 'Innventory Loss')
        production = ('Production', 'Production')
        transit_location = ('Transit Location', 'Transit Location')

    class RemovalStrategyChoices(models.TextChoices):
        FIFO = ('First In First Out (FIFO)', 'First In First Out (FIFO)')
        LIFO = ('Last In First Out (LIFO)', 'Last In First Out (LIFO)')
        FEFO = ('First Expiry First Out (FEFO)','First Expiry First Out (FEFO)')

    location_name = models.CharField(max_length=255)
    parent_location = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    location_type = models.CharField(max_length=255, choices=LocationTypeChoices.choices)
    is_a_scrap_location = models.BooleanField(default=False)
    is_a_return_location = models.BooleanField(default=False)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    removal_strategy = models.CharField(max_length=255, choices=RemovalStrategyChoices.choices, blank=True, null=True)
    external_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.location_name
    
    class Meta:
        indexes = [
        ]

class SerialNumbersModel(models.Model):
    serial_no = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True, null=True, related_name = 'serial')
    created_on = models.DateTimeField(default=timezone.now)
    best_before_date = models.DateTimeField(
        verbose_name="Best before Date", blank=True)
    removal_date = models.DateTimeField(
        verbose_name="Removal Date", blank=True)
    end_of_life = models.DateTimeField(
        verbose_name="End Of Life Date", blank=True)
    alert_time = models.DateTimeField(verbose_name="Alert Date", blank=True)
    is_repacked = models.BooleanField(default=False, verbose_name='Repacked')

    def __str__(self):
        return f"{self.serial_no} - {self.id}"
    
    class Meta:
        indexes = [
        ]



class Inventory(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    location_stock = models.ForeignKey(LocationModel, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0, verbose_name="On Hand Quantity")
    counted_quantity = models.FloatField(default=0.0)
    reserved_quantity = models.FloatField(default=0.0)
    serialno = models.ForeignKey(SerialNumbersModel, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def value(self):
        getproduct = ProductModel.objects.get(id=self.product.id)
        value = float(getproduct.cost) * self.quantity
        return round(value, 2)

    @property
    def measure(self):
        getproduct = ProductModel.objects.get(id=self.product.id)
        return getproduct.sales_measurement_unit

    @property
    def difference(self):
        difference = self.counted_quantity - self.quantity
        return difference



    def save(self, *args, **kwargs):
        # self.clean()
        if self._state.adding is True:
            # Get the last object to retrieve its ID
            last_object = Inventory.objects.latest('id')
            last_id = last_object.id
            # Increment the last ID to generate a new unique ID
            new_id = last_id + 1
            self.id = new_id

        self.quantity = round(self.quantity, 3)
        self.counted_quantity = round(self.counted_quantity, 3)
        self.reserved_quantity = round(self.reserved_quantity, 3)
        
        super(Inventory, self).save(*args, **kwargs) # Call the real save() method

    def __str__(self):
        return f"{self.product.name}-{self.id}"

    class Meta:
        indexes = [
            models.Index(fields=['created_at'], name='idx_inventory_created_at'),
            models.Index(fields=['product'], name='idx_inventory_product'),
            models.Index(fields=['location_stock'], name='idx_inventory_location'),
            models.Index(fields=['serialno'], name='idx_inventory_serialno'),
        ]
    
    def formatted_quantity(self):
        return f"{self.quantity:.3f}"
    formatted_quantity.short_description = 'On Hand Quantity'

    def formatted_counted_quantity(self):
        return f"{self.counted_quantity:.3f}"
    formatted_counted_quantity.short_description = 'Counted Quantity'

    def formatted_reserved_quantity(self):
        return f"{self.reserved_quantity:.3f}"
    formatted_reserved_quantity.short_description = 'Reserved Quantity'



class KYCDetailsModel(models.Model):
    firm_name = models.CharField(max_length=255)  # indexed
    incorporation_date = models.DateField(null=True, blank=True)
    business_category = models.ForeignKey(BusinessCategoryModel, on_delete=models.CASCADE,null=True, blank=True)
    company_logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)
    ho_address = models.TextField(null=True, blank=True)
    whatsapp_no = models.CharField(max_length=15, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    social_media_address = models.URLField(null=True, blank=True)
    pancard_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
    gstin_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
    tan_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
    cin_no = models.CharField(max_length=21, null=True, blank=True, unique=True)
    sez_company = models.CharField(max_length=255, null=True, blank=True)
    csc_funding_company = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['firm_name']),
            models.Index(fields=['business_category']),
            models.Index(fields=['gstin_no']),
        ]
        verbose_name = "KYC Detail"
        verbose_name_plural = "KYC Details"

    def __str__(self):
        return self.firm_name


class BankDetailsModel(models.Model):
    kyc_detail = models.ForeignKey(KYCDetailsModel, on_delete=models.CASCADE, related_name="bank_details")
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50, unique=True)
    ifsc_code = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    account_holder_name = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['bank_name']),
            models.Index(fields=['account_number']),
            models.Index(fields=['ifsc_code']),
        ]
        verbose_name = "Bank Detail"
        verbose_name_plural = "Bank Details"

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    
    
class VersionModel(models.Model):
    
    android_id=models.IntegerField()
    android_version = models.CharField(max_length=100)
    android_description =TinyMCEModelField(null=True,blank=True)
    android_status=models.CharField(max_length=30)
    
    ios_id=models.IntegerField()
    ios_version = models.CharField(max_length=100)
    ios_description =TinyMCEModelField(null=True,blank=True)
    ios_status=models.CharField(max_length=30)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.android_status

class OfferSliderModel(models.Model):
    """Slider banners"""
    image = models.ImageField(upload_to="offer_sliders/",null=True,blank=True)   # 1080x500 recommended
    banner_number = models.PositiveIntegerField()
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
 
    class Meta:
        ordering = ["banner_number"]  # always sorted by number
 
    def __str__(self):
        return f"Slider {self.banner_number}"
