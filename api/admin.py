from django.contrib import admin
from .models import TestResult


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'entry_method', 'created_at')
    list_filter = ('entry_method', 'result', 'created_at')
    search_fields = ('user__username', 'result')
    ordering = ('-created_at',)
