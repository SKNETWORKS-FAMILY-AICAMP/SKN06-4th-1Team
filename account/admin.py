from re import U
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ["username", "name", "state"]
    # 사용자 추가
    add_fieldsets = (
        ("인증정보", {"fields": ("username", "password1", "password2")}),
        ("개인정보", {"fields": ("name", "state", "birthday", "profile_img")}),
        ("권한", {"fields": ("is_staff", "is_superuser")}),
    )
    # 사용자 변경
    fieldsets = (
        ("인증정보", {"fields": ("username", "password")}),
        ("개인정보", {"fields": ("name", "state", "birthday", "profile_img")}),
        ("권한", {"fields": ("is_staff", "is_superuser")}),
    )


admin.site.register(User, CustomUserAdmin)
