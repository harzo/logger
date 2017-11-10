from django.contrib import admin

from .models import Log

class LogAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'start_time', 'end_time', 'summary')
    list_filter = ['id_user', 'start_time']

admin.site.register(Log, LogAdmin)