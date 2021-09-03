from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from model_utils import Choices
from enum import Enum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiling.models import City, Activity, Country





class Enquiry(models.Model):
    
    class Meta:
        verbose_name_plural = "Enquiries" 
    


    first_name = models.CharField(max_length=200,help_text="First name of client")
    last_name = models.CharField(max_length=200,null=True,blank=True,help_text="Last name of client")
    email = models.CharField(max_length=200,null=True,blank=True,help_text="Email of client")
    mobile = models.CharField(max_length=200,help_text="Mobile of client")
    service_code =  models.CharField(max_length=200,null=True,blank=True,help_text="Package/Activity")
    product_id = models.CharField(max_length=200,null=True,blank=True,help_text="Product id")
    product_url = models.CharField(max_length=255,null=True,blank=True,help_text="Product url")
    adults = models.CharField(max_length=200,null=True,blank=True,help_text="")
    children = models.CharField(max_length=200,null=True,blank=True,help_text="")
    date = models.CharField(max_length=200,null=True,blank=True,help_text="")
    message = models.TextField()
    
    is_signed_up =  models.BooleanField(default=0,help_text="Does user hold an account ?")
    user_id = models.IntegerField(default=0,help_text="User id, if user has an account",null=True,blank=True)
    
    is_new =  models.BooleanField(default=1,help_text="New or old")
    is_replied =  models.BooleanField(default=0,help_text="Has query been replied")
    actions_taken = models.TextField(null=True,blank=True)
    response_note = models.TextField(null=True,blank=True)
    
    
class BookingActivity(models.Model):
    
    class Meta:
        verbose_name_plural = "Booked Activities"

    lead_passenger_name = models.CharField(max_length=200,help_text="Full Name of lead passenger")
    mobile = models.CharField(max_length=200,help_text="Contact number")
    email = models.CharField(max_length=200,null=True,blank=True,help_text="Email of client")
    date = models.CharField(max_length=200,help_text="Departure/Activity date")
    adult_tally =  models.IntegerField(default=0,help_text="Tally of adult travellers")
    children_tally = models.IntegerField(default=0,help_text="Tally of child travellers")
    adult_expense = models.IntegerField(default=0,help_text="Expense for adults")
    children_expense = models.IntegerField(default=0,help_text="Expense for children")
    gst = models.IntegerField(default=0,help_text="Gst")
    gst_amount = models.IntegerField(default=0,help_text="Gst Amount") 
    expense = models.IntegerField(default=0,help_text="Expense excluding gst")
    expense_net = models.IntegerField(default=0,help_text="Net Amount including gst")
    payment_type= models.CharField(max_length=200,help_text="Type of payment - Full or Advance")
    user_id = models.IntegerField(default=0,help_text="User Id")
    booking_uid = models.CharField(max_length=200,help_text="Booking Unique-Id")
    txn = models.CharField(max_length=200,help_text="Transaction number")
    is_confirmation_sent = models.BooleanField(default=0,help_text="If the reply is sent")
    is_vendor_allocated = models.BooleanField(default=0,help_text="Has the vendor/handler been associated.")
    is_new = models.BooleanField(default=0,help_text="Is it a new booking")
    response = models.TextField(null=True,blank=True)
    comments = models.TextField(null=True,blank=True)
    
      
class BookingPackage(models.Model):
    
    
    class Meta:
        verbose_name_plural = "Booked Packages"

    lead_passenger_name = models.CharField(max_length=200,help_text="Full Name of lead passenger")
    mobile = models.CharField(max_length=200,help_text="Contact number")
    email = models.CharField(max_length=200,null=True,blank=True,help_text="Email of client")
    date = models.CharField(max_length=200,help_text="Departure/Activity date")
    adult_tally =  models.IntegerField(default=0,help_text="Tally of adult travellers")
    children_tally = models.IntegerField(default=0,help_text="Tally of child travellers")
    adult_expense = models.IntegerField(default=0,help_text="Expense for adults")
    children_expense = models.IntegerField(default=0,help_text="Expense for children")
    gst = models.IntegerField(default=0,help_text="Gst")
    gst_amount = models.IntegerField(default=0,help_text="Gst Amount") 
    expense = models.IntegerField(default=0,help_text="Expense excluding gst")
    expense_net = models.IntegerField(default=0,help_text="Net Amount including gst")
    payment_type= models.CharField(max_length=200,help_text="Type of payment - Full or Advance")
    user_id = models.IntegerField(default=0,help_text="User Id")
    booking_uid = models.CharField(max_length=200,help_text="Booking Unique-Id")
    txn = models.CharField(max_length=200,help_text="Transaction number")
    is_confirmation_sent = models.BooleanField(default=0,help_text="If the reply is sent")
    is_vendor_allocated = models.BooleanField(default=0,help_text="Has the vendor/handler been associated.")
    is_new = models.BooleanField(default=0,help_text="Is it a new booking")
    response = models.TextField(null=True,blank=True)
    comments = models.TextField(null=True,blank=True)    
    
    
    
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
    
    
    
class Order(models.Model):
    
    id = models.BigAutoField(primary_key=True,editable=True,help_text="Order Number")
    txn = models.CharField(max_length=200,help_text="Transaction Id")
    is_successfully_paid = models.BooleanField(default=0,help_text="Is the payment successful")
    response = models.BooleanField(default=0,help_text="Is the payment successful")
    
    total_amount = models.IntegerField(default=0,help_text="Net Pay")
    amount_paid = models.IntegerField(default=0,help_text="Net Pay",null=True, blank=True)
    payment_type = models.CharField(max_length=200,default='undefined',help_text="Payment Type")
    gst = models.IntegerField(default=0,help_text="Gst")
    gst_amount = models.IntegerField(default=0,help_text="Gst Amount")
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='user',help_text="Logged in user",null=True, blank=True)
    
    total_count = models.IntegerField(default=0,help_text="Number of Individuals",null=True, blank=True)
    adult_count = models.IntegerField(default=0,help_text="Number of adults",null=True, blank=True)
    adult_bill = models.IntegerField(default=0,help_text="Net bill for adults",null=True, blank=True)
    adult_discount_offered = models.IntegerField(default=0,help_text="Discount offered per adult",null=True, blank=True)
    adult_per_cost = models.IntegerField(default=0,help_text="Cost per adult",null=True, blank=True)
    kids_count = models.IntegerField(default=0,help_text="Number of children",null=True, blank=True)
    kids_bill = models.IntegerField(default=0,help_text="Net bill for kids",null=True, blank=True)
    kids_discount_offered = models.IntegerField(default=0,help_text="Discount offered per child",null=True, blank=True)
    kids_per_cost = models.IntegerField(default=0,help_text="Cost per Kids",null=True, blank=True)
    
    
    first_name = models.CharField(max_length=200,help_text="First Name",default="anonymous")
    last_name = models.CharField(max_length=200,help_text="Last Name",null=True, blank=True)
    mobile = models.CharField(max_length=200,help_text="Contact number",null=True, blank=True)
    email = models.CharField(max_length=200,null=True,blank=True,help_text="Email of client")
    
    date = models.CharField(max_length=200,help_text="Departure/Activity date",null=True, blank=True)
    
    productinfo =  models.IntegerField(default=0,help_text="Product Info") # package
    product_id = models.IntegerField(default=0,help_text="Product Id")
    product_uid = models.CharField(max_length=200,default=0,help_text="Product UID")
    service_code = models.CharField(max_length=10,help_text="Service code of product")
       
    has_action_taken = models.BooleanField(default=0,help_text="Has the vendor/handler been associated.")
    is_new = models.BooleanField(default=0,help_text="Is it a new booking")
    
    
    
    
    def adult_charge(self):
        grand = self.adult_per_cost * self.adult_count
        return int(grand)
    
    def kids_charge(self): 
        grand = self.kids_per_cost * self.kids_count
        return int(grand)
    
    def subtotal(self): # after discounting
        adult_per_dis = self.adult_per_cost * (self.adult_discount_offered/100) 
        adult_sub = (self.adult_per_cost - adult_per_dis) * self.adult_count
        
        kids_per_dis = self.kids_per_cost * (self.kids_discount_offered/100) 
        kids_sub = (self.kids_per_cost - kids_per_dis) * self.kids_count
        
        total = adult_sub + kids_sub
        return int(total)    
    
    def gst_on_subtotal(self):
        net_gst = self.subtotal() * (self.gst/100)
        return int(net_gst)
    
    def grandtotal(self):
        total = self.adult_charge() + self.kids_charge()
        return int(total)    
    
    def finalpay(self):
        final = self.subtotal() + self.gst_on_subtotal()
        return int(final)
        
    