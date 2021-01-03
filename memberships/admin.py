from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "preferred_name", "user_email")
    readonly_fields = ("user",)

    def user_email(self, obj):
        return obj.user

    # Membership registration should be done
    # via the custom member registration form.
    def has_add_permission(self, request):
        return False


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")
