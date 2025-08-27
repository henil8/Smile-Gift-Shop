from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = UserModel
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser", "role")
    search_fields = ("email", "first_name", "last_name", "mobile_no")
    ordering = ("email",)

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


# ----------------------
# Other Models
# ----------------------
@admin.register(RoleModel)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CountryModel)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("country_name", "country_code", "currency", "calling_code")
    search_fields = ("country_name", "country_code")


@admin.register(CountryGroupModel)
class CountryGroupAdmin(admin.ModelAdmin):
    list_display = ("group_name",)
    filter_horizontal = ("countries",)


@admin.register(StatesModel)
class StatesAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name",)
    list_filter = ("country",)


@admin.register(CitiesModel)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country", "is_active")
    list_filter = ("is_active", "country", "state")
    search_fields = ("name",)


@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "address_tags", "city", "state", "country", "is_default")
    search_fields = ("full_name", "address_line_1", "address_line_2", "landmark")
    list_filter = ("is_default", "country", "state", "city")


# Finally register UserModel with custom admin
admin.site.register(UserModel, UserAdmin)