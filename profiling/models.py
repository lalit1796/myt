from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from model_utils import Choices
from enum import Enum



# Create your models here.

class Country(models.Model):
    

    country_name = models.CharField(max_length=200)
    code = models.CharField(max_length=200,help_text="Unique code for country.")
    
    def __str__(self):
        return "%s" % (self.country_name)
        
    class Meta:
        verbose_name_plural = "Countries"    
        
class City(models.Model):

    #country list
    India = 'India'
    Sri_Lanka = 'Sri Lanka'
    
    country_list = [
            
         (India , 'India'),
         (Sri_Lanka, 'Sri Lanka') 
            
    ]

    city_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,related_name='country')
    slug = models.CharField(max_length=100,default="--slug--")
    intro  = models.TextField(null=True)
    body = RichTextUploadingField(help_text="Article body")
    advisory = models.TextField(blank=True,null=True)
    disclaimer = models.TextField(blank=True,null=True)
    
    featured_img_1 = models.ImageField(upload_to='city/',max_length=255)
    featured_title_1 = models.CharField(max_length=200,null=True)
    
    featured_img_2 = models.ImageField(upload_to='city/',max_length=255)
    featured_title_2 = models.CharField(max_length=200,null=True)


    featured_img_3 = models.ImageField(upload_to='city/',max_length=255)
    featured_title_3 = models.CharField(max_length=200,null=True)


    featured_img_4 = models.ImageField(upload_to='city/',max_length=255)
    featured_title_4 = models.CharField(max_length=200,null=True)


    featured_img_5 = models.ImageField(upload_to='city/',max_length=255,null=True,blank=True)
    featured_title_5 = models.CharField(max_length=200,null=True,blank=True)


    featured_img_6 = models.ImageField(upload_to='city/',max_length=255,null=True,blank=True)
    featured_title_6 = models.CharField(max_length=200,null=True,blank=True)
    
    
    featured_img_7 = models.ImageField(upload_to='city/',max_length=255,null=True,blank=True)
    featured_title_7 = models.CharField(max_length=200,null=True,blank=True)


    featured_img_8 = models.ImageField(upload_to='city/',max_length=255,null=True,blank=True)
    featured_title_8 = models.CharField(max_length=200,null=True,blank=True)
    
    keywords = models.TextField()
    
    def __str__(self):
        return "%s" % (self.city_name)
        
    class Meta:
        verbose_name_plural = "Cities"
    
    
           


class Activity(models.Model):
    
    
    act_list = [
            
         ( 'land' , 'Land Activity'),
         ( 'water', 'Water Activity'),
         ( 'air' , 'Air Activity'),
         ( 'other', 'Other Activity'),  
            
    ]

    activity_name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    type = models.CharField(max_length=100,choices=act_list,default="India")
    thumb = models.ImageField(upload_to='activity/thumbs',max_length=255,help_text="200 x 200")
    banner = models.ImageField(upload_to='activity/banners',max_length=255,help_text="900 x 300")
    
    def __str__(self):
        return "%s" % (self.activity_name)
    
    class Meta:
        verbose_name_plural = "Activities"

    
    
        
        

class Index(models.Model):
    
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    url = models.CharField(max_length=200,null=True,blank=True) 
    thumb = models.ImageField(upload_to='thumbs',max_length=255,help_text="Ideal dimaensions 300 x 240",null=True,blank=True)
    path1 = models.CharField(max_length=200,null=True,blank=True)
    path2 = models.CharField(max_length=200,null=True,blank=True)
    path3 = models.CharField(max_length=200,null=True,blank=True)
    path4 = models.CharField(max_length=200,null=True,blank=True)
    price = models.CharField(max_length=200,null=True,blank=True)
    service_time = models.CharField(max_length=200,null=True,blank=True)
    tags = models.TextField(null=True,blank=True)
    keywords = models.TextField(null=True,blank=True)
    
    make_exclusive =  models.BooleanField(default=0,help_text="For exclusive packages.")
    make_indemand =  models.BooleanField(default=0,help_text="For in demand packages.")
    make_limitedoffer = models.BooleanField(default=0,help_text="For limited packages.")
    make_inbudget =  models.BooleanField(default=0,help_text="For budget packages.")
    
    ref_id = models.CharField(max_length=10, default="",null=True,blank=True)
    ref_uid = models.CharField(max_length=10, default="",null=True,blank=True)
    ref_service_code = models.CharField(max_length=10, default="",null=True,blank=True)
    
    is_listed = models.BooleanField(default=0,help_text="Is Running on website")
    home_feature_status = models.BooleanField(default=0,help_text="Is Running on Home.")
    
    class Meta:
        verbose_name_plural = "Indeces"


    
    
