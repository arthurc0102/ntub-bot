from django.contrib import admin

from .models import Log


@admin.register(Log)
class LogModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_at', 'checked')
    list_filter = ('checked',)
