from django.contrib import admin
from .models import Student, UserProfile, CustomUser


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]
    ordering = ["last_name"]
    search_fields = ["email__startswith"]
    list_filter = ["birthdate"]
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("email", "phone_number"),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "course"]
    ordering = ["type"]
    search_fields = ["user__icontains"]
    list_filter = ["type"]
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "user",
                    "type",
                )
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("phone", "birthdate", "course"),
            },
        ),
    )


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]
    ordering = ["first_name"]
    search_fields = ["email__icontains"]
    list_filter = ["first_name"]
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("date_joined", "is_staff", "is_active"),
            },
        ),
    )
