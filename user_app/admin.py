from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = UserModel
    list_display = ("mobile_no","email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser", "role")
    search_fields = ("email", "first_name", "last_name", "mobile_no")
    ordering = ("email",)
    filter_horizontal = ("address",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "mobile_no", "address")}),
        ("Role & Status", {"fields": ("role", "approved_status")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )
    
@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile_no", "otp", "otp_requested_at")
    search_fields = ("user__email", "mobile_no")
    list_filter = ("otp_requested_at",)

# ----------------------
# Other Models
# ----------------------
@admin.register(RoleModel)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CountryModel)
class CountryAdmin(ImportExportModelAdmin):
    list_display = ("country_name", "country_code", "currency", "calling_code")
    search_fields = ("country_name", "country_code")


@admin.register(CountryGroupModel)
class CountryGroupAdmin(admin.ModelAdmin):
    list_display = ("group_name",)
    filter_horizontal = ("countries",)


@admin.register(StatesModel)
class StatesAdmin(ImportExportModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name",)
    list_filter = ("country",)


@admin.register(CitiesModel)
class CitiesAdmin(ImportExportModelAdmin):
    list_display = ("name", "state", "country", "is_active")
    list_filter = ("is_active", "country", "state")
    search_fields = ("name",)


@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "address_tags", "city", "state", "country","pincode", "is_default")
    search_fields = ("full_name", "street", "address", "landmark")
    list_filter = ("is_default", "country", "state", "city")


# Finally register UserModel with custom admin
admin.site.register(UserModel, UserAdmin)