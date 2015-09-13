from django.contrib import admin
from models import *
class RoomAdmin(admin.ModelAdmin):
	list_display = ('room', 'bhavan','vacancy')
class BillAdmin(admin.ModelAdmin):
	readonly_fields=('id',)
	list_display = ('id', 'gleader','college','amount')
#admin.site.register(Bill)
admin.site.register(Bill_new, BillAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bhavan)