"""mytrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static 

from django.conf import settings

#custom
from pages.views import home_view, search_view, login_view, info_view, city_view, product_view, city_list_view, product_list_view, activity_list_view, booking_p_view, activity_content_view, register_view, logout_view, profile_view, activity_view, enq_view, checkout_p_view, signup_view, booking_a_view 
from payment.views import checkout_view,  payment_response_view 

urlpatterns = [
    #home/search
    path('',home_view, name='home'),
    path('search/',search_view, name='search'),
    
    #ckeditore widget
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    #admin 
    path('jabes/', admin.site.urls),
    
    #info
    path('info/',info_view, name='info'),
    
    #city
    path('explore/',city_list_view, name='explore'),
    path('explore/<slug:slug>', city_view,name="city"),
    
    
    #package
    path('package/',product_list_view, name='package_all'),
    path('package/<slug:slug>',product_view, name='package_profile'),
    
    #activity_list_view
    path('activity/',activity_list_view, name='activity_all'),
    path('activity/<slug:slug>',activity_view, name='activity_cat_profile'),
    path('activity/<slug:name>/<slug:loc>/',activity_content_view, name='activity_profile_content'),
    
    #bookings activity_booking_profile
    path('package/book/<slug:slug>', booking_p_view, name='package_booking_profile'), 
    path('activity/book/<slug:slug>', booking_a_view, name='activity_booking_profile'),
    path('package/checkout/', checkout_p_view, name='package_checkout_profile'), 
    
    
    #payment
    path('checkout/<slug:orderid>', checkout_view, name='checkout_order'),
    path('payment/status', payment_response_view, name='payment_status'),
   
   
    
    
    #ajax
    
    path('auth/',register_view,name='register'),
    path('signup/',signup_view,name='signup'),
    path('logout/',logout_view,name='logout'),
    path('enq/',enq_view,name='enquiry'),
    
    #profile
    path('login/',login_view, name="logme"),
    path('account',profile_view,name='profile'),
    
    
    
    
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

