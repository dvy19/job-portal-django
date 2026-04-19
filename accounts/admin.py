from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RecruiterProfile

from .models import Skill

admin.site.register(Skill)

class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = ("email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)

    # Important: define readonly_fields if needed
    readonly_fields = ()

    fieldsets = (
        ("Login Info", {"fields": ("email", "password")}),
        ("Role", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )


# Optional: Improve RecruiterProfile admin view
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("id","full_name", "company_name", "user","position","city","state")  # adjust fields as per your model
    search_fields = ("user__email", "company_name")


# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin)