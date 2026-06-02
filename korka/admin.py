from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'course_name',
        'user',
        'status',
        'created_at',
    )

    list_filter = ('status',)

    search_fields = (
        'course_name',
        'user__username',
    )

    list_editable = ('status',)

    readonly_fields = ('created_at',)

    fields = (
        'user',
        'course_name',
        'start_date',
        'payment_method',
        'status',
        'feedback',
        'created_at',
    )