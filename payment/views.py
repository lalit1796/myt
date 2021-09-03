from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
import random
import uuid
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from client.models import Enquiry, BookingPackage, BookingActivity, Profile, Order
from django.shortcuts import redirect
from tours.models import Package, ActivitySale

key="dZB1Ieyn"
SALT = "q674HF1A91" 
PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
#PAYU_BASE_URL = "https://secure.payu.in/_payment"
action = ''

def hash(hash_string):
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    

def bill_calc_act(n,obj):
    return 1;


def checkout_view(request,orderid,*args,**kwargs):
    
    if not 'myorders' in request.session or not request.session['myorders']:
        request.session['myorders'] = ["0"]
        
    orderinsession =  request.session['myorders']   
    print(orderinsession)
    
    if request.method == 'POST':
        
        lfname=request.POST.get("fname","anonymous")
        llname=request.POST.get("lname","")
        pmobile=request.POST.get("mobile","")
        pemail=request.POST.get("email","")
        pdate=request.POST.get("date","")
        puid=request.POST.get("uid",0)
        pid=request.POST.get("id",0)
        service_code=request.POST.get("code")
        
        
        p_adult_count=request.POST.get("adults",0)
        p_kids_count=request.POST.get("children",0)
        
        ptotal_count= int(p_adult_count) + int(p_kids_count)
        
        # below variables to be set by sale table // RESETS
        p_adult_dis=0
        p_kids_dis=0
        p_adult_per_cost= 0
        p_kids_per_cost=0 
        p_gst = 0
        
        if service_code == 'act':
            product = ActivitySale.objects.get(uid=puid)
            p_adult_dis=0 # no discount avaliable
            p_kids_dis=0 # no discount possible
            
            p_adult_per_cost= product.prize
            p_kids_per_cost=0 #since this portal is not open for kids separately...
            p_gst = 5
        
        elif service_code == 'pac':
            p_gst = 10
        
        
        
        
        
        if  orderid == 'new': # if new
           
            for o in orderinsession: #checking if order with order id , product_uid, to the session in machine containg order ids exist or not.
                if Order.objects.filter(product_uid=puid,service_code=service_code,id=o).exists():
                    exist = o
                    break;
                else:
                    exist = None
                
            if exist:
            
                record = Order.objects.get(product_uid=puid,service_code=service_code,id=exist) #since id is auto increment so collision will not occur.
                
                #if exists then update with new variables
                
                
                record.first_name=lfname
                record.last_name=llname
                record.email=pemail
                record.mobile=pmobile
                record.date=pdate
                record.product_uid=puid
                record.product_id=pid
                record.service_code=service_code
                
                record.total_count = ptotal_count
                record.adult_count=p_adult_count
                record.kids_count=p_kids_count
                
                record.adult_per_cost=p_adult_per_cost
                record.kids_per_cost=p_kids_per_cost
                
                record.gst=p_gst
                
            else:
            
                record= Order(
                    first_name=lfname,
                    last_name=llname,
                    email=pemail,
                    mobile=pmobile,
                    date=pdate,
                    product_uid=puid,
                    service_code=service_code,
                    product_id=pid,
                    total_count = ptotal_count,
                    adult_count=p_adult_count,
                    kids_count=p_kids_count,
                    adult_per_cost=p_adult_per_cost,
                    kids_per_cost=p_kids_per_cost,
                    gst=p_gst
                    )
                request.session['myorders'] = orderinsession
                print(orderinsession)
            
            record.txn = "NOT ISSUED"
            record.total_amount = 0
            record.amount_paid = 0
            record.save()
            # saving all records... then creating final pay using its own property then saving again.

           
            orderinsession.append(record.id) # order in session 
            
            
            orderid = record.id
            return redirect('checkout_order',orderid = orderid)
            
            
        else:
            return HttpResponse("Invalid request.")
            
                
    else:
               
        if  Order.objects.filter(id=orderid).exists():  
            
            record = Order.objects.get(id=orderid) 
            
                    # lead-passenger-name mobile email date total-people 
            rand = bytes(bytearray([random.randint(0,200)]))    
            hash_object = hashlib.sha256(rand) 
            txnid = hash_object.hexdigest()[0:20]
            hashh = ''
            data={}
            data['txnid']=txnid
            data['key']=key
            data['amount']=record.finalpay()
            data['productinfo']=record.id
            data['firstname']=record.first_name
            data['lastname']=record.last_name
            data['email']=record.email
            data['service_provider']="payu_paisa"
            data["surl"]="http://127.0.0.1:8000/payment/status"
            data["furl"]="http://127.0.0.1:8000/payment/status"
            data["phone"]=record.mobile
            data['udf1']="" #gst
            data['udf2']="" #adult cost
            data['udf3']="" #kid cost
            data['udf4']="" #net discount
            data['udf5']="" #dis amount
            data['udf6']=""
            data['udf7']="" 
            data['udf8']=""
            data['udf9']=""
            data['udf10']=""
            
            record.total_amount = record.finalpay()
            record.save()
                
            #order = Order
                
            
                
            hashSequence="key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
            hash_string=""
                
            hashVarsSeq=hashSequence.split('|')
                
            for i in hashVarsSeq:
                try:
                    hash_string+=str(data[i])
                except Exception:
                    hash_string+=''
                hash_string+='|'
            hash_string+=SALT
            hashh=hash(hash_string) #from hash function 
                
            data["hash_string"]=hash_string
            data["hashh"]=hashh
            action=PAYU_BASE_URL
            
            context={
                'record' : record,
                'data' : data,
                'action' : action
             }
                
                
                
            return render(request, "checkout_act.html",context)
            
        else: # if slug is changed
            
            return HttpResponse("This is not a valid order. Please choose a valid order.")



    


@csrf_protect
@csrf_exempt
def payment_response_view(request):
    if request.method == 'POST':
        status=request.POST["status"]
        firstname=request.POST["firstname"]
        amount=request.POST["amount"]
        txnid=request.POST["txnid"]
        posted_hash=request.POST["hash"]
        key=request.POST["key"]
        productinfo=request.POST["productinfo"]
        email=request.POST["email"]
        salt=SALT
        
        lname=request.POST.get("lastname")
        mobile=request.POST.get("mobile")
        
        data = {}
        data['status']=status
        data['firstname']=firstname
        data['amount']=amount
        data['txnid']=txnid
        data['productinfo']=productinfo
        data['email']=email
        data['lastname']=lname
        data['mobile']=mobile
        try:
            additionalCharges=request.POST["additionalCharges"]
            retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
        except Exception:
            retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
        hashh=hash(retHashSeq) #from hash function
        if(hashh != posted_hash):
            data['valid']=False
            
        else:
            data['valid']=True
            order =  Order.objects.get(id=productinfo)
            order.is_successfully_paid=True
            order.txn = txnid 
            
            order.save()
            

        context={
            'data':data,
            'order':order
        }    
        return render(request,"booking_payment_response.html",context)
    
    else:
        return redirect("/")
	
