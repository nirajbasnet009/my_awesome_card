from django.shortcuts import render,redirect
from django.http import HttpResponse
from shop.models import Product,Contact,Orders,OrderUpdate
from math import ceil 
import json
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}
    for cat in cats:
         prod = Product.objects.filter(category=cat)
         n = len(prod)
         nslides = n//4+ceil(n/4-n//4) 
         allProds.append([prod,range(1,nslides),nslides])

    products = {'allProds':allProds}

    return render(request, 'shop/index.html',products)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if(request.method == 'POST'):
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        message = request.POST.get('message','')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        return render(request, 'shop/contact.html',{'thank':True})

    return render(request, 'shop/contact.html')

def tracker(request):
    try:
        if request.method == 'POST':
            order_id = request.POST.get('order_id',default=0)
            email = request.POST.get('email',default='hh')
            order = Orders.objects.filter(order_id=order_id,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
    except Exception as e:
        print(e)
        return HttpResponse('{}')

    return render(request, 'shop/tracker.html')
def searchMatch(query, product):
    '''returns true if query matches the product'''
    if query in product.product_name.lower() or query in product.desc.lower() or query in product.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category')
    print(catProds)
    cats = {item['category'] for item in catProds}
    for cat in cats:
         prodlist = Product.objects.filter(category=cat)
         print(prodlist)
         prod = [product for product in prodlist if searchMatch(query,product)]
         n = len(prod)
         nslides = n//4+ceil(n/4-n//4) 
         if len(prod) != 0:
            allProds.append([prod,range(1,nslides),nslides])
            
    products = {'allProds':allProds,'msg':''}
    if len(allProds) == 0 or len(query)<4:
        products = {'msg':"please make sure to enter relevant search query"}

    return render(request, 'shop/search.html',products)

def productview(request,myid):
    # Fetching items using id
    prod = Product.objects.filter(id=myid)
    print(prod)
    return render(request, 'shop/productview.html',{'prod':prod[0]})

def checkout(request):
    if(request.method == 'POST'):
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone',0)
        total_amt = int(request.POST.get('total_amt',0))
        address = request.POST.get('address1','')+' '+ request.POST.get('address2','')
        # order_id = request.POST.get('order_id','')
        items_json = request.POST.get('items_json','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code',0)
        order = Orders(items_json=items_json,amount=total_amt,name=name,email=email,address=address,city=city, state=state, phone=phone, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc ="The order has been placed.")
        update.save()
        # return render(request, 'shop/checkout.html',{'thank':True, 'id':order.order_id})
        # request khalti to transfer the amount to your account after payment by user
      
        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        payload = json.dumps({
            "return_url": "http://127.0.0.1:8000/shop/verifypayment",
            "website_url": "http://127.0.0.1:8000",
            "amount":1000,
            "purchase_order_id": order.order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": name,
                "email": email,
                "phone": phone
            }
        })
        headers = {
            'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        payment_url = response.json()['payment_url']
        return redirect(payment_url)
        # return render(request, 'shop/checkout.html',{'thank':True, 'id':order.order_id})
                    
    return render(request, 'shop/checkout.html')
# def checkout(request):
#     if request.method == 'POST':
#         name = request.POST.get('name', '')
#         email = request.POST.get('email', '')
#         phone = request.POST.get('phone', 0)
#         total_amt = request.POST.get('total_amt', 0)
#         address = request.POST.get('address1', '') + ' ' + request.POST.get('address2', '')
#         items_json = request.POST.get('items_json', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zip_code = request.POST.get('zip_code', 0)
#         order = Orders(items_json=items_json, amount=total_amt, name=name, email=email, address=address,
#                        city=city, state=state, phone=phone, zip_code=zip_code)
#         order.save()
#         update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
#         update.save()

#         url = "https://a.khalti.com/api/v2/epayment/initiate/"

#         payload = json.dumps({
#             "return_url": "http://127.0.0.1:8000/shop/verifypayment",
#             "website_url": "http://127.0.0.1:8000",
#             "amount": 1000,
#             "purchase_order_id": order.order_id,
#             "purchase_order_name": "test",
#             "customer_info": {
#                 "name": name,
#                 "email": email,
#                 "phone": phone
#             }
#         })
#         headers = {
#             'Authorization': 'key test_secret_key_72de9b06f06a400ebb29783a5a417e37',
#             'Content-Type': 'application/json',
#         }

#         response = requests.request("POST", url, headers=headers, data=payload)

#         response_data = response.json()
#         print(response_data)
#         payment_url = response_data.get('payment_url')

#         if payment_url:
#             return redirect(payment_url)
#         else:
#             # Handle the case when 'payment_url' is not present in the response
#             return HttpResponse("Error: Payment URL not available.")

#     return render(request, 'shop/checkout.html')


def verifypayment(request):
    # khalti will send post request
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get('pidx')
    payload = json.dumps({
        'pidx': pidx
    })
    headers = {
        'Authorization': "key test_secret_key_72de9b06f06a400ebb29783a5a417e37",
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if(response.status == "Completed"):
        print('success')

    return render(request,'shop/checkout.html',{'thank':True})
