from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    list_display  = ["email", "role", "is_active", "is_staff"]
    list_filter   = ["role", "is_active", "is_staff"]
    search_fields = ["email"]
    ordering      = ["email"]

    fieldsets = (
        ("Login Info",  {"fields": ("email", "password")}),
        ("Role",        {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields":  ("email", "password1", "password2", "role"),
        }),
    )


# This is the line that registers your model with the admin panel
admin.site.register(CustomUser, CustomUserAdmin)