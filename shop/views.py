from django.shortcuts import render
from django.http import HttpResponse
from .models import product,Contact,order,updateorder
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import checksum
MERCHANT_KEY = 'bKMfNxPPf_QdZppa';
# Create your views here.
def index(request):
    #products=product.objects.all()
    #print(products)

   # allprod=[[products,range(1,nslides),nslides],[products,range(1,nslides),nslides]]

    allprod=[]
    catprod=product.objects.values('category','id')     #fetching the products using category.
    cats={item['category'] for item in catprod}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil(n / 4 - (n // 4))
        allprod.append([prod,range(1,nslides),nslides])

    params = {'allprod': allprod}
    return render(request,'shop/index.html',params)


def searchMatch(query,item):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower():
      return True
    else:
        return False



def search(request):

    query=request.GET.get('search')
    allprod=[]
    catprod=product.objects.values('category','id')     #fetching the products using category.
    cats={item['category'] for item in catprod}
    for cat in cats:
        prodtemp=product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query ,item)]
        n = len(prod)
        nslides = n // 4 + ceil(n / 4 - (n // 4))
        if len(prod)!=0:
           allprod.append([prod,range(1,nslides),nslides])

    params = {'allprod': allprod,'msg':""}
    if len(allprod)==0 or len(query)<4:
        params={'msg':'please enter the relevent search'}
    return render(request, 'shop/search.html',params)










def about(request):
    return  render(request,'shop/about.html')


def contact(request):
    thank = False

    if request.method=='POST':

       print(request)
       name=request.POST.get('name','')
       email=request.POST.get('Email','')
       phone=request.POST.get('Contact No.','')
       desc=request.POST.get('Address','')
       print(name,email,phone,desc)
       contact=Contact(name=name,email=email,phone=phone,desc=desc)
       contact.save()
       thank=True
    return render(request, 'shop/contact.html',{'thank':thank})


def tracker(request):
    if request.method == 'POST':
        orderId=request.POST.get('orderId','')
        Email=request.POST.get('Email','')
       
        try:
            Order = order.objects.filter(order_id=orderId, email=Email)
            if len(Order) > 0:
                update = updateorder.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)


            else:
             return HttpResponse('error')


        except Exception as e:
            return HttpResponse('error')

    return render(request, 'shop/tracker.html')




def products(request,myid):
    #fetch the products using this myid.
    Product = product.objects.filter(id=myid)

    return render(request, 'shop/prodview.html',{'Product':Product[0]})


def checkout(request):
    return render(request, 'shop/checkout.html')



#def clearcart(request):
   # return render(request, 'shop/clearcart.html')


def productlist(request):
    context = {'product':product.objects.all()}
    return render(request,'shop/product.html',context)


def checkout(request):

    if request.method=='POST':
       print(request)
       items_json=request.POST.get('itemsjson','')
       name=request.POST.get('name','')
       amount=request.POST.get('amount','')
       email=request.POST.get('Email','')
       address=request.POST.get('Address1','') + ' ' + request.POST.get('Address2','')

       city=request.POST.get('City','')
       state=request.POST.get('State','')
       pin_code=request.POST.get('PinCode','')
       phone = request.POST.get('PhoneNumber', '')
       print(name,email,phone)
       Order=order(name=name,email=email,phone=phone,address=address,city=city,state=state,pin_code=pin_code,items_json=items_json,amount=amount)
       Order.save()
       update=updateorder(order_id=Order.order_id,update_desc='your order has been placed successfully')
       update.save()

       thank=True
       id=Order.order_id
       # return render(request, 'shop/checkout.html' ,{'thank':thank,'id':id})
       #request paytm to transfer the amount to your account after receiving payment from user.

       param_dict = {

           'MID':'DIY12386817555501617',
           'ORDER_ID': 'dddgfgfeeeh',
           'TXN_AMOUNT': str(amount),
           'CUST_ID': email,
           'INDUSTRY_TYPE_ID': 'Retail',
           'WEBSITE': 'WEBSTAGING',
           'CHANNEL_ID': 'WEB',
           'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

       }
       param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
       return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')

@csrf_exempt #gives a relaxation to this end pointi.e it provides a bypass to csrf tokens.

def handlerequest(request):
    # paytm will send you post request here.

    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            Checksum=form[i]

    verify=checksum.verify_checksum(response_dict,MERCHANT_KEY,Checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order Successful')

        else:
            print('Order was not successful because' + response_dict['RESPMSG'])

    return render(request,'shop/paymentstatus.html',{'response':response_dict})











