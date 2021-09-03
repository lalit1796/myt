from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.shortcuts import render
from django.http import HttpResponse
from tours.models import Package, ActivitySale
from profiling.models import Country, City, Activity, Index
from props.models import Itinerary, Qlink, Homeflyer
from client.models import Enquiry
from pytz import timezone
from datetime import datetime,timedelta
from django.http import HttpResponse
from itertools import chain
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.defaultfilters import slugify
from django.db import IntegrityError
import uuid 
import datetime


# Create your views here.



def qlinks():
    qlinks = Qlink.objects.all()
    return qlinks

def country():
    return Country.objects.all()

def city():
    return City.objects.all()
    
def activity():
    return Activity.objects.all()    

# home view
def home_view(request,*args,**kwargs):
    flyers = Homeflyer.objects.filter(is_active=True, is_home_active=True)
    product = Index.objects.filter(home_feature_status=True,is_listed=True)
    
    
    
    context={
        'pagetitle':"Home",
        'prod':product,
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        'flyers':flyers,
        'qlinks':qlinks()
    }
    return render(request, "home.html",context)
    
    
    
# search view
def search_view(request,*args,**kwargs):
    
    key = (request.GET.get('k')) 
    key = key.replace(","," ").rstrip()
    bkey = key.split(" ")
    
    
    product = Index.objects.filter(keywords__icontains=key,is_listed=True) #most relevant.
    productb = product.exclude(id__in=product) #empty for least relevent. #typecasting... 
    
    for k in bkey:
        temp = Index.objects.filter(keywords__icontains=k,is_listed=True).exclude(id__in=product).exclude(id__in=productb) #exclude products already selected.
        productb = productb|temp 
        print(productb)
       
   
  
    product = list(chain(product,productb))  #chaining to order product before productb. #final product.
    context={
        'pagetitle':key,
        'prod':product,
        'key':key,
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        'pagetitle':key+' - myTrip Search'
    }
    return render(request, "searchpage.html",context)    
    
   



#info view
def info_view(*args,**kwargs):
    return HttpResponse('helo world')
    
    
#explore
def city_list_view(request,*args,**kwargs):
    return HttpResponse('helo city view') # currently city list view is not defined


#explore/city#profile
def city_view(request,slug,*args,**kwargs):
    
    cityp = City.objects.get(slug=slug) #only one object
    product = Package.objects.filter(tags__icontains=slug) # query set
    activity_in = ActivitySale.objects.filter(city=cityp.id)
    
    context = {
        'pagetitle':"Explore | "+cityp.city_name, #default
        'prod':product,
        'city':cityp,
        'activity':activity_in,
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        'qlinks':qlinks()
    }
    return render(request, "__citi_profile_layout.html",context)
    
# product list view    
def product_list_view(request,*args,**kwargs):
    product = Index.objects.filter(is_listed=True,ref_service_code="pac")
    cities = City.objects.all()
    context={
        'pagetitle':"Find your adventure",
        'prod':product,
        'pagetitle': 'Holidays | Trips | Vacations - Packages',
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        
    }
    return render(request, "searchpage.html",context)
    
# activity list view    
def activity_list_view(request,*args,**kwargs):
    
    activities = Activity.objects.all()
    context={
        'pagetitle':"Find your adventure",
        'qlinks':qlinks(),
        'cities':city(),
        'countries':country(),
        'activities':activity(),
       
        
    }
    return render(request, "_activitypage.html",context)    
    
    
#package/item
def product_view(request,slug,*args,**kwargs):
    package = Package.objects.get(url_title=slug)
    itinerary = Itinerary.objects.get(id=package.itinerary_id)
    #product = Package.objects.all() # query set
    
    key = (package.tags).replace(",","").replace("\r","").replace("\n"," ").rstrip()
    bkey = (key.split(" "))
    while("" in bkey): 
        bkey.remove("") 
    
    
    product = Package.objects.filter(url_title=slug) #filter to get query set not the object alone...
    productb = product.exclude(id__in=product) #empty for least relevent. #typecasting... 
    
    
    for k in bkey:
        temp = Package.objects.filter(tags__icontains=k).exclude(id__in=product) 
        productb = productb|temp 
       
   
  
    product = productb
    
    
    
    
    context = {
        'slug':"rafting",
        'pagetitle': package.package_title ,
        'prod':package,
        'prods':product,
        'itin':itinerary,
        'qlinks':qlinks(),
        
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        
        'meta':True,
        'meta_keyword':package.keywords
    }
    return render(request, "__package_layout.html",context)
    
#activity/name
def activity_view(request,slug,*args,**kwargs):

    aname = Activity.objects.get(slug=slug)
    available = ActivitySale.objects.filter(name=aname)

    context={
        'pagetitle':aname.activity_name,
        'activity':aname,
        'avail':available,
        'qlinks':qlinks(),
        
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        'avail':available,
        
    }
    return render(request, "__activity_layout_list.html",context) 
    
#activity/name/location
def activity_content_view(request,name,loc,*args,**kwargs):
    available = ActivitySale.objects.get(slug=loc)
    nearby = ActivitySale.objects.filter(city = available.city)
   
    context = {
        
        'cities':city(),
        'countries':country(),
        'activities':activity(),
        'pagetitle': available.name.activity_name+" "+available.location,
        'sale': available,
        'nearby': nearby,
        'qlinks':qlinks(),
        'meta':False,
        
    }
    return render(request, "__activity_layout.html",context)    
    
#bookings    
def booking_p_view(request,slug,*args,**kwargs):
    
    date = request.GET.get('date')
    package= Package.objects.get(uid=slug)
    context = {
            
        'pagetitle': package.package_title ,
        'prod':package,
        'date':date,
        'cities':city(),
        'countries':country(),
        'activities':activity(),
            
        'meta':False,
    }
    if date is not None:
    
        valid_date=True
        try:
            datetime.datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            valid_date=False
         
        print(date)        
        print(valid_date)
        
        if valid_date:
            
            return render(request, "book_pac.html",context)
        else:
            return redirect('package_booking_profile',slug = slug) # redirecting to same view but this time without date in get...
            
    else:
        print ("this ran")
        return render(request, "book_pac.html",context)
        
        
def booking_a_view(request,slug,*args,**kwargs):
    
        
        available = ActivitySale.objects.get(uid=slug)
       
       
        context = {
            
            'pagetitle': available.name.activity_name+" "+available.location ,
            'sale':available,
            
            'cities':city(),
            'countries':country(),
            'activities':activity(),
            
            'meta':False,
        }
        return render(request, "book_act.html",context)
    

def checkout_p_view(request,*args,**kwargs):
    
    if request.method != 'POST':
        return redirect("/")
    else:
        slug = request.POST.get('slug')
        uid = request.POST.get('uid')
        package= Package.objects.get(url_title=slug,uid=uid)
       
        context = {
            'slug':"rafting",
            'pagetitle': package.package_title,
            'prod':package,
            
            'cities':city(),
            'countries':country(),
            'activities':activity(),
            
            'meta':False,
        }
        return render(request, "payment_pac.html",context)

        

    
    
# login view
def login_view(request,*args,**kwargs):
    #return HttpResponse('helo world')
    cities = City.objects.all()
    if request.user.is_authenticated:
        return redirect("/") 
    else:
        context={
            'pagetitle':"Login",
            
            'cities':city(),
            'countries':country(),
            'activities':activity(),
        }
        return render(request, "login.html",context)

#profile view #user
def profile_view(request):
    cities = City.objects.all()
    if request.user.is_authenticated:
        context={
            'pagetitle':"Profile",
            
            'cities':city(),
            'countries':country(),
            'activities':activity(),
            
        }
        return render(request,"profile.html",context)   
    else:
        return redirect("/")
       


# ajax view renderer

def register_view(request,*args,**kwargs):
    if request.method == 'POST':
        mail =request.POST.get("email")
        secret=request.POST.get("password")
        
        if request.user.is_authenticated:
            return HttpResponse('loggedIn') 
        else:
            getuser = User.objects.get(email=mail)
            uname = getuser.username
            user = authenticate(username=uname, password=secret)
            if user is not None:
                login(request, user)
                return HttpResponse('success')
            else:
                return HttpResponse('failed')
    else:
        return HttpResponse('invalid')
        
    
def signup_view(request,*args,**kwargs):
   
    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        secret = request.POST.get("password")
        conf = request.POST.get("conf")
        
        if(conf != secret):
            return HttpResponse("pnm") 
        else:
            if User.objects.filter(email=email).exists():
                return HttpResponse("axt")
            else:        
                unique_name = uuid.uuid4().hex[:8].upper()
                while User.objects.filter(username=unique_name).exists():
                    unique_name = uuid.uuid4().hex[:8].upper()
                uname = slugify(unique_name)    
                user = User.objects.create_user(uname, email, secret)
                user.first_name = fname
                user.last_name = lname
                user.profile.mobile = mobile
                user.save()
                response = "uct"
        
                return HttpResponse(response) 
            
    else:
        return HttpResponse('invalid')   
    

def logout_view(request):
    logout(request)
    src = (request.GET.get('src')) 
    return redirect(src)
    
   
def enq_view(request):

    if request.method == 'POST':
            
        if request.user.is_authenticated:
            is_signed_up=True
            user_id=request.user.id
        else:
            is_signed_up=False
            user_id=0
        
        product = request.POST.get("prod")
        product_id = request.POST.get("id")
        product_url = request.POST.get("url")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name","")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        message = request.POST.get("message")
        date = request.POST.get('date', 'NOTSET')
        adults = request.POST.get('adults', 'NOTSET')
        children = request.POST.get('children', 'NOTSET')
        
        e = Enquiry(first_name=first_name,last_name=last_name,product=product,product_id=product_id,email=email,mobile=mobile,message=message,product_url=product_url,date=date,adults=adults,children=children,is_signed_up=is_signed_up,user_id=user_id)
        e.save()
        
        return HttpResponse("enq_sub")
        
    else:
        return HttpResponse("Invalid request.")