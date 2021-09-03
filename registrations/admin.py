from django.contrib import admin
import uuid
from django import forms
from django.contrib.auth.models import Group
from tours.models import Package, ActivitySale
from profiling.models import City, Activity, Country, Index 
from client.models import Enquiry, BookingPackage, BookingActivity, Profile, Order
from props.models import Itinerary, Qlink, Homeflyer
import csv
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.db import models

admin.site.unregister(Group)
admin.site.site_header = "myTrip"
admin.site.index_title = "Administrative Panel"
admin.site.site_title = "myTrip Admin Panel"




#manager
class SiteManager(models.Manager):
    def isnot_super(self,request):
        spr = True;
        if request.user.is_superuser:
            spr = False
        return spr


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
    
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected"


class packageAdmin(admin.ModelAdmin):
    
    class Media:
        css = {'all':('cs/airpicker.css',) }
        js = ('js/admin_cst.js',)


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

    def get_readonly_fields(self,request,obj=None):
        readonly = ["url_title","uid","service_code"]
        return readonly

    def indexing(self,request,obj):
        if Index.objects.filter(ref_id=obj.id,ref_uid=obj.uid,ref_service_code=obj.service_code).exists():
            index = Index.objects.get(ref_id=obj.id,ref_uid=obj.uid,ref_service_code=obj.service_code)
            
        else:
            index = Index(
            ref_id=obj.id,
            ref_uid=obj.uid,
            ref_service_code=obj.service_code,
            )
        index.title=obj.package_title
        index.description=obj.intro
        index.url=obj.url_title
        index.thumb=obj.thumb
        index.price=obj.generalprize_per_adult
        index.service_time=obj.duration_days
        index.tags=obj.tags
        index.keywords=obj.keywords
        
        index.make_exclusive=obj.make_exclusive
        index.make_indemand=obj.make_indemand
        index.make_limitedoffer=obj.make_limitedoffer
        index.make_inbudget=obj.make_inbudget
        
        index.is_listed=obj.is_listed
        index.home_feature_status=obj.home_feature_status
        
        index.save()
    
        
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            slug = slugify(obj.package_title)
            unique_slug = slug
            num = 1
            while Package.objects.filter(url_title=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
           
            obj.url_title = slugify(unique_slug) #Slug only created once.
            
            suuid = uuid.uuid4().hex[:8]
            pos = 1
            while ActivitySale.objects.filter(uid=suuid).exists():
                suuid = '{}{}'.format(suuid, num)
            obj.uid = suuid
            
            self.indexing(request,obj)
            super().save_model(request, obj, form, change=True)
        else:
            self.indexing(request,obj)
            super().save_model(request, obj, form, change=True)
    
    actions = ["export_as_csv",]
    list_display=('package_title','dates','generalprize_per_adult','generalprize_per_child','home_feature_status',)
    list_filter=('generalprize_per_adult','home_feature_status',)
    list_per_page = 200





class cityAdmin(admin.ModelAdmin):
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

    
    def get_readonly_fields(self,request,obj=None):
        readonly = ["slug",]
        return readonly
        
        
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            slug = slugify(obj.city_name)
            unique_slug = slug
            num = 1
            while City.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            obj.slug = slugify(unique_slug) #Slug for city
            super().save_model(request, obj, form, change=True)
        else:
            super().save_model(request, obj, form, change=True)
            
    list_display=('city_name','id','country')
    list_filter=('city_name','country',)
    list_per_page = 200
    
    
class activityAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            slug = slugify(obj.activity_name)
            unique_slug = slug
            num = 1
            while Activity.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            obj.slug = slugify(unique_slug) #Slug for city
            super().save_model(request, obj, form, change=True)
        else:    
            super().save_model(request, obj, form, change=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']


    list_display=('activity_name','id','type')
    list_filter=('type',)
    
class activitysaleAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self,request,obj=None):
        readonly = ["slug","uid","service_code"]
        return readonly
    
    def indexing(self,request,obj):
        if Index.objects.filter(ref_id=obj.id,ref_uid=obj.uid,ref_service_code=obj.service_code).exists():
            index = Index.objects.get(ref_id=obj.id,ref_uid=obj.uid,ref_service_code=obj.service_code)
            
        else:
            index = Index(
            ref_id=obj.id,
            ref_uid=obj.uid,
            ref_service_code=obj.service_code,
            )
        index.title=obj.location
        index.description=obj.intro
        index.url=obj.slug
        index.thumb=obj.thumb
        index.price=obj.prize
        index.service_time=obj.duration
        index.path1=obj.name.slug
        index.keywords=obj.keywords
        
        index.make_exclusive=obj.make_exclusive
        index.make_indemand=obj.make_indemand
        index.make_limitedoffer=obj.make_limitedoffer
        index.make_inbudget=obj.make_inbudget
        
        index.is_listed=obj.is_listed
        index.home_feature_status=obj.home_feature_status
        
        index.save()
    
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            slug = slugify(obj.location)
            unique_slug = slug
            num = 1
            while ActivitySale.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            obj.slug = slugify(unique_slug) #Slug for city
            
            suuid = uuid.uuid4().hex[:8]
            pos = 1
            while ActivitySale.objects.filter(uid=suuid).exists():
                suuid = '{}{}'.format(suuid, num)
            obj.uid = suuid
            self.indexing(request,obj)
            super().save_model(request, obj, form, change=True)
        else: 
            self.indexing(request,obj)        
            super().save_model(request, obj, form, change=True)
    
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']


    list_display=('name','city','uid','prize','is_booking_open','is_listed','location',)
    list_filter=('is_booking_open','is_listed','is_booking_open',)
 












 
class enquiryAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        if SiteManager.isnot_super(self,request):
            return False
    
    def get_readonly_fields(self,request,obj=None):
        readonly = ["first_name","last_name","email","mobile","service_code","service_code_id","service_code_url","adults","children","date","message","is_signed_up","user_id","is_new"]
        return readonly 
    
 
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            
    def save_model(self, request, obj, form, change):
        obj.is_new=False
        super().save_model(request, obj, form, change=True)
 
    list_display=("id","is_new","is_replied","first_name","last_name","email","mobile","service_code",)
    list_filter=('is_new','is_replied','service_code',)
 
 
 
 
 
 
 
 
 
 
 
class countryAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']


    list_display=('country_name','id',)

class qlinkAdmin(admin.ModelAdmin):
    list_display=('link_name','link_src','is_active','is_home_active',)
    list_filter=('is_active','is_home_active',)
    list_per_page = 200


class indexAdmin(admin.ModelAdmin):

    def get_readonly_fields(self,request,obj=None):
        readonly = ["title",
                    "ref_id",
                    "ref_uid",
                    "ref_service_code",
                    "make_exclusive",
                    "make_inbudget",
                    "make_indemand",
                    "make_limitedoffer",
                    "keywords",
                    "tags",
                    "description",
                    "url",
                    "thumb",
                    "path1",
                    "path2",
                    "path3",
                    "path4",
                    "price",
                    "service_time",
                    "is_listed",
                    "home_feature_status"
                    ]
        return readonly 
        
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    list_display=('title','ref_id','ref_uid','ref_service_code','home_feature_status','is_listed',)
    list_per_page = 200













class adminBookingPackage(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            
            
            
            
            
            
class adminBookingActivity(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']            

class profileAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self,request,obj=None):
        readonly = ["user","mobile","address","bio","location","birth_date"]
        return readonly 
    
 
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            
    def save_model(self, request, obj, form, change):
        obj.is_new=False
        super().save_model(request, obj, form, change=True)
 
    list_display=("user","mobile","address","bio","location","birth_date",)


class adminOrder(admin.ModelAdmin):

    #def has_add_permission(self, request):
        #return False
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']  

    #run this save model to reset starting point as 1000
    #first remove has_add_permission to reset through admin...
    
    #def save_model(self, request, obj, form, change):
        #obj.id=1000
        #super().save_model(request, obj, form, change=True)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
        
    list_display=('id','txn',)    
 
# Package
admin.site.register(Package,packageAdmin)
# Country
admin.site.register(Country,countryAdmin)
# City
admin.site.register(City,cityAdmin)
# Activity
admin.site.register(Activity,activityAdmin)
# ActivitySale
admin.site.register(ActivitySale,activitysaleAdmin)
# Itenerary
admin.site.register(Itinerary)
# Enquiry
admin.site.register(Enquiry,enquiryAdmin)
# Quicklinks
admin.site.register(Qlink,qlinkAdmin)
#Homeflyers
admin.site.register(Homeflyer)

admin.site.register(BookingPackage,adminBookingPackage)
admin.site.register(BookingActivity,adminBookingActivity)
admin.site.register(Profile,profileAdmin)
admin.site.register(Order,adminOrder)

admin.site.register(Index,indexAdmin)

