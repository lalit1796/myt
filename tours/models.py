from django.db import models
import uuid
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from model_utils import Choices
from enum import Enum

from profiling.models import City, Activity, Country
from props.models import Itinerary
# Create your models here.




class Package(models.Model):


    #age group
    ALL = 'all'
    ABOVE18 = '18'
    
    AGE_GROUP = [
            
         (ALL , 'ALL'),
         (ABOVE18, 'ABOVE18') 
            
    ]
    
    
    home_feature_status = models.BooleanField(default=1,help_text="If ticked, it means that this sale is fetured on home in Pins.")
    uid = models.CharField(unique=True,max_length=200, default="--uid--")
    url_title = models.SlugField(unique=True,max_length=200)
    service_code = models.CharField(max_length=10, default="pac")
    package_title = models.CharField(max_length=200)
    intro  = models.TextField(null=True)
    insight = models.TextField(null=True)
    generalprize_per_adult = models.IntegerField(default=0)
    are_children_allowed =  models.BooleanField(default=0,help_text="Tick if children allowed.")
    generalprize_per_child = models.IntegerField(default=0)
    discount_pax2 = models.IntegerField(default=0,help_text="Discount applicable for min 2 individuals.(1 adult + 1 child) or 2 adults; on their rspective charges.")
    discount_pax4 = models.IntegerField(default=0,help_text="Discount applicable for min 4 individuals.")
    discount_pax6 = models.IntegerField(default=0,help_text="Discount applicable for min 6 individuals.")
    discount_pax8 = models.IntegerField(default=0,help_text="Discount applicable for min 8 individuals.")
    discount_max = models.IntegerField(default=0,help_text="Discount applicable for more than 8 individuals.")
    
    gst = models.IntegerField(default=5)
    dates = models.CharField(max_length=200)
    duration_days = models.IntegerField(default=1,help_text="Trip days")
    itinerary = models.ForeignKey(Itinerary,on_delete=models.PROTECT,related_name='itinerary',help_text="Select or Create Itinerary.")
    highlight = models.TextField()
    inclusion = models.TextField()
    exclusion = models.TextField()
    agegroup = models.CharField(max_length=100,choices=AGE_GROUP,default="All")
    mention_cities = models.CharField(max_length=255,help_text="Use same names of cities in citylist. eg: new delhi, chandigarh, manali, ...")
    make_exclusive =  models.BooleanField(default=0,help_text="For exclusive packages.")
    make_indemand =  models.BooleanField(default=0,help_text="For in demand packages.")
    make_limitedoffer = models.BooleanField(default=0,help_text="For limited packages.")
    make_inbudget =  models.BooleanField(default=0,help_text="For budget packages.")
    is_booking_open = models.BooleanField(default=1,help_text="If ticked, it means the bookings are closed for this sale.")
    is_couple_only = models.BooleanField(default=1,help_text="If ticked, it means the package is for couples.")
    is_or_has_trekking = models.BooleanField(default=1,help_text="If ticked, it means the tour contains some kind of trekking")
    is_it_group_package = models.BooleanField(default=1,help_text="If ticked, it means the tour will happen in group.")
    is_expedition = models.BooleanField(default=1,help_text="If ticked, it means it is an expedition.")
    is_listed = models.BooleanField(default=1,help_text="If ticked, it means that this sale is live.")
    requirement = models.TextField(blank=True,null=True)
    advisory = models.TextField(blank=True,null=True)
    thingstocarry = models.TextField(blank=True,null=True)
    ameneties = models.TextField(blank=True,null=True)
    disclaimer = models.TextField(blank=True,null=True)
    tags = models.TextField(default=0,help_text="Eg: Goa beach, Snow, Holiday in Manali")
    keywords = models.TextField()
    
    thumb = models.ImageField(upload_to='thumbs',max_length=255,help_text="Ideal dimensions 300 x 240")
    
    featured_img_1 = models.ImageField(upload_to='tourImg/',max_length=255)
    featured_title_1 = models.CharField(max_length=200)
    
    featured_img_2 = models.ImageField(upload_to='tourImg/',max_length=255)
    featured_title_2 = models.CharField(max_length=200)


    featured_img_3 = models.ImageField(upload_to='tourImg/',max_length=255)
    featured_title_3 = models.CharField(max_length=200)


    featured_img_4 = models.ImageField(upload_to='tourImg/',max_length=255)
    featured_title_4 = models.CharField(max_length=200)


    featured_img_5 = models.ImageField(upload_to='tourImg/',max_length=255)
    featured_title_5 = models.CharField(max_length=200)
    
    @property
    def printcost(self):
        cost = self.generalprize_per_adult
        dis = self.discount_pax2
        dis_amount = cost * (dis/100) 
        amount = cost - dis_amount
        return int(amount)
    
    
    def pax4(self):
        cost = self.generalprize_per_adult
        dis = self.discount_pax4
        if(dis <= 0):
            return self.printcost
        else:
            dis_amount = cost * (dis/100) 
            amount = cost - dis_amount
            print("hit")
            return int(amount)
    
    
    
    def pax6(self):
        cost = self.generalprize_per_adult
        dis = self.discount_pax6
        if(dis<=0):
            return self.pax4()
        else:
            dis_amount = cost * (dis/100) 
            amount = cost - dis_amount
            return int(amount)
    
    
    
    def pax8(self):
        cost = self.generalprize_per_adult
        dis = self.discount_pax8
        if(dis<=0):
            return self.pax6()
        else:
            dis_amount = cost * (dis/100) 
            amount = cost - dis_amount
            return int(amount)
            
    
    def dis_max(self):
        cost = self.generalprize_per_adult
        dis = self.discount_max
        if(dis<=0):
            return self.pax8()
        else:
            dis_amount = cost * (dis/100) 
            amount = cost - dis_amount
            return int(amount)
    
    
class ActivitySale(models.Model):
    
    ALL = 'all'
    ABOVE18 = '18'
    
    AGE_GROUP = [
            
         (ALL , 'ALL'),
         (ABOVE18, 'ABOVE18') 
            
    ]
    
    home_feature_status = models.BooleanField(default=0,help_text="If ticked, it means that this sale is fetured on home in Pins.")    
    name = models.ForeignKey(Activity,on_delete=models.PROTECT,related_name='name',help_text="If activity is not listed then it can be created in profiling or ask admin to create one.")
    uid = models.CharField(unique=True,max_length=200, default="--uid--")
    slug = models.CharField(unique=True,max_length=200,default="--url-slug--")
    service_code = models.CharField(max_length=10, default="act")
    city = models.ForeignKey(City,on_delete=models.PROTECT,related_name='city',help_text="If city is not listed then it can be created in profiling or ask admin to create one.")
    location = models.CharField(max_length=200,help_text="Write the location name to create a unique url eg: 'Greater Akshardhaam Rafting Point' it will make url as '.../greater-akshardhaam-rafting-point/' only once. ")
    activitypoint = models.TextField()
    duration = models.CharField(max_length=200, default="0 hours", help_text="Mention Clear Durataion in minutes or hours or days. Eg: 15 minutes")
    mapembeed = models.TextField()
    
    is_booking_open = models.BooleanField(default=1,help_text="If ticked, it means the bookings are closed for this sale.")
    is_listed = models.BooleanField(default=1,help_text="If ticked, it means that this sale is live.")
    
    make_exclusive =  models.BooleanField(default=0,help_text="For exclusive packages.")
    make_indemand =  models.BooleanField(default=0,help_text="For in demand packages.")
    make_limitedoffer = models.BooleanField(default=0,help_text="For limited packages.")
    make_inbudget =  models.BooleanField(default=0,help_text="For budget packages.")
        
    intro  = models.TextField()
    prize = models.IntegerField(default=0)
    gst = models.IntegerField(default=5)
    
    highlight = models.TextField()
    inclusion = models.TextField(null=True,blank=True)
    exclusion = models.TextField(null=True,blank=True)
        
    agegroup = models.CharField(max_length=100,choices=AGE_GROUP,default="AllAgeGroup")
    vendor = models.TextField(default="none")
    
    body = RichTextUploadingField(help_text="For Additional informations",null=True,blank=True)
    
    requirement = models.TextField(blank=True,null=True)
    advisory = models.TextField(blank=True,null=True)
    disclaimer = models.TextField(blank=True,null=True)
    
    keywords = models.TextField()
    
    thumb = models.ImageField(upload_to='thumbs',max_length=255,help_text="Ideal dimensions 300 x 240")
    
    featured_img_1 = models.ImageField(upload_to='saleImg/',max_length=255)
    featured_title_1 = models.CharField(max_length=200)
    
    featured_img_2 = models.ImageField(upload_to='saleImg/',max_length=255)
    featured_title_2 = models.CharField(max_length=200)


    featured_img_3 = models.ImageField(upload_to='saleImg/',max_length=255)
    featured_title_3 = models.CharField(max_length=200)


    featured_img_4 = models.ImageField(upload_to='saleImg/',max_length=255)
    featured_title_4 = models.CharField(max_length=200)


    featured_img_5 = models.ImageField(upload_to='saleImg/',max_length=255,null=True,blank=True)
    featured_title_5 = models.CharField(max_length=200,null=True,blank=True)
    
    featured_img_6 = models.ImageField(upload_to='saleImg/',max_length=255,null=True,blank=True)
    featured_title_6 = models.CharField(max_length=200,null=True,blank=True)
    
    featured_img_7 = models.ImageField(upload_to='saleImg/',max_length=255,null=True,blank=True)
    featured_title_7 = models.CharField(max_length=200,null=True,blank=True)
    
    featured_img_8 = models.ImageField(upload_to='saleImg/',max_length=255,null=True,blank=True)
    featured_title_8 = models.CharField(max_length=200,null=True,blank=True)
    
    featured_img_9 = models.ImageField(upload_to='saleImg/',max_length=255,null=True,blank=True)
    featured_title_9 = models.CharField(max_length=200,null=True,blank=True)
    
    featured_img_10 = models.ImageField(upload_to='saleImg/',max_length=255,null=True,blank=True)
    featured_title_10 = models.CharField(max_length=200,null=True,blank=True)    
    
  
        
    
    
    