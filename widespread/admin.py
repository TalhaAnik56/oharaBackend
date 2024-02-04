from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    list_select_related = ["customer", "seller"]

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_customer",
        "is_seller",
    )

    def is_customer(self, user):
        # hasattr method is checking that in the user object is there any attribute named "customer", if there is it will return true,otherwise false
        if hasattr(user, "customer"):
            icon = format_html(
                '<img src="/static/admin/img/icon-yes.svg" alt="Yes" width="16" height="16">'
            )
            return icon
        else:
            icon = format_html(
                '<img src="/static/admin/img/icon-no.svg" alt="No" width="16" height="16">'
            )
            return icon

    def is_seller(self, user):
        # #hasattr method is checking that in the user object is there any attribute named "seller", if there is it will return true,otherwise false
        if hasattr(user, "seller"):
            icon = format_html(
                '<img src="/static/admin/img/icon-yes.svg" alt="Yes" width="16" height="16">'
            )
            return icon
        else:
            icon = format_html(
                '<img src="/static/admin/img/icon-no.svg" alt="No" width="16" height="16">'
            )
            return icon
