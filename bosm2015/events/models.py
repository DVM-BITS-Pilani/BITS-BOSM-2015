from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
# class Category(models.Model):
#     name=models.CharField(max_length=100, unique=True)
#     weight=models.PositiveSmallIntegerField()
#     class Meta:
#         verbose_name_plural = 'categories'
#     def __unicode__(self):
#         return  self.name

class EventNew(models.Model):
    name = models.CharField(max_length=100,unique=True)
    content = RichTextField()
    description = models.CharField(blank=True,max_length=140)
    icon = models.ImageField(blank=True, upload_to="icons")
    date = models.CharField(max_length=100, default='TBA')
    time = models.CharField(max_length=100, default='TBA')
    venue = models.CharField(max_length=100, default='TBA')
    endtime = models.CharField(max_length=100, default='TBA')
    max_limit = models.IntegerField(default=11) 
    min_limit = models.IntegerField(default=2)
    class Meta:
        verbose_name_plural = 'events'
    def __unicode__(self):
        return self.name