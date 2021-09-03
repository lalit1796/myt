from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from model_utils import Choices
from enum import Enum

from profiling.models import City, Activity, Country

# Create your models here.

class Itinerary(models.Model):    

    itinerary_name = models.CharField(max_length=200,help_text="Refrence Name for Itenerary.")
    itinerary_length = models.IntegerField(default=0)
    
    head_1 = models.CharField(max_length=200)
    desc_1  = models.TextField()
    
    head_2 = models.CharField(max_length=200,null=True,blank=True)
    desc_2  = models.TextField(null=True,blank=True)
    
    head_3 = models.CharField(max_length=200,null=True,blank=True)
    desc_3  = models.TextField(null=True,blank=True)
    
    head_4 = models.CharField(max_length=200,null=True,blank=True)
    desc_4  = models.TextField(null=True,blank=True)
    
    head_5 = models.CharField(max_length=200,null=True,blank=True)
    desc_5  = models.TextField(null=True,blank=True)
    
    head_6 = models.CharField(max_length=200,null=True,blank=True)
    desc_6  = models.TextField(null=True,blank=True)
    
    head_7 = models.CharField(max_length=200,null=True,blank=True)
    desc_7  = models.TextField(null=True,blank=True)
    
    head_8 = models.CharField(max_length=200,null=True,blank=True)
    desc_8  = models.TextField(null=True,blank=True)
    
    head_9 = models.CharField(max_length=200,null=True,blank=True)
    desc_9  = models.TextField(null=True,blank=True)
    
    head_10 = models.CharField(max_length=200,null=True,blank=True)
    desc_10  = models.TextField(null=True,blank=True)
    
    head_11 = models.CharField(max_length=200,null=True,blank=True)
    desc_11  = models.TextField(null=True,blank=True)
    
    head_12 = models.CharField(max_length=200,null=True,blank=True)
    desc_12  = models.TextField(null=True,blank=True)
    
    head_13 = models.CharField(max_length=200,null=True,blank=True)
    desc_13  = models.TextField(null=True,blank=True)
    
    head_14 = models.CharField(max_length=200,null=True,blank=True)
    desc_14  = models.TextField(null=True,blank=True)
    
    head_15 = models.CharField(max_length=200,null=True,blank=True)
    desc_15 = models.TextField(null=True,blank=True)
    
    head_16 = models.CharField(max_length=200,null=True,blank=True)
    desc_16  = models.TextField(null=True,blank=True)
    
    head_17 = models.CharField(max_length=200,null=True,blank=True)
    desc_17  = models.TextField(null=True,blank=True)
    
    head_18 = models.CharField(max_length=200,null=True,blank=True)
    desc_18  = models.TextField(null=True,blank=True)
    
    head_19 = models.CharField(max_length=200,null=True,blank=True)
    desc_19  = models.TextField(null=True,blank=True)
    
    head_20 = models.CharField(max_length=200,null=True,blank=True)
    desc_20  = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return "%s" % (self.itinerary_name)
    
    class Meta:
        verbose_name_plural = "Itineraries"
        
      


class Qlink(models.Model):
        
    link_name = models.CharField(max_length=200)
    link_src = models.TextField()
    is_active = models.BooleanField(default=1,help_text="If ticked, it means 'is active everywhere - home page requires additional permission.'")
    is_home_active = models.BooleanField(default=1,help_text="If ticked, it means 'is active on home page if is_active status is true'.")
    
    
    
class Homeflyer(models.Model):

    flyer = models.ImageField(upload_to='homeflyers/',max_length=255)
    link_src = models.TextField()
    is_active = models.BooleanField(default=1,help_text="If ticked, it means 'is active everywhere - home page requires additional permission.'")
    is_home_active = models.BooleanField(default=1,help_text="If ticked, it means 'is active on home page if is_active status is true'.")