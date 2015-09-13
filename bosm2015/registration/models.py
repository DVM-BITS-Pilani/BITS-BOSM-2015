from django.db import models
from django.contrib.auth.models import User
from regsoft.models import *
# Create your models here.
class UserProfile(models.Model):
    firstname = models.CharField('First Name', max_length=200)
    lastname = models.CharField('Last Name', max_length=200)
    college = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email_id = models.EmailField()
    user = models.ForeignKey(User, unique=True)
    default_limits = models.BooleanField(default=True)
    barcode = models.CharField(max_length=100,null=True,blank=True)
    def __unicode__(self):
        return str(self.firstname)+' '+str(self.lastname)
    class Meta:
        verbose_name_plural = "User Profiles"

class Participant(models.Model):
	GENDERS = (
		('M', 'Male'),
		('F', 'Female'),
        # ('O', 'Other'),
	)
	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=10, choices=GENDERS)
	phone = models.BigIntegerField()
	email_id = models.EmailField(blank=True)
	events = models.ManyToManyField('events.EventNew', blank = True)
	sport_leader = models.CharField(max_length=200, blank = True, null=True)
	gleader = models.ForeignKey(User,blank=True,null=True)
	firewallz = models.NullBooleanField('passed firewallz', null=True,blank=True)
	fid = models.NullBooleanField('passed inner booth',blank=True, null=True)
	acco=models.NullBooleanField('passed recnacc', null=True,blank=True)
	controlzpay=models.NullBooleanField('passed controlz', null=True,blank=True)
	room = models.ForeignKey('regsoft.Room',null=True,blank = True) # - will add later when working on reg soft
	#fireid = models.CharField(max_length = 100,null=True,blank=True)
	coach=models.BooleanField(default=False)
	barcode = models.CharField(max_length=100,null=True,blank=True)  #ignore this test chutiyap
	confirmation = models.BooleanField(default=False)
	bill_id=models.IntegerField( null = True, default= None, blank=False)
	def __unicode__(self):
		return str(self.name)

class EventLimits(models.Model):
    event = models.ForeignKey('events.EventNew')
    leader = models.ForeignKey('registration.UserProfile')
    limit = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Event Limits'

# Suggested Models by Nikhil
# class Leader(models.Model):
#     name = models.CharField(max_length=100)
#     # last_name = models.CharField(max_length=200)
#     college = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     phone = models.BigIntegerField(blank=True, null=True)
#     # email = models.EmailField(blank=True)
#     user = models.OneToOneField(User)
#     def __unicode__(self):
#         return str(self.name)

# class Participant(models.Model):
#     GENDERS = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         # ('O', 'Other'),
#     )
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=1, choices=GENDERS)
#     phone = models.BigIntegerField()
#     email = models.EmailField(blank=True)
#     events = models.ManyToManyField('events.Event', blank=True)
#     leader = models.ForeignKey(Leader, blank=True, null=True)
#     is_coach = models.BooleanField(default=False)
#     firewallz_id = models.CharField(max_length=100, blank=True, null=True)
#     passed_firewallz_outer = models.BooleanField(default=False)
#     passed_firewallz_inner = models.BooleanField(default=False)
#     passed_controlz = models.BooleanField(default=False)
#     passed_recnacc = models.BooleanField(default=False)
#     room = models.ForeignKey('regsoft.Room', blank=True, null=True) # - will add later when working on reg soft
#     def __unicode__(self):
#         return str(self.name)
