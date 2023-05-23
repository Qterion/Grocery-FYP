from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import NewUserForm, CustomUserChangeForm
class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",'gluten_trigger','lactose_trigger','nut_trigger')
    list_filter = ("email", "is_staff", "is_active",'gluten_trigger','lactose_trigger','nut_trigger')
    fieldsets = (
        (None, {"fields": ("email", "password",'username','gluten_trigger','lactose_trigger','nut_trigger')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active",'gluten_trigger','lactose_trigger','nut_trigger', "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
admin.site.register(CustomUser,CustomUserAdmin)