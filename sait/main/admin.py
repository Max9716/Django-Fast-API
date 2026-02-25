from django.contrib import admin

from . models import Flat, Application
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import UserActionLog

admin.site.register(Flat)
admin.site.register(Application)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date', 'get_data')
    readonly_fields = ('session_key', 'expire_date', 'get_data')

    def get_data(self, obj):
        return obj.get_decoded()
    get_data.short_description = 'Data'

@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'path', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'action', 'path')
    ordering = ('-timestamp',)