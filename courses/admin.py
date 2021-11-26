from django.contrib import admin
from courses.models import Course


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "start_date"]
    ordering = ["id"]
    search_fields = ["name"]
