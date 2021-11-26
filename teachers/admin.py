from django.contrib import admin
from .models import Teacher


# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "course_count"]
    ordering = ["last_name"]
    search_fields = ["email__startswith"]

    def course_count(self, obj):
        courses = 0
        if obj.course:
            courses = obj.course.all().count()
        return courses
