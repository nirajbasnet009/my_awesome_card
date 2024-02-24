from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product 
from math import ceil 
# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values('category', 'id')
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
    return render(request, 'shop/index1.html')

def tracker(request):
    return HttpResponse('We are at tracker')

def search(request):
    return HttpResponse('We are at search')

def productview(request):
    return HttpResponse('We are at productview')

def checkout(request):
    return HttpResponse('We are at checkout')