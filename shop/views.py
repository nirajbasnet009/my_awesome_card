from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product,Contact,Orders,OrderUpdate
from math import ceil 
import json
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

def search(request):
    return HttpResponse('We are at search')

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
        address = request.POST.get('address1','')+' '+ request.POST.get('address2','')
        # order_id = request.POST.get('order_id','')
        items_json = request.POST.get('items_json','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code',0)
        order = Orders(items_json=items_json,name=name,email=email,address=address,city=city, state=state, phone=phone, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc ="The order has been placed.")
        update.save()
        print(update.update_id)
        return render(request, 'shop/checkout.html',{'thank':True, 'id':order.order_id})
    return render(request, 'shop/checkout.html')

