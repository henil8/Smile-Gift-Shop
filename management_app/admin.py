from django.contrib import admin
from .models import *
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.utils.html import format_html
# Register your models here.


@admin.register(CategoryTagsModel)
class CategoryTagsAdmin(admin.ModelAdmin,):
    list_display = ("name",)
    search_fields = ("name",)



class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(CategoryModel)
    list_display = ("name", "sequence", "is_active", "category_tags", "full_pathtext")
    list_filter = ("is_active", "category_tags")
    search_fields = ("name", "full_pathtext")
    ordering = ("sequence",)

admin.site.register(CategoryModel,CategoryAdmin)


# -------------------------
# Brand + Product
# -------------------------
@admin.register(BrandModel)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "number")
    search_fields = ("name",)


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image','image_preview']

    def image_preview(self,obj):
        if obj.image:
             return format_html('<img src="{}" width="100" height="75" style="object-fit:cover; border-radius:4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'image']
    readonly_fields = ['thumbnail_preview']
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit:cover; border-radius:4px;" />', obj.image.url)
        return "-"
    thumbnail_preview.short_description = 'Preview'

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "short_name", "product_price", "brand", "is_published", "is_archived")
    list_filter = ("brand", "category", "is_published", "is_archived", "product_use_type", "product_type")
    search_fields = ("name", "short_name", "item_code", "company_code", "hsn_code")
    inlines = [ProductImageInline]
    ordering = ("-created_at",)
    filter_horizontal = ("product_tag","category","sub_category")


# -------------------------
# News + Business Category
# -------------------------
@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "role")
    search_fields = ("title",)
    list_filter = ("role",)


@admin.register(BusinessCategoryModel)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# -------------------------
# Inquiry + Feedback + Help
# -------------------------
@admin.register(InquiryModel)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "product_name", "quantity", "status")
    list_filter = ("status",)
    search_fields = ("name__email", "product_name__name")


@admin.register(FeedbackModel)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("title", "email")
    search_fields = ("title", "email")


@admin.register(HelpAndSupportModel)
class HelpAndSupportAdmin(admin.ModelAdmin):
    list_display = ("title", "email")
    search_fields = ("title", "email")


# -------------------------
# Firm + Third Party
# -------------------------
@admin.register(FirmModel)
class FirmAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__email")


@admin.register(ThirdPartyModel)
class ThirdPartyAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__email")


# -------------------------
# Orders + Order Lines
# -------------------------
class OrderLinesInline(admin.TabularInline):
    model = OrderLinesModel
    extra = 1


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer", "order_status", "final_total", "is_paid", "created_at")
    list_filter = ("order_status", "is_paid", "is_expired", "is_gift", "is_ecommerce")
    search_fields = ("order_id", "customer__email")
    ordering = ("-created_at",)
    inlines = [OrderLinesInline]


@admin.register(OrderLinesModel)
class OrderLinesAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "selling_price", "product_total")
    search_fields = ("order__order_id", "product__name")


from django.contrib import admin
from .models import LocationModel, SerialNumbersModel, Inventory


@admin.register(LocationModel)
class LocationModelAdmin(admin.ModelAdmin):
    list_display = (
        "id", "location_name", "location_type", "parent_location",
        "is_a_scrap_location", "is_a_return_location", "barcode"
    )
    list_filter = ("location_type", "is_a_scrap_location", "is_a_return_location")
    search_fields = ("location_name", "barcode")
    ordering = ("location_name",)


@admin.register(SerialNumbersModel)
class SerialNumbersModelAdmin(admin.ModelAdmin):
    list_display = (
        "id", "serial_no", "product", "created_on",
        "best_before_date", "removal_date", "end_of_life",
        "alert_time", "is_repacked"
    )
    list_filter = ("is_repacked", "created_on", "best_before_date", "removal_date")
    search_fields = ("serial_no", "product__name")
    ordering = ("-created_on",)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "product", "location_stock",
        "formatted_quantity", "formatted_counted_quantity",
        "formatted_reserved_quantity", "value", "measure", "created_at"
    )
    list_filter = ("created_at", "location_stock", "product")
    search_fields = ("product__name", "location_stock__location_name")
    ordering = ("-created_at",)
    readonly_fields = ("value", "measure", "difference")


@admin.register(KYCDetailsModel)
class KYCDetailsAdmin(admin.ModelAdmin):
    list_display = ("firm_name", "business_category", "gstin_no", "pancard_no", "sez_company", "csc_funding_company")
    search_fields = ("firm_name", "gstin_no", "pancard_no", "cin_no")
    list_filter = ("business_category", "sez_company", "csc_funding_company")


@admin.register(BankDetailsModel)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "account_number", "ifsc_code", "account_holder_name", "kyc_detail")
    search_fields = ("bank_name", "account_number", "ifsc_code")
    list_filter = ("bank_name",)


@admin.register(FavouriteModel)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("user_id", "product_id", "status", "created_at", "updated_at", "deleted_at")
    search_fields = ("user_id", "product_id", "created_at")
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
            "id","user","product","brand","qty","price","total_price","status","created_at","updated_at",
        )
    list_filter = ("status", "created_at", "updated_at", "brand")
    search_fields = ("user__email", "user__first_name", "user__last_name", "product__name", "brand__name")
    ordering = ("-created_at",)

    def total_price(self, obj):
            return obj.total_price
