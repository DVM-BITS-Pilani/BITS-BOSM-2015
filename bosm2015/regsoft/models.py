from django.db import models

# Create your models here.
class Bhavan(models.Model):
	name=models.CharField(max_length=50)
	def __unicode__(self):
		return self.name
class Room(models.Model):
	bhavan=models.ForeignKey('Bhavan')
	room=models.CharField(max_length=50)
	vacancy=models.IntegerField()
	def __unicode__(self):
		return str(self.room)

#class bill(models.Model):
	#gleader=models.CharField(max_length=80)
	#glid= models.IntegerField(null=True)
	#amount=models.IntegerField()
	#college=models.CharField(max_length=100)
	#number = models.IntegerField()
	# notes_1000 = models.IntegerField(null=True, blank=True, default=0)
	# notes_500 = models.IntegerField(null=True, blank=True, default=0)
	# notes_100 = models.IntegerField(null=True, blank=True, default=0)
	# notes_50 = models.IntegerField(null=True, blank=True, default=0)
	# notes_20 = models.IntegerField(null=True, blank=True, default=0)
	# notes_10 = models.IntegerField(null=True, blank=True, default=0)
	#def __unicode__(self):
		#return str(self.number)

# class Bill(models.Model):
	# gleader=models.CharField(max_length=80)
	# amount=models.IntegerField()
	# college=models.CharField(max_length=100)
	# number = models.IntegerField()
	#draft_number = models.CharField(max_length=100)
	# def __unicode__(self):
		# return str(self.number)
		
class Bill_new(models.Model):
	gleader=models.CharField(max_length=80)
	amount=models.IntegerField()
	college=models.CharField(max_length=100)
	#number = models.IntegerField()
	draft_number = models.CharField(max_length=100)
	def __unicode__(self):
		return str(self.id)