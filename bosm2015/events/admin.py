from django.contrib import admin
from .models import EventNew
# Register your models here.

class EventNewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'min_limit', 'max_limit')
    list_display_links = ['name']
    # list_filter = ['category']
    search_fields = ['name']
# admin.site.register(Category)
admin.site.register(EventNew, EventNewAdmin)