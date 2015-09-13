from django.contrib import admin
from registration.models import UserProfile, Participant, EventLimits
from django.db import models
from django.forms import CheckboxSelectMultiple

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'college', 'leader_name', 'firewallz', 'controlzpay', 'acco')
    list_filter = ('firewallz', 'acco', 'controlzpay')
    filter_horizontal = ('events',)
    search_fields = ('name',)
    def college(self, obj):
        try:
            result = obj.gleader.userprofile_set.last().college
        except AttributeError:
            result = '(None)'
        return result
    def leader_name(self, obj):
        try:
            result = obj.gleader.userprofile_set.last()
        except AttributeError:
            result = '(None)'
        return result

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('name', 'gender', 'phone', 'events', 'room')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Leader Information', {'fields': ['firstname', 'lastname', 'college', 'city', 'phone', 'user', 'default_limits']}),
    ]
    search_fields = ('firstname', 'lastname', 'college')
    # inlines = [ParticipantInline]
    def members(self, obj):
        return obj.user.participant_set.count()
    list_display = ('__unicode__', 'college', 'members', 'city', 'phone')
    list_filter = ('city', 'college')

class EventLimitsAdmin(admin.ModelAdmin):
    list_display = ('leader', 'event', 'limit')
    fields = ( 'leader', 'event', 'limit')
    search_fields = ('leader',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(EventLimits, EventLimitsAdmin)