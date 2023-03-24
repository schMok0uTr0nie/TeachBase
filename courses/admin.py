from django.contrib import admin
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner_name', 'created_at', 'total_score', 'total_tasks',
                    'content_type', 'is_netology', 'duration')
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'owner_name',)
    list_filter = ('owner_name', 'content_type', 'is_netology', )


admin.site.register(Course, CourseAdmin)
